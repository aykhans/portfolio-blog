from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PastDatetime,
    computed_field,
    TypeAdapter
)

from app.core.config import settings


class PostBase(BaseModel):
    title: Optional[str] = Field(max_length=100)
    text: Optional[str] = None
    image_path: Optional[str] = None


class PostCreate(PostBase):
    title: str = Field(max_length=100)
    text: str
    image_path: str


class PostUpdate(PostBase): ...


class PostInTemplate(PostBase):
    title: str
    text: str
    created_at: PastDatetime

    class Config:
        from_attributes = True


ListPostInTemplate = TypeAdapter(list[PostInTemplate])


class PostInDBBase(PostBase):
    slug: str
    title: str
    text: str
    image_path: Optional[str] = None
    owner_id: int

    class Config:
        from_attributes = True


class Post(PostInDBBase):
    @computed_field
    @property
    def image_url(self) -> str | None:
        if self.image_path is None:
            return None

        return str(
            settings.MEDIA_FOLDER /
            settings.FILE_FOLDERS['post_images'] /
            self.image_path
        )