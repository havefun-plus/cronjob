import traceback
from html.parser import HTMLParser
from typing import AnyStr


def ensure_str(raw: AnyStr) -> str:
    if not raw:
        return ''
    if isinstance(raw, str):
        return raw.strip()
    return raw.decode('utf8').strip()


def ensure_html(raw: AnyStr) -> str:
    parser = HTMLParser()
    return parser.unescape(ensure_str(raw))


def global_exception_handler(exc_type, exc_value, exc_traceback):
    traceback.print_exception(exc_type, exc_value, exc_traceback)
