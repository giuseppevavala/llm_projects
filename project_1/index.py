import ollama
from website import Website

url = "https://home.cern/about/who-we-are/our-mission"
website = Website(url)

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

user_prompt = f"Website: {website.url}\n\n{website.text}"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

response = ollama.chat(
    model="llama3.2",
    messages=messages,
)

out_file = "output.md"
with open(out_file, "w") as f:
    f.write(response["message"]["content"])
