"""Functions convert Markdown texts into valid HTML.
"""

import re


STR_BOLD = '(.*)__(.*)__(.*)'
STR_ITALIC = '(.*)_(.*)_(.*)'
STR_LIST = '\* (.*)'


def get_bold_text(text: str) -> str:
    """Identify if text has a valid character to be
    recognized as Markdown code for bold '__emphasized__'.
    :param text: str - Any text.
    :return: str - Text with character recognized as 
    Markdown code to bold.
    """
    m = re.match(STR_BOLD, text)
    if m:
        return m.group(1)

def get_italic_text(text: str) -> str:
    """Identify if text has a valid character to be
    recognized as Markdown code for talicize ' _italicized_'.
    :param text: str - Any text.
    :return: str - Text with character recognized as 
    Markdown code to talicize.
    """
    m = re.match(STR_ITALIC, text)
    if m:
        return m.group(1)

def get_list_text(text: str) -> str:
    """Identify if text has a valid character to be
    recognized as Markdown code for unordered lists '*'.
    :param text: str - Any text.
    :return: str - Text with character recognized as 
    Markdown code to unordered lists.
    """
    m = re.match(STR_LIST, text)
    if m:
        return m.group(1)

def parsing_headers_level(text: str) -> str:
    """Identify if text has a structurally valid Markdown 
    to recognizes up to 6 hash (#).

    :param text: str - Any text.
    :return: str - Text with valid HTML Section Heading elements.

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
    return f'{match.group(1)}<em>{match.group(2)}</em>{match.group(3)}'

def parsing_bold(match: re.Match) -> str:
    return f'{match.group(1)}<strong>{match.group(2)}</strong>{match.group(3)}'

def parsing_bold_italic(text: str) -> str:
    m1 = re.match(STR_BOLD, text)
    if m1:
        text = parsing_bold(m1)

    m1 = re.match(STR_ITALIC, text)
    if m1:
        text = parsing_italic(m1)
    return text

def parse(markdown: str) -> str:
    res = ''
    in_list = False
    in_list_append = False
    for i in markdown.split('\n'):
        i = parsing_headers_level(i)

        text = get_list_text(i)
        if text:
            if not in_list:
                in_list = True
                text = parsing_bold_italic(text)
                i = '<ul><li>' + text + '</li>'
            else:
                text = parsing_bold_italic(text)
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
