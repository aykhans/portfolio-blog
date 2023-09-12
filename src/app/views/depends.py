import io
from typing import (
    Annotated,
    Generator
)

from PIL import Image
from jose import jwt

from pydantic import ValidationError

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    Cookie,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status
)
from fastapi.security import OAuth2PasswordBearer

from app.models.user import User as UserModel
from app.core import security
from app.core.config import settings
from app.db.session import (
    SessionLocal,
    AsyncSessionLocal
)
from app import crud
from app import schemas
from app.utils.image_operations import (
    generate_unique_image_name,
    save_image
)


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl='/login')


def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


async def get_async_db() -> Generator:
    async with AsyncSessionLocal() as async_db:
        yield async_db


async def get_access_token_from_cookie_or_die(access_token: Annotated[str, Cookie()]) -> str:
    return access_token


async def get_access_token_from_cookie_or_none(access_token: Annotated[str, Cookie()] = None) -> str | None:
    return access_token


async def get_current_user_or_die(
    db: AsyncSession = Depends(get_async_db), token: str = Depends(get_access_token_from_cookie_or_die)
) -> UserModel:

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.JWTTokenPayload(**payload)

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    if  token_data.sub is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = await crud.user.get_by_email(db, email=token_data.sub)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_current_user_or_none(
    db: AsyncSession = Depends(get_async_db), token: str | None = Depends(get_access_token_from_cookie_or_none)
) -> UserModel | None:

    if token is None: return None

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.JWTTokenPayload(**payload)

    except (jwt.JWTError, ValidationError):
        return None

    if  token_data.sub is None:
        return None

    user = await crud.user.get_by_email(db, email=token_data.sub)
    if user is None:
        return None

    return user


async def get_current_active_user_or_die(
    current_user: UserModel = Depends(get_current_user_or_die),
) -> UserModel:

    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_user_or_none(
    current_user: UserModel | None = Depends(get_current_user_or_none),
) -> UserModel | None:

    if current_user is None: return None

    if current_user.is_active is False:
        return None
    return current_user


async def get_current_active_superuser_or_die(
    current_user: UserModel = Depends(get_current_active_user_or_die),
) -> UserModel:

    if current_user.is_superuser is False:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_current_active_superuser_or_none(
    current_user: UserModel | None = Depends(get_current_active_user_or_none),
) -> UserModel | None:

    if current_user is None: return None

    if current_user.is_superuser is False:
        return None
    return current_user


async def handle_image(image: UploadFile = File(...)) -> str:
    try:
        pil_image = Image.open(io.BytesIO(image.file.read()))

        if pil_image.format.lower() not in ['png', 'jpg', 'jpeg']:
            raise ValueError('Invalid image format')

        unique_image_name = await generate_unique_image_name(
            path = settings.MEDIA_PATH / settings.FILE_FOLDERS['post_images'],
            image_name = image.filename,
            image_format = pil_image.format.lower()
        )

        await save_image(
            image = pil_image,
            image_path = settings.MEDIA_PATH /
                settings.FILE_FOLDERS['post_images'] /
                unique_image_name
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid image'
        )

    finally:
        try:
            pil_image.close()

        except: ...
    return str(unique_image_name)