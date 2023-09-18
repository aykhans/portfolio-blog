from contextlib import contextmanager

from app.views.depends import get_mongo_client


async def create_mongodb_database_if_not_exists(
    db_name: str
) -> None:

    with contextmanager(get_mongo_client)() as client:
        if db_name not in client.list_database_names():
            client[db_name].create_collection('init')