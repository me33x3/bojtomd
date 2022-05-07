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
            content += get_ol(child, 0) + '\n\n'
        elif child.name == 'ul':
            content += get_ul(child, 0) + '\n\n'
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

def get_ol(child, depth):
    text, num = '', ord('1')

    style = get_style(child)
    if 'list-style-type' in style:
        type = style['list-style-type']
        if type == 'lower-alpha':
            num = ord('a')
        elif type == 'upper-alpha':
            num = ord('A')

    for line in child:
        if line.text.strip() == '':
            continue

        for sub in line:
            if sub.text.strip() == '':
                continue
            elif sub.name == 'ol':
                text += get_ol(sub, depth + 1)
            elif sub.name == 'ul':
                text += get_ul(sub, depth + 1)
            else:
                print(chr(num), sub)
                text += '\t' * depth + '%c. %s  \n' % (chr(num), sub.strip().replace(' ', ' '))
                num += 1

    return text.rstrip()

def get_ul(child, depth):
    text = ''

    for line in child:
        if line.text.strip() == '':
            continue

        for sub in line:
            if sub.text.strip() == '':
                continue
            elif sub.name == 'ol':
                text += get_ol(sub, depth + 1)
            elif sub.name == 'ul':
                text += get_ul(sub, depth + 1)
            else:
                text += '\t' * depth + '* %s  \n' % sub.strip().replace(' ', ' ')

    return text.rstrip()

def get_table(child):
    return '\n'.join([line for line in str(child).split('\n')])

def get_blockquote(child):
    return str(child)

def get_style(tag):
    style = {}
    if 'style' in tag.attrs:
        for attr in tag['style'].split(';')[:-1]:
            k, v = attr.split(':')
            style[k] = v
    return style