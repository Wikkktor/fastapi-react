from core.auth import create_access_token, authenticate
from crud.crud_user import crud_user
from api.deps import get_db, get_current_user
from core.exceptions import get_user_exception
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from models.user import User
from schemas.auth import Token
from schemas.user import UserInDB, UserCreate

router = APIRouter()


@router.post("/login/", status_code=status.HTTP_200_OK, response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Getting the JWT for a user with data from oauth2 request body
    :param db: Database connection required
    :param form_data: request body data
    :return: Access Token JWT
    """
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise get_user_exception()

    return Token(access_token=create_access_token(sub=user.id), token_type="bearer")


@router.get("/me/", response_model=UserInDB, status_code=status.HTTP_200_OK)
def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    """
    Fetch the current logged in user.
    """

    return current_user


@router.post("/signup/", status_code=201, response_model=UserInDB)
def create_user_signup(user_in: UserCreate, db: Session = Depends(get_db)) -> UserInDB:
    """
    Create new user without the need to be logged in.
    """

    return crud_user.create(db=db, obj_in=user_in)
