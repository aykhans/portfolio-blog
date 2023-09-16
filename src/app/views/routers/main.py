from typing import Annotated

from fastapi.templating import Jinja2Templates
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)
from fastapi import (
    APIRouter,
    Query,
    Request,
    Depends,
    BackgroundTasks
)

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.schemas import ListPostInTemplate
from app.schemas.main import SendEmail
from app.schemas.post import PostDetail
from app.utils.email_utils import send_email_notification
from app.models.user import User as UserModel
from app.utils.rate_limiter import limiter
from app.views.depends import (
    get_async_db,
    get_current_active_superuser_or_none
)


router = APIRouter()

templates = Jinja2Templates(directory=settings.APP_PATH / 'templates')


@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
                'index.html',
                {"request": request}
            )


@router.post('/send-email')
@limiter.limit('2/day')
async def send_email(
    request: Request,
    background_tasks: BackgroundTasks,
    form_data: SendEmail = Depends()
):

    body = f"name: {form_data.name}\n"\
            f"email: {form_data.email}\n"\
            f"phone: {form_data.phone}\n"\
            f"message: {form_data.message}"

    email_notification = send_email_notification(
            subject=f"Portfolio Blog (by {form_data.email})",
            body=body
        )

    if email_notification is not None:
        background_tasks.add_task(
            email_notification
        )

    return RedirectResponse(
        str(request.url_for('home')) + '#contact',
        status_code=303
    )


@router.get('/blog', response_class=HTMLResponse)
async def blog(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    user: UserModel | None = Depends(get_current_active_superuser_or_none),
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
                    'skip': skip,
                    'user': user
                }
            )


@router.get('/blog/{slug}', response_class=HTMLResponse)
async def blog_post(
    request: Request,
    slug: str,
    db: AsyncSession = Depends(get_async_db)
):

    post = await crud.post.get_by_slug(db, slug=slug)

    if post is None:
        return RedirectResponse(
            str(request.url_for('blog')),
            status_code=303
        )

    return templates.TemplateResponse(
                'post.html',
                {
                    'request': request,
                    'post': PostDetail.model_validate(post)
                }
            )
