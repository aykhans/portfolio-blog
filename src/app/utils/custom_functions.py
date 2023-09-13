import re


def html2text(html: str) -> str:
    return re.sub(
            re.compile('<.*?>'),
            '',
            html
        )