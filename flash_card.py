import os
from colorama import init, Fore, Back, Style
import readchar

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_size():
    """Ottiene le dimensioni del terminale"""
    return os.get_terminal_size()

def draw_card(text, width=40, height=10, is_front=True, to_study=0, studied=0, total_cards=0):
    """Disegna una flashcard ASCII colorata con il testo centrato"""
    # Colori diversi per fronte e retro
    card_color = Fore.CYAN if is_front else Fore.GREEN
    text_color = Fore.YELLOW if is_front else Fore.WHITE
    
    top_bottom = card_color + "+" + "="*(width-2) + "+" + Style.RESET_ALL
    empty_line = card_color + "|" + " "*(width-2) + "|" + Style.RESET_ALL
    
    # Centra il testo
    text_lines = text.split('\n')
    centered_text = []
    for line in text_lines:
        centered_text.append(line.center(width-2))
    
    # Calcola le linee vuote prima e dopo il testo
    total_empty_lines = height - 2 - len(text_lines)
    top_padding = total_empty_lines // 2
    bottom_padding = total_empty_lines - top_padding
    
    # Calcola il padding verticale per centrare la carta nello schermo
    terminal_height, terminal_width = get_terminal_size().lines, get_terminal_size().columns
    vertical_padding = (terminal_height - height) // 2
    horizontal_padding = (terminal_width - width) // 2
    
    # Aggiungi padding verticale
    print('\n' * (vertical_padding - 1))
    
    # Aggiungi i contatori
    if to_study is not None and studied is not None:
        counter_text = f"{Fore.RED}{Style.BRIGHT}{to_study}{Style.RESET_ALL}   {Fore.GREEN}{Style.BRIGHT}{studied}{Style.RESET_ALL}"
        print(f"\033[{vertical_padding + 1};{horizontal_padding}H{counter_text}")
    
    if total_cards is not None:
        count_cards = studied + to_study
        total_text = f"{Fore.WHITE}{Style.BRIGHT}{count_cards}/{total_cards}{Style.RESET_ALL}"
        # Posiziona il totale nell'angolo superiore destro
        print(f"\033[{vertical_padding + 1};{horizontal_padding + width - len(str(total_cards))}H{total_text}")
    
    # Disegna la carta
    for line in [top_bottom, *[empty_line]*top_padding, 
                 *[card_color + "|" + text_color + line + card_color + "|" + Style.RESET_ALL for line in centered_text],
                 *[empty_line]*bottom_padding, top_bottom]:
        print(" " * horizontal_padding + line)

def print_bottom_message(message):
    """Stampa un messaggio nell'ultima riga dello schermo"""
    terminal_height = get_terminal_size().lines
    # Sposta il cursore all'ultima riga
    print(f"\033[{terminal_height};0H", end='')
    print(message)

def show_flashcard(front_text, back_text, to_study=None, studied=None, total_cards=None) -> bool:
    """Gestisce l'interazione con la flashcard"""
    init()  # Inizializza colorama
    
    # Mostra il fronte della carta
    clear_screen()
    draw_card(front_text, is_front=True, to_study=to_study, studied=studied, total_cards=total_cards)
    print_bottom_message("Premi SPAZIO per vedere la risposta...")
    
    # Aspetta che l'utente prema spazio
    while True:
        key = readchar.readchar()
        if key == ' ':
            break
    
    # Mostra il retro della carta
    clear_screen()
    draw_card(back_text, is_front=False, to_study=to_study, studied=studied, total_cards=total_cards)
    print_bottom_message("Conosci questa carta? Premi INVIO se la conosci, TAB se non la conosci")
    
    # Aspetta la risposta dell'utente
    while True:
        key = readchar.readchar()
        if key == '\t':  # TAB
            return False
        elif key == '\n':  # INVIO
            return True

if __name__ == "__main__":
    # Esempio di utilizzo
    front = "Go (verb.)"
    back = "Andare\n(to go, went, gone)"
    show_flashcard(front, back)