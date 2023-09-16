from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union
)

from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete(CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        q = select(self.model).where(self.model.id == id)
        obj = await db.execute(q)
        return obj.scalar_one_or_none()

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:

        q = (
            select(self.model).
            offset(skip).
            limit(limit).
            order_by(self.model.id.desc())
        )
        obj = await db.execute(q)
        return obj.scalars()

    def sync_get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:

        q = (
            select(self.model).
            offset(skip).
            limit(limit).
            order_by(self.model.id.desc())
        )
        obj = db.execute(q)
        return obj.scalars()

    async def create(
        self, db: Session, *, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:

        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in

        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def remove(self, db: Session, *, id: int) -> ModelType:
        q = select(self.model).where(self.model.id == id)
        obj = await db.execute(q)
        obj = obj.scalar_one()
        await db.delete(obj)
        await db.commit()

        return obj
