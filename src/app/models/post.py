from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String
)

from app.db.base_class import Base


class Post(Base):
    id = Column(Integer(), primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    slug = Column(String(), index=True, nullable=False, unique=True)
    text = Column(String(), index=True, nullable=False)
    image_path = Column(String(100), index=True, unique=True, nullable=False)
    owner_id = Column(Integer(), ForeignKey("user.id"))

    owner = relationship("User", back_populates="posts")
