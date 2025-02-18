from word_repository import WordRepository


header = """#separator:tab
#html:true
#tags column:3
"""

out_fiile = open("anki.txt", "w")

repo = WordRepository()

out_fiile.write(header)

for word in repo.get_words():
    if not word["is_known"]:
        out_fiile.write(f"{word['word']} ({word['type']})\t{word['translate']}\n")