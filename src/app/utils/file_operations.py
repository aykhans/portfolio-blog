from pathlib import Path
from os import remove


async def mkdir_if_not_exists(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True)


def remove_file(file_path: str) -> None:
    try: remove(file_path)
    except FileNotFoundError: ...