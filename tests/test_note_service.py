import sys
import os

import unittest
import os
import json
from services.note_service import NoteService
from models.note import TextNote, VoiceNote

class TestNoteService(unittest.TestCase):
    def setUp(self):
        """Вызывается перед каждым тестом: создаем чистый сервис"""
        self.service = NoteService()
        # Подменяем путь, чтобы не испортить реальные данные
        self.service.filepath = "data/test_notes.json"
        self.service.notes = []
        self.service.undo_stack = []

    def tearDown(self):
        """Вызывается после каждого теста: удаляем тестовый JSON"""
        if os.path.exists("data/test_notes.json"):
            os.remove("data/test_notes.json")

    def test_add_note_positive(self):
        """Позитивный случай: успешное добавление заметки"""
        note = TextNote("Test Title", ["test"], "Some text", "2026-01-01")
        self.service.add_note(note)
        self.assertEqual(len(self.service.get_notes()), 1)
        self.assertEqual(self.service.get_notes()[0].title, "Test Title")

    def test_delete_note_negative_out_of_bounds(self):
        """Негативный случай: удаление несуществующего индекса"""
        note = TextNote("Title", ["tag"], "text")
        self.service.add_note(note)
        result = self.service.delete_note(99)  # Индекса 99 нет
        self.assertIsNone(result)
        self.assertEqual(len(self.service.get_notes()), 1)

    def test_undo_stack_boundary_empty(self):
        """Граничный случай: попытка отмены (Undo), когда стек пуст"""
        result = self.service.undo()
        self.assertFalse(result)  # Должно вернуться False, программа не должна падать

    def test_undo_action_success(self):
        """Позитивный случай: проверка восстановления данных через Undo"""
        note = TextNote("Title", ["tag"], "text")
        self.service.add_note(note)
        self.service.delete_note(0)  # Сначала добавили, потом удалили
        self.assertEqual(len(self.service.get_notes()), 0)
        
        self.service.undo()  # Отменяем удаление
        self.assertEqual(len(self.service.get_notes()), 1)
        self.assertEqual(self.service.get_notes()[0].title, "Title")

if __name__ == "__main__":
    unittest.main()
