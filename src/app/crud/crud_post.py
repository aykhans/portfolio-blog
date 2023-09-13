from typing import (
    List,
    Optional
)

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.post import Post
from app.schemas.post import (
    PostCreate,
    PostUpdate
)


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    async def create_with_owner(
        self,
        db: Session,
        *,
        obj_in: PostCreate,
        owner_id: int
    ) -> Post:

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def get_by_slug(
        self,
        db: Session,
        slug: str
    ) -> Optional[Post]:

        q = select(self.model).where(self.model.slug == slug)
        obj = await db.execute(q)
        return obj.scalar_one_or_none()

    async def get_multi_by_owner(
        self,
        db: Session,
        *,
        owner_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Post]:

        q = (
            select(self.model)
            .where(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )

        objs = await db.execute(q)

        return objs.scalars()

    def create(self):
        raise DeprecationWarning("Use create_with_owner instead")

post = CRUDPost(Post)