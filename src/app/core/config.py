from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    PROJECT_NAME: str = 'FastAPI Portfolio & Blog'

    MAIN_PATH: Path = Path(__file__).resolve().parent.parent.parent # path to src folder
    APP_PATH: Path = MAIN_PATH / 'app' # path to app folder
    MEDIA_FOLDER: Path = Path('media') # name of media folder
    MEDIA_PATH: Path = MAIN_PATH / MEDIA_FOLDER # path to media folder

    FILE_FOLDERS: dict[str, Path] = {
        'post_images': Path('post_images'),
    }

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200 # 30 days

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    def get_postgres_dsn(self, _async: bool=False) -> PostgresDsn:
        scheme = 'postgresql+asyncpg' if _async else 'postgresql'

        return PostgresDsn.build(
            scheme=scheme,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        )


settings = Settings()