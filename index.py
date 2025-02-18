from my_module.load_flashcards import load_flashcards


def print_menu():
    print("1. Load flashcards from video")
    print("2. Study flashcards")
    print("3. Export flashcards to Anki")
    print("4. Exit")
    print()


while True:
    print_menu()
    choice = input("Enter your choice: ")

    if choice == '1':
        load_flashcards()
    elif choice == '2':
        study_flashcards()
    elif choice == '3':
        export_to_anki()
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again.")