import re


def parsing_headers_level(text):
    headers = {}
    for i in range(1,7):
        headers['#'*i + ' (.*)'] = f'<h{i}>{text[i+1:]}</h{i}>'

    for key in headers:
        if re.match(key, text) is not None:
            return headers[key]
    
    return text

def parsing_italic(match):
    return f'{match.group(1)}<em>{match.group(2)}</em>{match.group(3)}'

def parsing_bold(match):
    return f'{match.group(1)}<strong>{match.group(2)}</strong>{match.group(3)}'

def parse(markdown):
    lines = markdown.split('\n')
    res = ''
    in_list = False
    in_list_append = False
    for i in lines:
        i = parsing_headers_level(i)
        m = re.match(r'\* (.*)', i)
        if m:
            if not in_list:
                in_list = True
                is_bold = False
                is_italic = False
                curr = m.group(1)
                m1 = re.match('(.*)__(.*)__(.*)', curr)
                if m1:
                    curr = parsing_bold(m1)
                    is_bold = True
                m1 = re.match('(.*)_(.*)_(.*)', curr)
                if m1:
                    curr = parsing_italic(m1)
                    is_italic = True
                i = '<ul><li>' + curr + '</li>'
            else:
                is_bold = False
                is_italic = False
                curr = m.group(1)
                m1 = re.match('(.*)__(.*)__(.*)', curr)
                if m1:
                    is_bold = True
                m1 = re.match('(.*)_(.*)_(.*)', curr)
                if m1:
                    is_italic = True
                if is_bold:
                    curr = parsing_bold(m1)
                if is_italic:
                    curr = parsing_italic(m1)
                i = '<li>' + curr + '</li>'
        else:
            if in_list:
                in_list_append = True
                in_list = False

        m = re.match('<h|<ul|<p|<li', i)
        if not m:
            i = '<p>' + i + '</p>'
        m = re.match('(.*)__(.*)__(.*)', i)
        if m:
            i = parsing_bold(m)
        m = re.match('(.*)_(.*)_(.*)', i)
        if m:
            i = parsing_italic(m)
        if in_list_append:
            i = '</ul>' + i
            in_list_append = False
        res += i
    if in_list:
        res += '</ul>'
    return res
