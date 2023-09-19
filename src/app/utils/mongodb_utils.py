from contextlib import contextmanager
from datetime import datetime
from logging import (
    Handler,
    LogRecord
)

from pymongo.database import Database
from pymongo.collection import Collection

from app.core.config import settings
from app.schemas.logs import MongoDBLog
from app.views.depends import get_mongo_client


async def create_mongodb_database_if_not_exists(
    db_name: str
) -> None:

    with contextmanager(get_mongo_client)() as client:
        if db_name not in client.list_database_names():
            client[db_name].\
                create_collection(settings.MONGO_DB_DEFAULT_COLLECTION)


class MongoDBLogHandler(Handler):
    def emit(self, record: LogRecord) -> None:
        with contextmanager(get_mongo_client)() as client:
            db: Database = client[settings.MONGO_DB_LOGS_NAME]
            collection: Collection = db['init']
            collection.insert_one(
                MongoDBLog(
                    created=datetime.fromtimestamp(record.created),
                    filename=record.filename,
                    levelname=record.levelname,
                    func_name=record.funcName,
                    lineno=record.lineno,
                    msg=record.getMessage(),
                    name=record.name,
                    pathname=record.pathname,
                    args=record.args if record.args else {}
                ).model_dump()
            )