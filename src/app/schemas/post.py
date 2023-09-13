from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PastDatetime,
    TypeAdapter,
    field_validator
)

from app.utils.custom_functions import html2text

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


class PostInTemplate(BaseModel):
    title: str
    text: str
    created_at: PastDatetime
    slug: str

    class Config:
        from_attributes = True

    @field_validator('text', mode='after')
    @classmethod
    def html_to_text(cls, v: str) -> str:
        return html2text(v)[:60]


ListPostInTemplate = TypeAdapter(list[PostInTemplate])


class PostDetail(BaseModel):
    title: str
    text: str
    created_at: PastDatetime
    image_path: str

    class Config:
        from_attributes = True

    @field_validator('image_path', mode='after')
    @classmethod
    def absolute_image_path(cls, v: str) -> str | None:
        return str(
            settings.MEDIA_FOLDER /
            settings.FILE_FOLDERS['post_images'] /
            v
        )


class PostInDBBase(PostBase):
    slug: str
    title: str
    text: str
    image_path: str
    owner_id: int

    class Config:
        from_attributes = True


class Post(PostInDBBase):
    @field_validator('image_path', mode='after')
    @classmethod
    def absolute_image_path(cls, v: str) -> str | None:
        return str(
            settings.MEDIA_FOLDER /
            settings.FILE_FOLDERS['post_images'] /
            v
        )