from datetime import timedelta
from typing import Annotated
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from app.params import ACCESS_TOKEN_EXPIRE_MINUTES,fake_users_db
from app.router import router
from app.container import Container
from app.instrumentor import instrumentator
from app.models import Token
from app.utils import authenticate_user, create_access_token

from pprint import pprint


container = Container()
db = container.db()
db.create_database()

app = FastAPI()
app.container = container

# Router
app.include_router(router)

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supervision
instrumentator.instrument(app)
instrumentator.expose(app)



@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# Main
if __name__ == "__main__":
    #uvicorn.run("main:app", host="0.0.0.0", port=8080, ssl=ssl_context)
    uvicorn.run("main:app", host="0.0.0.0", port=8080, ssl_keyfile="ssl/key.pem",
               ssl_certfile="ssl/cert.pem")

