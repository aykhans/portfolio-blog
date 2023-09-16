from datetime import timedelta
from typing import (
    Annotated,
    Optional
)

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.templating import Jinja2Templates
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    RedirectResponse
)
from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
    Depends
)

from app import crud
from app.core import security
from app.models.user import User as UserModel
from app.schemas import (
    JWTToken,
    LoginForm
)
from app.core.config import settings
from app.schemas.post import (
    PostCreate,
    PostUpdate
)
from app.schemas.post import Post as PostSchema
from app.views.depends import (
    get_async_db,
    get_current_active_superuser_or_die,
    get_current_active_superuser_or_none,
    get_post_by_slug_or_die,
    handle_post_image_or_die,
    handle_post_image_or_none
)


router = APIRouter()

templates = Jinja2Templates(directory=settings.APP_PATH / 'templates')


@router.get(
    f"/{settings.LOGIN_URL}",
    response_class=HTMLResponse,
    include_in_schema=False
)
async def get_login(
    request: Request
):

    return templates.TemplateResponse(
                'admin/login.html',
                {
                    'request': request,
                    'login_url': f'/{settings.LOGIN_URL}'
                }
            )


@router.post(
    f"/{settings.LOGIN_URL}",
    response_model=JWTToken,
    include_in_schema=False
)
async def login(
    db: AsyncSession = Depends(get_async_db),
    form_data: LoginForm = Depends()
):

    user = await crud.user.authenticate(
        db, email=form_data.email, password=form_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    elif user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return {
        "access_token": security.create_access_token(
            user.email,
            expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.get(
    '/add-post',
    response_class=HTMLResponse,
)
async def get_create_post(
    request: Request,
    user: UserModel = Depends(get_current_active_superuser_or_die)
):

    return templates.TemplateResponse(
                'admin/add-post.html',
                {
                    'request': request
                }
            )


@router.post('/add-post')
async def create_post(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    user: UserModel = Depends(get_current_active_superuser_or_die),
    title: str = Form(...),
    text: str = Form(...),
    image: str = Depends(handle_post_image_or_die)
):

    obj_in = PostCreate(
        title=title,
        text=text,
        image_path=image
    )

    post = await crud.post.create_with_owner(
        db, obj_in=obj_in, owner_id=user.id
    )

    return RedirectResponse(
        str(request.url_for('get_update_post', slug=post.slug)),
        status_code=303
    )


@router.get('/update-post/{slug}')
async def get_update_post(
    request: Request,
    user: UserModel = Depends(get_current_active_superuser_or_none),
    post: str = Depends(get_post_by_slug_or_die)
):

    if user is None:
        return RedirectResponse(
            f'/{settings.LOGIN_URL}',
            status_code=303
        )

    if user.id != post.owner_id:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse(
                'admin/update-post.html',
                {
                    'request': request,
                    'post': PostSchema.model_validate(post)
                }
            )


@router.post('/update-post/{slug}')
async def update_post(
    request: Request,
    user: UserModel = Depends(get_current_active_superuser_or_none),
    post: str = Depends(get_post_by_slug_or_die),
    db: AsyncSession = Depends(get_async_db),
    title: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
    image: Annotated[str, Depends(handle_post_image_or_none)] = None
):

    if user is None:
        return RedirectResponse(
                f'/{settings.LOGIN_URL}',
                status_code=303
            )

    if user.id != post.owner_id:
        raise HTTPException(status_code=404, detail="Post not found")

    obj_in = PostUpdate(
        title=title,
        text=text,
        image_path=image
    ).model_dump(exclude_none=True)

    updated_post = await crud.post.update(
        db=db,
        db_obj=post,
        obj_in=obj_in
    )

    return templates.TemplateResponse(
                'admin/update-post.html',
                {
                    'request': request,
                    'post': PostSchema.model_validate(updated_post)
                }
            )


@router.get('/delete-post/{slug}')
async def get_delete_post(
    request: Request,
    user: UserModel = Depends(get_current_active_superuser_or_die),
    post: str = Depends(get_post_by_slug_or_die)
):

    if user.id != post.owner_id:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse(
                'admin/delete-post.html',
                {
                    'request': request,
                    'post': PostSchema.model_validate(post)
                }
            )


@router.post('/delete-post/{slug}')
async def delete_post(
    request: Request,
    user: UserModel = Depends(get_current_active_superuser_or_die),
    post: str = Depends(get_post_by_slug_or_die),
    db: AsyncSession = Depends(get_async_db)
):

    if user.id != post.owner_id:
        raise HTTPException(status_code=404, detail="Post not found")

    await crud.post.remove_by_slug(db, slug=post.slug)

    return RedirectResponse(
        str(request.url_for('blog')),
        status_code=303
    )


@router.get("/admin")
def admin(
    request: Request
):

    return FileResponse(settings.STATIC_FOLDER / 'just_a.gif')
