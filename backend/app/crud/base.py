from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Column, UnaryExpression, desc
from sqlalchemy.orm import Session, Query

from core.exceptions import object_does_not_exist
from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def apply_ordering(
        self,
        query: Query[Any],
        model: Type[ModelType],
        order_by: str,
        default: Column[str] | UnaryExpression = None,
    ) -> Query[Type[ModelType]]:
        """Apply ordering to the query based on the order_by parameter."""
        if order_by:
            descending: bool = order_by.startswith(
                "-"
            )  # Check if order_by starts with "-"
            column_name: str = order_by.lstrip(
                "-"
            )  # Remove the "-" to get the column name
            if column := getattr(model, column_name, None):
                return query.order_by(desc(column) if descending else column)
            elif default is not None:
                return query.order_by(default)

        return query

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a single object by its ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_or_404(self, db: Session, id: Any) -> ModelType:
        """Get a single object by its ID or raise a 404 error."""
        if result := self.get(db=db, id=id):
            return result
        raise object_does_not_exist()

    def get_multi(
        self, db: Session, *, offset: int = 0, limit: int = 5000
    ) -> List[ModelType]:
        """Get multiple objects with offset and limit."""
        return (
            db.query(self.model)
            .order_by(self.model.id)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new object."""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj: ModelType = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """Update an object."""
        obj_data: Any = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data: dict[str, Any] = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """Remove an object by its ID."""
        db_obj: ModelType = self.get_or_404(db=db, id=id)
        db.delete(db_obj)
        db.commit()
        return db_obj
