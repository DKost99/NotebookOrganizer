import json
import os
import copy
from models.note import Note

class NoteService:
    def __init__(self):
        self.notes = []
        self.undo_stack = []
        self.filepath = "data/notes.json"
        self.load_from_json()

    def _save_state_to_stack(self):
        """Сохранение копии текущего списка для отмены изменений"""
        self.undo_stack.append(copy.deepcopy(self.notes))

    def undo(self) -> bool:
        """Откат к предыдущему состоянию списка заметок"""
        if not self.undo_stack:
            return False
        self.notes = self.undo_stack.pop()
        return True

    def add_note(self, note):
        self._save_state_to_stack()
        self.notes.append(note)

    def get_notes(self):
        return self.notes

    def update_note(self, index: int, updated_note) -> bool:
        """Обновление существующей заметки"""
        if 0 <= index < len(self.notes):
            self._save_state_to_stack()
            self.notes[index] = updated_note
            return True
        return False

    def delete_note(self, index: int):
        if 0 <= index < len(self.notes):
            self._save_state_to_stack()
            return self.notes.pop(index)
        return None

    def filter_by_tag(self, tag: str) -> list:
        return [note for note in self.notes if tag.strip() in note.tags]

    def filter_by_date(self, date: str) -> list:
        return [note for note in self.notes if note.date == date]

    def save_to_json(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        data = [note.to_dict() for note in self.notes]
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_from_json(self):
        self.notes = []
        if not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                for item in data:
                    tags = [t.strip() for t in item["tags"]]
                    from models.note import TextNote, VoiceNote
                    note_type = item.get("type")
                    
                    if note_type == "TextNote":
                        note = TextNote(item["title"], tags, item["text"], item["date"])
                    elif note_type == "VoiceNote":
                        note = VoiceNote(item["title"], tags, item["duration"], item["date"])
                    else:
                        continue
                    self.notes.append(note)
        except Exception as e:
            print(f"Error loading JSON: {e}")

