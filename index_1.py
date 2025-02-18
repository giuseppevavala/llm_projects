import json

from word_repository import WordRepository
from flash_card import show_flashcard

input_file = "return.json"

word_repository = WordRepository()

with open(input_file) as f:
    flashcards = json.load(f)

total_cards = len(flashcards)
counter = 0
known_counter = 0
not_known_counter = 0

for flashcard in flashcards:
    counter += 1

    known = word_repository.is_word_known(flashcard["word"], flashcard["type"])
    if known is not None:
        if known:
            known_counter += 1
        else:
            not_known_counter += 1
        continue

    front_text = flashcard["word"] + " (" + flashcard["type"] + ")"
    back_text = flashcard["translate_in_context"] + " ," + flashcard["common_translate"] 

    if flashcard["common_translate"] != flashcard["translate_in_context"]:
        translate = f"{flashcard["translate_in_context"]} , {flashcard["common_translate"]}"
    else:
        translate = flashcard["translate_in_context"]

    if show_flashcard(front_text, back_text, known_counter, not_known_counter, total_cards):
        word_repository.add_word(flashcard["word"], flashcard["type"], is_known=True, translate=translate)
    else:
        word_repository.add_word(flashcard["word"], flashcard["type"], is_known=False, translate=translate)

