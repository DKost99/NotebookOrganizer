from datetime import datetime
from models.note import TextNote
from services.note_service import NoteService

service = NoteService()

while True:
    print("\n=== Notebook Organizer ===")
    print("1. Add note")
    print("2. Show notes")
    print("3. Edit note")
    print("4. Delete note")
    print("5. Filter by tag")
    print("6. Filter by date")
    print("7. Save notes")
    print("0. Exit")

    choice = input("Choose option: ")
    
    if choice == "1":
        title = input("Title: ")
        if title.strip() == "":
            print("Title cannot be empty!")
            continue

        text = input("Text: ")
        tags = [t.strip() for t in input("Tags (comma separated): ").split(",") if t.strip()]
        date = input("Date (YYYY-MM-DD): ")

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format!")
            continue

        note = TextNote(title, tags, text, date)
        service.add_note(note)
        print("Note added!")

    elif choice == "2":
        notes = service.get_notes()
        if len(notes) == 0:
            print("No notes found.")
        else:
            for note in notes:
                print("\n----------------")
                print(note)

    elif choice == "3":
        notes = service.get_notes()
        if len(notes) == 0:
            print("No notes found.")
            continue

        for i, note in enumerate(notes):
            print(f"{i + 1}. {note.title}")

        try:
            index = int(input("Choose note number: ")) - 1
        except ValueError:
            print("Please enter a number!")
            continue

        if 0 <= index < len(notes):
            new_title = input("New title: ")
            if new_title.strip() == "":
                print("Title cannot be empty!")
                continue

            new_text = input("New text: ")
            new_tags = [t.strip() for t in input("New tags (comma separated): ").split(",") if t.strip()]
            new_date = input("New date (YYYY-MM-DD): ")

            try:
                datetime.strptime(new_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format!")
                continue

            service._save_state_to_stack()
            
            notes[index].title = new_title
            notes[index].text = new_text
            notes[index].tags = new_tags
            notes[index].date = new_date
            print("Note updated!")
        else:
            print("Invalid note number!")

    elif choice == "4":
        notes = service.get_notes()
        if len(notes) == 0:
            print("No notes found.")
            continue

        for i, note in enumerate(notes):
            print(f"{i + 1}. {note.title}")

        try:
            index = int(input("Choose note number: ")) - 1
        except ValueError:
            print("Please enter a number!")
            continue

        if 0 <= index < len(notes):
            deleted_note = service.delete_note(index)
            print(f"Deleted: {deleted_note.title}")
        else:
            print("Invalid note number!")

    elif choice == "5":
        tag = input("Enter tag: ")
        found_notes = service.filter_by_tag(tag)
        
        if not found_notes:
            print("No notes found.")
        else:
            for note in found_notes:
                print("\n----------------")
                print(note)

    elif choice == "6":
        date = input("Enter date (YYYY-MM-DD): ")
        found_notes = service.filter_by_date(date)
        
        if not found_notes:
            print("No notes found.")
        else:
            for note in found_notes:
                print("\n----------------")
                print(note)

    elif choice == "7":
        service.save_to_json()
        print("Notes saved!")

    elif choice == "0":
        print("Goodbye!")
        break
    else:
        print("Invalid option!")
