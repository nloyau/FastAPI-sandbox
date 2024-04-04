"""Services module."""

from uuid import uuid4
from typing import Iterator

from .repositories import NoteRepository
from .models import Note

class NoteService:

    def __init__(self, Note_repository: NoteRepository) -> None:
        self._repository: NoteRepository = Note_repository

    def get_Notes(self) -> Iterator[Note]:
        return self._repository.get_all()

    def get_Note_by_id(self, Note_id: int) -> Note:
        return self._repository.get_by_id(Note_id)

    def create_Note(self) -> Note:
        uid = uuid4()
        return self._repository.add(text=f"{uid}@email.com", completed=False)

    def delete_Note_by_id(self, Note_id: int) -> None:
        return self._repository.delete_by_id(Note_id)