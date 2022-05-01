def get_content(tag):
    content = ''
    for child in tag:
        if child.name == 'div':
            content += get_div(child)
        elif child.name == 'p':
            content += get_p(child) + '\n\n'
        elif child.name == 'pre':
            content += get_pre(child) + '\n\n'
        elif child.name == 'ol':
            content += get_ol(child) + '\n\n'
        elif child.name == 'ul':
            content += get_ul(child) + '\n\n'
        elif child.name == 'table':
            content += get_table(child) + '\n\n'
        elif child.name == 'blockquote':
            content += get_blockquote(child) + '\n\n'

    return content

def get_div(child):
    return get_content(child)

def get_p(child):
    # 이미지
    if child.find('img'):
        if 'http' not in child.img['src']:
            child.img['src'] = 'https://www.acmicpc.net' + child.img['src']

    text = str(child).replace(' ', ' ')
    if text[:3] == '<p>':
        text = text[3:-4]
    else:
        # 가운데 정렬
        style = child['style']
        if 'center' in style:
            text = '<div align="center">%s</div>' % text[text.index('>') + 1:-4]

    return text

def get_pre(child):
    text = '\n'.join([line.rstrip() for line in child.text.split('\n')])

    if text[0] != '\n':
        text = '\n' + text
    if text[-1] != '\n':
        text += '\n'

    return '```%s```' % text

def get_ol(child):
    text, num = '', 1
    for line in child:
        temp = str(line).lstrip().rstrip()
        if temp:
            text += '%d. %s\n' % (num, temp[4:-5])
            num += 1

    return text.rstrip()

def get_ul(child):
    text = ''
    for line in child:
        temp = str(line).lstrip().rstrip()
        if temp:
            text += '* %s\n' % temp[4:-5]

    return text.rstrip()

def get_table(child):
    return '\n'.join([line for line in str(child).split('\n')])

def get_blockquote(child):
    return str(child)