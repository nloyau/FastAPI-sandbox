"""Containers module."""

from dependency_injector import containers, providers
from app.repositories import NoteRepository
from app.services import NoteService
from .database import Database

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["app.router"])
    config = providers.Configuration(yaml_files=["config.yml"])
    db = providers.Singleton(Database, db_url=config.db.url)

    Note_repository = providers.Factory(
        NoteRepository,
        session_factory=db.provided.session,
    )

    Note_service = providers.Factory(
        NoteService,
        Note_repository=Note_repository,
    )

