from bs4 import BeautifulSoup


def html2text(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()