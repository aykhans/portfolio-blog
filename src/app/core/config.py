from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import (
    EmailStr,
    PostgresDsn,
    MongoDsn
)


class Settings(BaseSettings):
    PROJECT_NAME: str = 'FastAPI Portfolio & Blog'

    # -------------------------------- Paths --------------------------------

    # path to src folder
    MAIN_PATH: Path = Path(__file__).resolve().parent.parent.parent
    # path to app folder
    APP_PATH: Path = MAIN_PATH / 'app'
    # name of media folder
    MEDIA_FOLDER: Path = Path('media')
    # path to media folder
    MEDIA_PATH: Path = MAIN_PATH / MEDIA_FOLDER
    # name of static folder
    STATIC_FOLDER_NAME: Path = Path('static')
    # path to static folder
    STATIC_FOLDER: Path = MAIN_PATH / STATIC_FOLDER_NAME

    FILE_FOLDERS: dict[str, Path] = {
        'post_images': Path('post_images'),
    }

    # ------------------------------ Paths End ------------------------------


    # --------------------------------- App ---------------------------------

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days

    @property
    def LOGIN_URL(self) -> str:
        return self.SECRET_KEY[-10:]

    # ------------------------------- App End -------------------------------


    # ------------------------------ PostgreSQL ------------------------------

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    def get_postgres_dsn(self, _async: bool = False) -> PostgresDsn:
        scheme = 'postgresql+asyncpg' if _async else 'postgresql'

        return PostgresDsn.build(
            scheme=scheme,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        )

    # ---------------------------- PostgreSQL End ----------------------------


    # ------------------------------- MongoDB -------------------------------

    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_DB_PORT: int = 27017
    MONGO_DB_LOGS_NAME: str = 'logs'
    MONGO_DB_DEFAULT_COLLECTION: str = 'init'

    @property
    def MONGO_DB_DSN(self) -> MongoDsn:
        return MongoDsn.build(
            scheme='mongodb',
            username=self.MONGO_INITDB_ROOT_USERNAME,
            password=self.MONGO_INITDB_ROOT_PASSWORD,
            host='mongodb',
            port=self.MONGO_DB_PORT,
        )

    # ----------------------------- MongoDB End -----------------------------


    # -------------------------------- Email ---------------------------------

    SMTP_SSL_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_USER: EmailStr
    SMTP_PASSWORD: str

    EMAILS_FROM_NAME: str = PROJECT_NAME
    EMAIL_RECIPIENTS: list[EmailStr] = []

    # ------------------------------ Email End -------------------------------

settings = Settings()
