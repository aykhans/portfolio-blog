from pathlib import Path
from PIL import Image

from app.utils.file_operations import mkdir_if_not_exists


async def generate_unique_image_name(
    path: Path,
    image_name: Path | str,
    image_format: str
) -> Path | str:

    number = 1
    temp_image_name = image_name

    while (path / temp_image_name).exists():
        temp_image_name = f'{image_name}-{number}.{image_format}'
        number += 1

    return temp_image_name


async def save_image(image: Image, image_path: Path) -> None:
    await mkdir_if_not_exists(image_path.parent)
    image.save(image_path)
