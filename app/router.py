from typing import Annotated
from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import inject, Provide
from app.container import Container
from app.models import Note, User
from app.services import NoteService
from app.utils import get_current_active_user


router = APIRouter(prefix="/api/v1")

@router.get("/test")
def test():
    return {"status": "OK"}

@router.get("/notes")
@inject
async def get_list(
        note_service: NoteService = Depends(Provide[Container.Note_service]),
        current_user: User= Depends(get_current_active_user)
):
    return note_service.get_Notes()

@router.post("/note")
@inject
async def post_note(
        note_service: NoteService = Depends(Provide[Container.Note_service]),
        current_user: User= Depends(get_current_active_user)
):
    return note_service.create_Note()



@router.get("/users/me/items/",response_model=None)
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return {"item_id": "Foo", "owner": current_user.username}