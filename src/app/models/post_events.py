from contextlib import contextmanager
from slugify import slugify

from sqlalchemy.orm.base import NO_VALUE
from sqlalchemy.event import (
    listen,
    listens_for
)

from app.views.depends import get_db
from app.utils.file_operations import remove_file
from app.core.config import settings
from .post import Post


def generate_slug(target, value, oldvalue, initiator):
    slug = slugify(value)

    with contextmanager(get_db)() as db:
        number = 1
        temp_slug = slug

        while db.query(Post).filter(
            Post.slug == temp_slug
        ).first() is not None:
            temp_slug = f'{slug}-{number}'
            number += 1

        target.slug = temp_slug


listen(Post.title, 'set', generate_slug)


def remove_old_image_on_update(target, value, oldvalue, initiator):
    if oldvalue is not NO_VALUE:
        remove_file(
            settings.MEDIA_PATH /
            settings.FILE_FOLDERS['post_images'] /
            oldvalue
        )


listen(Post.image_path, 'set', remove_old_image_on_update)


@listens_for(Post, 'before_delete')
def before_delete_listener(mapper, connection, target):
    if target.image_path:
        remove_file(
            settings.MEDIA_PATH /
            settings.FILE_FOLDERS['post_images'] /
            target.image_path
        )
