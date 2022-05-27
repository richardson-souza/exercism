"""Functions convert Markdown texts into valid HTML.
"""

import re
from typing import Union


STR_BOLD = r'(.*)__(.*)__(.*)'
STR_ITALIC = r'(.*)_(.*)_(.*)'
STR_LIST = r'\* (.*)'


def match_bold_text(text: str) -> Union[re.Match, None]:
    """Identify if text has a valid character to be
    recognized as Markdown code for bold '__emphasized__'.

    :param text: str - Any text.
    :return: re.Match or None.
    """
    return re.match(STR_BOLD, text)

def match_italic_text(text: str) -> Union[re.Match, None]:
    """Identify if text has a valid character to be
    recognized as Markdown code for talicize '_italicized_'.

    :param text: str - Any text.
    :return: re.Match or None.
    """
    return re.match(STR_ITALIC, text)

def match_list_text(text: str) -> Union[re.Match, None]:
    """Identify if text has a valid character to be
    recognized as Markdown code for unordered lists '*'.

    :param text: str - Any text.
    :return: re.Match or None.
    """
    return re.match(STR_LIST, text)

def parsing_headers_level(text: str) -> str:
    """Identify if text has a structurally valid Markdown
    to recognizes up to 6 hash (#).

    :param text: str - Any text with Mardown code '#'.
    :return: str - Text with section header '<h1>text</h1>'.

    Function that takes any text and converts it to a section
    header HTML elements if it identifies that text has a
    structurally valid Markdown to recognize up to 6 hash
    characters (#) for 6 levels. Otherwise returns text
    without changes.
    """
    headers = {}
    for i in range(1,7):
        headers['#'*i + ' (.*)'] = f'<h{i}>{text[i+1:]}</h{i}>'

    for k, _ in headers.items():
        if re.match(k, text) is not None:
            return headers[k]

    return text

def parsing_italic(match: re.Match) -> str:
    """Convert text with Markdown code for talicize in a valid HTML <em>.

    :param match: re.Match - Object with valid Mardown code '_'.
    :return: str - Text with emphasis element '<em>emphasized</em>'.

    """
    return f'{match.group(1)}<em>{match.group(2)}</em>{match.group(3)}'

def parsing_bold(match: re.Match) -> str:
    """Convert text with Markdown code for bold in a valid HTML <strong>.

    :param match: re.Match - Object with valid Mardown code '__'.
    :return: str - Text with strong importance element <strong>emphasized</strong>.
    """
    return f'{match.group(1)}<strong>{match.group(2)}</strong>{match.group(3)}'

def parsing_bold_italic(text: str) -> str:
    """
    """
    bold_text = match_bold_text(text)
    if bold_text:
        text = parsing_bold(bold_text)

    italic_text = match_italic_text(text)
    if italic_text:
        text = parsing_italic(italic_text)

    return text

def parsing_list(text: str, in_list: bool) -> Union[str, bool]:
    """Convert text with Markdown code for unordered lists '*' in a valid HTML <ul>.

    :param text: str - Literal with valid Mardown code '*'.
    :return: str - Text with unordered list element <ul><li>item</li></ul>.
    """
    if not in_list:
        return '<ul><li>' + text + '</li>', True
    return '<li>' + text + '</li>', in_list

def parse(markdown: str) -> str:
    """Main function
    """
    res = ''
    in_list = False
    in_list_append = False
    for i in markdown.split('\n'):
        i = parsing_headers_level(i)
        match = match_list_text(i)
        if match:
            text = parsing_bold_italic(match.group(1))
            i, in_list = parsing_list(text, in_list)
        else:
            if in_list:
                in_list_append = True
                in_list = False

        match = re.match('<h|<ul|<p|<li', i)
        if not match:
            i = '<p>' + i + '</p>'
        i = parsing_bold_italic(i)
        if in_list_append:
            i = '</ul>' + i
            in_list_append = False
        res += i

    if in_list:
        res += '</ul>'

    return res
