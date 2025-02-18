import json

class WordRepository:
    def __init__(self, json_file = "words.json"):
        self.json_file = json_file

    def get_words(self) -> list:
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        
    def word_exists(self, word, word_type):
        try:
            with open(self.json_file, 'r') as f:
                words = json.load(f)
                return any(w["word"] == word and w["type"] == word_type for w in words)
        except FileNotFoundError:
            return False
            
    def add_word(self, word, word_type, is_known, translate=""):
        try:
            with open(self.json_file, 'r') as f:
                words = json.load(f)
        except FileNotFoundError:
            words = []
            
        if not self.word_exists(word, word_type):
            new_word = {
                "word": word,
                "type": word_type,
                "is_known": is_known,
                "translate": translate
            }
            words.append(new_word)
            
            with open(self.json_file, 'w') as f:
                json.dump(words, f, indent=4)
            return True
        return False
    
    def is_word_known(self, word, word_type):
        try:
            with open(self.json_file, 'r') as f:
                words = json.load(f)
                for w in words:
                    if w["word"] == word and w["type"] == word_type:
                        return w.get("is_known", False)
                return None  # Ritorna None se la parola non esiste
        except FileNotFoundError:
            return None

