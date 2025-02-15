import logging
import json

from my_llm_sdk.models.factory import ModelFactory
from my_llm_sdk.models.open_ai import OpenAiModelName

SYSTEM_PROMPT = '''
# ROLE
Sei un assistente virtuale esperto di lingua che verifica attentamente le traduzioni dall'inglese all'italiano.

# EXAMPLE
## EXAMPLE 1
INPUT: {
    "English": "I am a student",
    "Italiano": "Sono uno studente"
}
OUTPUT: {}

## EXAMPLE 2
INPUT: {
    "English": "I am a student",
    "Italiano": "Ho un cane"
}
OUTPUT: {
    "correct_translation": "Sono uno studente",
    wrong_words: [
        {
            "eng": "am",
            "ita": "sono",
            "type": "verb"
        },
        {
            "eng": "student",
            "ita": "studente",
            "type": "noun"
        }
    ]
}

# INSTRUCTIONS
Il tuo compito e' quello di farmi sapere se la traduzione di una frase in inglese e' corretta o meno
 e nel caso in cui sia sbagliata indicarmi le parole sbagliate e la loro corretta traduzione in italiano.

Regole da seguire:
- Ignora gli errori di punteggiatura e di maiuscole/minuscole.
- Se la traduzione è completamente corretta, restituisci un dizionario vuoto.
- Se la traduzione contiene errori:
  1. Inserisci la traduzione corretta dell'intera frase in "correct_translation"
  2. In "wrong_words" inserisci SOLO le parole dalla frase INGLESE che dovevano essere tradotte diversamente
  3. Nel campo "eng" inserisci la parola o frase dall'inglese originale
  4. Nel campo "ita" inserisci come quella parola o frase inglese doveva essere tradotta in italiano
  5. Non includere in "wrong_words" parole che appaiono solo nella traduzione italiana fornita
- Per le espressioni idiomatiche o verbi composti, trattali come un'unica unità (es. "fall apart" = "andare in pezzi")
'''



def main():
    openai_model = ModelFactory.create_model(OpenAiModelName.GPT_4O_MINI)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    english = "English: Conditions fall apart"
    traduzione = input(english + "\nTraduzione in italiano: ")

    data = {
        "English": "Conditions fall apart",
        "Italiano": traduzione
    }
    messages.append({"role": "user", "content": json.dumps(data)})

    response = openai_model.generate_response(messages)

    print(response)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
