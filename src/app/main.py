from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import FileResponse

from pydantic import ValidationError

from app.core.config import settings
from app.views.router import main_router


app = FastAPI(
    title=settings.PROJECT_NAME
)

# app.mount(
#     '/static',
#     StaticFiles(directory=settings.MAIN_PATH / 'static'),
#     name='static'
# )

app.include_router(main_router)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return await request_validation_exception_handler(request, exc)


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return FileResponse(settings.STATIC_FOLDER / '404.jpg')
