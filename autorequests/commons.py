from __future__ import annotations

import json
import urllib.parse


def indent(data: str, spaces: int = 4) -> str:
    """
    indents a code block a set amount of spaces
    note: is ~1.5x faster than textwrap.indent(data, " " * spaces)
    (from my testing)
    """
    indent_block = " " * spaces
    return "\n".join((indent_block + line if line else line) for line in data.splitlines())


def extract_cookies(headers: dict[str, str]) -> dict[str, str]:
    """:returns: a dict of cookies based off the 'cookie' header"""
    cookie_header = headers.pop("cookie", None)
    if not cookie_header:
        return {}
    cookie_dict = {}
    for cookie in cookie_header.split("; "):
        key, value = cookie.split("=", maxsplit=1)
        cookie_dict[key] = value
    return cookie_dict


def format_dict(data: dict, indent: int | None = 4) -> str:
    """format a dictionary"""
    # I'm not sure it's possible to pretty-format this with something like
    # pprint, but if it is possible LMK!
    formatted = json.dumps(data, indent=indent)
    # parse bools and none
    # leading space allows us to only match literal false and not "false" string
    formatted = formatted.replace(" null", " None")
    formatted = formatted.replace(" true", " True")
    formatted = formatted.replace(" false", " False")
    return formatted


def parse_url_encoded(x: str) -> dict[str, str]:
    """parses application/x-www-form-urlencoded and query string params"""
    return dict(urllib.parse.parse_qsl(x, keep_blank_values=True))
