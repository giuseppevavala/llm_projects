import logging
import os

from my_llm_sdk.models.factory import ModelFactory, ModelType

SYSTEM_PROMPT = "Il tuo unico compito è convertire file di mappe mentali dal formato txt in file mark down, in modo che siano compatibili con Xmind."

TEXT_DIRECTORY = "./file_di_testo"
MD_DIRECTORY = "./file_md"


def convert_file_to_markdown(file_name: str, openai_model):

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    src_file_path = f"{TEXT_DIRECTORY}/{file_name}.txt"
    dst_file_path = f"{MD_DIRECTORY}/{file_name}.md"

    with open(src_file_path, "r") as f:
        text_file = f.read()
        messages.append({"role": "user", "content": text_file})

    response = openai_model.generate_response(messages)

    if response.startswith("```markdown\n"):
        response = response[12:]

    if response.endswith("```"):
        response = response[:-3]

    with open(dst_file_path, "w") as f:
        f.write(response)


def main():
    openai_model = ModelFactory.create_model(ModelType.OPENAI)

    for file_name in os.listdir(TEXT_DIRECTORY):
        if file_name.endswith(".txt"):
            file_name = file_name[:-4]
            convert_file_to_markdown(file_name, openai_model)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
