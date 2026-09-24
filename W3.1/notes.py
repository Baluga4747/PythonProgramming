from pathlib import Path

file_path = Path(__file__).resolve().parent / "class_notes.txt"

note = input("Enter a note: ")

try:
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(note + "\n")

    with open(file_path, "r", encoding="utf-8") as file:
        notes = file.read()

    print("\nSaved notes:")
    print(notes, end="")

except OSError:
    print("Could not save the note.")