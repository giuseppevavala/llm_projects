import gradio as gr
import os
import copy

from prompt import CHAT_SYSTEM_PROMPT
from prompt import GRAMMAR_SYSTEM_PROMPT
from prompt import CONTEXT_SYSTEM_PROMPT
from prompt import ENGLISH_LEVEL

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

openai = OpenAI()
MODEL = "gpt-4o-mini"


def send_to_openai_stram(messages):
    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

def send_to_openai(messages):
    ret = openai.chat.completions.create(model=MODEL, messages=messages)
    ret = ret.choices[0].message.content
    return ret

def send_to_openai_grammar(messages):
    if len(messages) < 2:
        return ""

    messages = copy.deepcopy(messages)
    messages = messages[-2:]
    system_prompt = GRAMMAR_SYSTEM_PROMPT
    messages.append({"role": "system", "content": system_prompt})
    ret = openai.chat.completions.create(model=MODEL, messages=messages)
    ret = ret.choices[0].message.content
    return ret


def send_to_openai_chat(messages, situation, english_level):
    messages = copy.deepcopy(messages)
    system_prompt = CHAT_SYSTEM_PROMPT.format(situation=situation)
    system_prompt += ENGLISH_LEVEL[english_level]
    messages.append({"role": "system", "content": system_prompt})
    ret = send_to_openai(messages)
    return ret

def send_to_openai_context(messages, situation):
    if len(messages) < 4:
        return ""

    messages = copy.deepcopy(messages)
    messages = messages[-4:]
    system_prompt = CONTEXT_SYSTEM_PROMPT.format(situation=situation)
    messages.append({"role": "system", "content": system_prompt})
    ret = send_to_openai(messages)
    return ret


def chat_function(message, history, situation_text, english_level):
    history.append({"role": "user", "content": message})

    ret = send_to_openai_chat(history, situation_text, english_level)
    grammar_suggestion = send_to_openai_grammar(history)
    context_suggestion = send_to_openai_context(history, situation_text)

    history.append({"role": "assistant", "content": ret})
    history = history[-15:]

    return "", history, grammar_suggestion, context_suggestion


with gr.Blocks() as demo:
    with gr.Row():  # Crea una riga che conterrà le due colonne
        with gr.Column(scale=1):  # Prima colonna
            situation_text = gr.Textbox(
                label="Situation", lines=1, value="colloquio di lavoro"
            )
            english_level = gr.Radio(
                choices=["A1", "A2", "B1", "B2", "C1", "C2"],
                label="English level",
                value="B1",
            )
            chat_box = gr.Chatbot(type="messages", value=[], autoscroll=True)
            message = gr.Textbox(label="Your message:", lines=1)

        with gr.Column(scale=1):  # Seconda colonna
            grammar_teacher_tb = gr.Textbox(label="Grammar", lines=14)
            context_teacher_tb = gr.Textbox(label="Suggestion", lines=14)
        
        message.submit(
                fn=chat_function,
                inputs=[message, chat_box, situation_text, english_level],
                outputs=[message, chat_box, grammar_teacher_tb, context_teacher_tb],
            )

demo.launch(share=False)
