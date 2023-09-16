from bs4 import BeautifulSoup
from fastapi import Request


def html2text(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


def get_remote_address(request: Request) -> str:
    return request.headers.get('host')
