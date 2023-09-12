from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.templating import Jinja2Templates
from fastapi.responses import (
    FileResponse,
    HTMLResponse
)
from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Depends
)

from app import crud
from app.core import security
from app.models.user import User as UserModel
from app.schemas import JWTToken, LoginForm
from app.core.config import settings
from app.views.depends import (
    get_async_db,
    get_current_active_superuser
)


router = APIRouter()

templates = Jinja2Templates(directory=settings.APP_PATH / 'templates')


@router.get(f"/{settings.SECRET_KEY[-10:]}", response_class=HTMLResponse)
async def login(
    request: Request
):

    return templates.TemplateResponse(
                'admin/login.html',
                {
                    'request': request,
                    'login_url': f'/{settings.SECRET_KEY[-10:]}'
                }
            )


@router.post(f"/{settings.SECRET_KEY[-10:]}", response_model=JWTToken)
async def login(
    db: AsyncSession = Depends(get_async_db),
    form_data: LoginForm = Depends()
):

    user = await crud.user.authenticate(
        db, email=form_data.email, password=form_data.password
    )

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    elif user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": security.create_access_token(
            user.email,
            expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.get("/admin")
def admin(
    request: Request
):

    return FileResponse(settings.STATIC_FOLDER / 'just_a.gif')