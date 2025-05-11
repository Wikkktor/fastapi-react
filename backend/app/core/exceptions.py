from fastapi import HTTPException
from fastapi import status


def user_username_exists() -> HTTPException:
    username_exception: HTTPException = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The given username already exists",
    )
    return username_exception


def user_must_be_admin() -> HTTPException:
    authority_exception: HTTPException = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Authority failed",
    )
    return authority_exception


def get_user_exception() -> HTTPException:
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect password or email",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def object_does_not_exist() -> HTTPException:
    object_exception: HTTPException = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Object does not exists",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return object_exception


def custom_exception(detail: str = "Something went wrong.") -> HTTPException:
    authority_exception: HTTPException = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
    )
    return authority_exception


def no_permission() -> HTTPException:
    permission_exception: HTTPException = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="No permission"
    )

    return permission_exception
