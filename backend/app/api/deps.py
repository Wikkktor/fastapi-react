import os
from typing import Generator, Union
from core.auth import oauth2_bearer
from db.session import SessionLocal
from dotenv import load_dotenv
from fastapi import Depends, Response
from jose import jwt, JWTError
from models.user import User
from sqlalchemy.orm import Session

from core.exceptions import get_user_exception

load_dotenv()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    response: Response, token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)
) -> Union[User, Exception]:
    try:
        payload = jwt.decode(token, os.getenv("TOKEN"), algorithms=[os.getenv("ALGORYTM")])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise get_user_exception()
    except JWTError:
        raise get_user_exception()

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise get_user_exception()
    return user
