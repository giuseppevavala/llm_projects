import os
import pysrt
import html

from bs4 import BeautifulSoup

def load_flashcards():
    video_file = input("Enter the name of the file: ")
    if not os.path.exists(video_file):
        raise Exception("File not found")
    
    num_stream = input("Enter the number of the stream: ")

    os.system(f"ffmpeg -i {video_file.replace(" ", "\\ ")} -map 0:s:{num_stream} ./data/subs.srt")
    if not os.path.exists("./data/subs.srt") or os.stat("./data/subs.srt").st_size == 0:
        raise Exception("Subtitle file not found or empty")
    
    
        
    cleaned_text = clean_subtitles("./data/subs.srt")

    with open("./data/subs.txt", "w", encoding='utf-8') as f:
        f.write(cleaned_text)



def clean_subtitles(input_file):    
    subs = pysrt.open(input_file)
    cleaned_text = []
    
    for sub in subs:
        # Salta le linee che contengono crediti dei sottotitoli
        if 'SUBTITLE TRANSLATION BY:' in sub.text:
            continue
            
        # Rimuovi tutti i tag HTML e decodifica le entità HTML
        text = BeautifulSoup(sub.text, "html.parser").get_text()
        text = html.unescape(text).strip()
        
        # Aggiungi solo se la linea contiene testo
        if text:
            cleaned_text.append(text)
    
    return '\n'.join(cleaned_text)