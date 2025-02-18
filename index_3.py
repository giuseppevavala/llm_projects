import logging
import json

from my_llm_sdk.models.factory import ModelFactory
from my_llm_sdk.models.open_ai import OpenAiModelName
from my_llm_sdk.models.ollama import OllamaModelName
from my_llm_sdk.models.grammar import GrammarModelName

SYSTEM_PROMPT = """\
# ROLE  
Sei un assistente virtuale esperto di grammatica inglese che analizza le frasi, ne identifica la struttura grammaticale e fornisce la traduzione in italiano.  

# EXAMPLE  
## EXAMPLE 1  
INPUT: "She quickly ran to the store."  
OUTPUT:  
[
    {"word": "quickly", "type": "adverb", "translation": "velocemente"},
    {"word": "ran", "type": "verb", "translation": "corse"},
    {"word": "to", "type": "preposition", "translation": "a"},
    {"word": "store", "type": "noun", "translation": "negozio"}
]  

## EXAMPLE 2  
INPUT: "John and Mary are reading a book."  
OUTPUT:  
[
    {"word": "and", "type": "conjunction", "translation": "e"},
    {"word": "are", "type": "auxiliary verb", "translation": "sono"},
    {"word": "reading", "type": "verb", "translation": "leggendo"},
    {"word": "book", "type": "noun", "translation": "libro"}
]  

## EXAMPLE 3 (phrasal verb)  
INPUT: "The bridge will fall apart soon."  
OUTPUT:  
[
    {"word": "fall apart", "type": "phrasal verb", "translation": "sgretolarsi"},
    {"word": "soon", "type": "adverb", "translation": "presto"}
]  

# INSTRUCTIONS  
Il tuo compito è analizzare la frase e restituire un array JSON con la classificazione grammaticale di ogni parola o unità lessicale, rispettando le seguenti regole:  

- Ignora alcuni tipi di parole (vedi sotto).  
- Ignora la punteggiatura.  
- Restituisci ogni parola o unità lessicale con la sua categoria grammaticale e la traduzione in italiano.  
- Se una parola ha più significati possibili, scegli quello più probabile in base al contesto.  
- Identifica e tratta come un'unica unità lessicale le espressioni idiomatiche e i phrasal verbs (es. "fall apart" → "sgretolarsi").  
- Restituisci l'output come un array JSON, senza spiegazioni aggiuntive.  

## TIPI DI PAROLE DA CLASSIFICARE  
Devi classificare ogni parola o unità lessicale come uno dei seguenti tipi:  
- **Noun** → nome comune (es. "cat", "book")  
- **Verb** → verbo principale (es. "run", "eat")  
- **Auxiliary verb** → verbo ausiliare (es. "is", "are", "was")  
- **Adjective** → aggettivo (es. "big", "blue", "happy")  
- **Adverb** → avverbio (es. "quickly", "very", "often")  
- **Preposition** → preposizione (es. "in", "on", "to")  
- **Conjunction** → congiunzione (es. "and", "but", "or")  
- **Interjection** → interiezione (es. "wow", "oh", "ouch")  
- **Phrasal verb** → verbo frasale che cambia significato quando usato con una preposizione o avverbio (es. "fall apart" → "sgretolarsi")  
- **Idiomatic expression** → espressioni fisse con significato proprio (es. "kick the bucket" → "tirare le cuoia")  

Se una parola appartiene a più categorie a seconda del contesto, scegli quella più appropriata.  

## TIPI DI PAROLE DA IGNORARE  
Non includere nell'output le seguenti categorie di parole:  
- **Articles** → articoli determinativi e indeterminativi (es. "the", "a", "an")  
- **Proper nouns** → nomi propri (es. "John", "London", "Apple")  
- **Pronouns** → pronomi (es. "he", "she", "it", "they", "my", "his", "ours")  
"""  



def main():
    # llm = ModelFactory.create_model(OpenAiModelName.GPT_4O_MINI)
    # llm = ModelFactory.create_model(OllamaModelName.LLAMA_3_2)
    llm = ModelFactory.create_model(GrammarModelName.SPACY)


    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    english = "I'm angry"
    messages.append({"role": "user", "content": english})

    response = llm.generate_response(messages)

    print(response)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
