"""Functions convert Markdown texts into valid HTML.
"""

import re
from typing import Union


STR_BOLD = '(.*)__(.*)__(.*)'
STR_ITALIC = '(.*)_(.*)_(.*)'
STR_LIST = r'\* (.*)'


def get_bold_text(text: str) -> Union[re.Match, None]:
    """Identify if text has a valid character to be
    recognized as Markdown code for bold '__emphasized__'.
    """
    return re.match(STR_BOLD, text)

def get_italic_text(text: str) -> Union[re.Match, None]:
    """Identify if text has a valid character to be
    recognized as Markdown code for talicize ' _italicized_'.
    """
    return re.match(STR_ITALIC, text)

def get_list_text(text: str) -> Union[re.Match, None]:
    """Identify if text has a valid character to be
    recognized as Markdown code for unordered lists '*'.
    """
    return re.match(STR_LIST, text)

def parsing_headers_level(text: str) -> str:
    """Identify if text has a structurally valid Markdown
    to recognizes up to 6 hash (#).

    Function that takes any text and converts it to a section
    header HTML elements if it identifies that text has a
    structurally valid Markdown to recognize up to 6 hash
    characters (#) for 6 levels. Otherwise returns text
    without changes.
    """
    headers = {}
    for i in range(1,7):
        headers['#'*i + ' (.*)'] = f'<h{i}>{text[i+1:]}</h{i}>'

    for key in headers:
        if re.match(key, text) is not None:
            return headers[key]

    return text

def parsing_italic(match: re.Match) -> str:
    """
    """
    return f'{match.group(1)}<em>{match.group(2)}</em>{match.group(3)}'

def parsing_bold(match: re.Match) -> str:
    """
    """
    return f'{match.group(1)}<strong>{match.group(2)}</strong>{match.group(3)}'

def parsing_bold_italic(text: str) -> str:
    """
    """
    bold_text = get_bold_text(text)
    if bold_text:
        text = parsing_bold(bold_text)

    italic_text = get_italic_text(text)
    if italic_text:
        text = parsing_italic(italic_text)
    return text

def parse(markdown: str) -> str:
    """Main function
    """
    res = ''
    in_list = False
    in_list_append = False
    for i in markdown.split('\n'):
        i = parsing_headers_level(i)

        match = get_list_text(i)
        if match:
            text = parsing_bold_italic(match.group(1))
            if not in_list:
                in_list = True
                i = '<ul><li>' + text + '</li>'
            else:
                i = '<li>' + text + '</li>'
        else:
            if in_list:
                in_list_append = True
                in_list = False

        m = re.match('<h|<ul|<p|<li', i)
        if not m:
            i = '<p>' + i + '</p>'
        i = parsing_bold_italic(i)
        if in_list_append:
            i = '</ul>' + i
            in_list_append = False
        res += i

    if in_list:
        res += '</ul>'

    return res
