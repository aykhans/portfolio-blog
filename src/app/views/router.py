from fastapi import APIRouter
from app.views.routers import (
    main,
    user
)


main_router = APIRouter()
main_router.include_router(main.router, tags=['main'])
main_router.include_router(user.router, tags=['user'])