from sqlalchemy import Column, String, Boolean, Integer
from pydantic import BaseModel
from .database import Base


#  Note model
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    completed = Column(Boolean, default=False)


#class NoteIn(BaseModel):
#    text: str
#    completed: bool


#class Note(BaseModel):
#    id: int
#    text: str
#    completed: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
