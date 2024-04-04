"""Repositories module."""

from contextlib import AbstractContextManager
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from .models import Note


class NoteRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Note]:
        with self.session_factory() as session:
            return session.query(Note).all()

    def get_by_id(self, Note_id: int) -> Note:
        with self.session_factory() as session:
            Note = session.query(Note).filter(Note.id == Note_id).first()
            if not Note:
                raise NoteNotFoundError(Note_id)
            return Note

    def add(self, text: str, completed: bool = False) -> Note:
        with self.session_factory() as session:
            Note = Note(text , completed)
            session.add(Note)
            session.commit()
            session.refresh(Note)
            return Note

    def delete_by_id(self, Note_id: int) -> None:
        with self.session_factory() as session:
            entity: Note = session.query(Note).filter(Note.id == Note_id).first()
            if not entity:
                raise NoteNotFoundError(Note_id)
            session.delete(entity)
            session.commit()


class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class NoteNotFoundError(NotFoundError):

    entity_name: str = "Note"
