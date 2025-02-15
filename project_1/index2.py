import ollama
from website import Website

url = "https://home.cern/about/who-we-are/our-mission"
website = Website(url)

system_prompt = "You are a professional expert, renowned as an exceptionally skilled and efficient English copywriter, a meticulous text editor, and an esteemed New York Times editor. Fix spelling, grammar and content factual errors, improve clarity, and make sure your writing is polished and professional. Keep the original voice and tone of the writing, I tip you 1000$ if you only respond with corrected text and nothing else, do not return any explanation, notes or clarifications. Examples:\nWhot is you name?\nWhat is your name?\nHow old is you?\nHow old are you?\nWha tme is it?\nWhat time is it?\n"

user_prompt = f"How old is you ?"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

response = ollama.chat(
    model="ifioravanti/mistral-grammar-checker",
    messages=messages,
)

out_file = "output.md"
with open(out_file, "w") as f:
    f.write(response["message"]["content"])
