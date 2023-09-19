from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import FileResponse

from pydantic import ValidationError

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.views.router import main_router
from app.utils.rate_limiter import limiter
from app.utils.mongodb_utils import create_mongodb_database_if_not_exists


app = FastAPI(
    title=settings.PROJECT_NAME
)

app.state.limiter = limiter

# app.mount(
#     '/static',
#     StaticFiles(directory=settings.MAIN_PATH / 'static'),
#     name='static'
# )

# --------------------------------- Routers ---------------------------------

app.include_router(main_router)

# ------------------------------- Routers end -------------------------------


# ---------------------------------- Events ----------------------------------

@app.on_event('startup')
async def app_startup():
    await create_mongodb_database_if_not_exists(settings.MONGO_DB_LOGS_NAME)

# -------------------------------- Events end --------------------------------


# ---------------------------- Exception handlers ----------------------------

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return await request_validation_exception_handler(request, exc)


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return FileResponse(settings.STATIC_FOLDER / '404.jpg')

# -------------------------- Exception handlers end --------------------------