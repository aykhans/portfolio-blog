from typing import Annotated

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import (
    APIRouter,
    Query,
    Request,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.schemas import ListPostInTemplate
from app.views.depends import get_async_db


router = APIRouter()

templates = Jinja2Templates(directory=settings.APP_PATH / 'templates')


@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
                'index.html',
                {"request": request}
            )


@router.get('/blog', response_class=HTMLResponse)
async def blog(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    skip: Annotated[int, Query(gt=-1)] = 0,
    new: bool = False
):

    if new:
        skip -= 10
        if skip < 0:
            skip = 0

    posts = await crud.post.get_multi(db, skip=skip, limit=6)
    posts = ListPostInTemplate.validate_python(posts)

    if len(posts) == 6:
        skip += 5
        posts = posts[:-1]

    return templates.TemplateResponse(
                'blog.html',
                {
                    'request': request,
                    'posts': posts,
                    'skip': skip
                }
            )