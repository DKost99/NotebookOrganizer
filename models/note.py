from datetime import datetime

class Note:
    """Базовый класс для заметок"""
    def __init__(self, title: str, tags: list, date: str = None):
        self.title = title
        self.tags = tags
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "title": self.title,
            "tags": self.tags,
            "date": self.date
        }

class TextNote(Note):
    """Текстовая заметка с полем text"""
    def __init__(self, title: str, tags: list, text: str, date: str = None):
        super().__init__(title, tags, date)
        self.text = text

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["text"] = self.text
        return data

    def __str__(self) -> str:
        return f"Title: {self.title}\nText: {self.text}\nTags: {', '.join(self.tags)}\nDate: {self.date}"

class VoiceNote(Note):
    """Голосовая заметка с полем duration"""
    def __init__(self, title: str, tags: list, duration: int, date: str = None):
        super().__init__(title, tags, date)
        self.duration = duration

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["duration"] = self.duration
        return data

    def __str__(self) -> str:
        return f"Title: {self.title}\nDuration: {self.duration}s\nTags: {', '.join(self.tags)}\nDate: {self.date}"
