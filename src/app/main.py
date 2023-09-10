import io
from fastapi import Body, Depends, FastAPI, HTTPException, Request, Form, UploadFile, File, status
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import BaseModel, ValidationError, field_validator
from app import crud
from app.core import security
from app.core.config import settings
from app.schemas import JWTToken
from app.schemas.login import LoginForm

from app.schemas.post import Post, PostCreate, PostUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import User, UserCreate
from fastapi.responses import HTMLResponse
from app.views.depends import get_async_db, handle_image

from typing import Annotated, Any
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from PIL import Image
import aiofiles
from pathlib import Path
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.views.router import main_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title=settings.PROJECT_NAME
)

# app.mount(
#     '/static',
#     StaticFiles(directory=settings.APP_PATH / 'static'),
#     name='static'
# )

app.include_router(main_router)

# templates = Jinja2Templates(directory=main_path / 'templates')



# @app.get("/", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("test.html", {"request": request})

# from pydantic import BaseModel


# class User(BaseModel):
#     username: str
#     password: str

# @app.post("/", response_class=HTMLResponse)
# async def read_item(request: Request, user: User):
#     print(user)
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/t", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return await request_validation_exception_handler(request, exc)


# @app.post("/login", response_model=JWTToken)
# async def login(
#     db: AsyncSession = Depends(get_async_db),
#     form_data: LoginForm = Depends()
# ) -> Any:

#     user = await crud.user.authenticate(
#         db, email=form_data.email, password=form_data.password
#     )

#     if user is None:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")

#     elif user.is_active is False:
#         raise HTTPException(status_code=400, detail="Inactive user")

#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

#     return {
#         "access_token": security.create_access_token(
#             user.email,
#             expires_delta=access_token_expires
#         ),
#         "token_type": "bearer",
#     }


# @app.get('/alma')
# async def test(
#     *,
#     request: Request,
#     db: AsyncSession = Depends(get_async_db),
#     # title: str = Form(...),
#     # text: str = Form(...),
#     # image: str = Depends(handle_image),
# ):

#     # post = PostCreate(title=title, text=text, image_path=image)
#     # post = await crud.post.create_with_owner(db, obj_in=post, owner_id=1)

#     # async with aiofiles.open(settings.MEDIA_PATH / settings.FILE_FOLDERS['post_images'] / image.filename, 'wb') as out_file:
#     #     content = await image.read()
#     #     await out_file.write(content)

#     # post = await crud.post.remove(db, id=34)
#     # post = await crud.post.get_by_id(db, id=33)

#     # if post is None:
#     #     raise HTTPException(status_code=404, detail="Post not found")

#     # post = await crud.post.update(db, db_obj=post, obj_in={'text': text})

#     # posts = await crud.post.get_multi(db)

#     # posts = await crud.post.get_multi_by_owner(db, owner_id=1)

    # user = await crud.user.get_by_email(db, email='aykhan.shahs0@gmail.com')
#     print(type(user))
#     # if user is not None:
#     #     raise HTTPException(status_code=400, detail="Email already registered")

#     # user = await crud.user.create(db, obj_in=UserCreate(email='aykhan.shahs0@gmail.com', password='alma'))

#     # user = await crud.user.update(db, db_obj=user, obj_in={'password': 'alma'})

#     # user = await crud.user.authenticate(db, email='aykhan.shahs1@gmail.com', password='alma')

#     # if user is None:
#     #     raise HTTPException(status_code=400, detail="Incorrect email or password")

#     # user = await crud.user.remove(db, id=2)

    # return user