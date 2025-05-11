from typing import Any, Optional

from sqlalchemy.orm import Session

from core.exceptions import object_does_not_exist
from crud.base import CRUDBase
from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.auth import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get a user by their email address."""
        if result := db.query(User).filter(User.email == email).first():
            return result
        raise object_does_not_exist()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create a new user."""
        create_data: dict[str, Any] = obj_in.model_dump()
        create_data.pop("password")
        db_obj: User = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()

        return db_obj


crud_user = CRUDUser(User)
