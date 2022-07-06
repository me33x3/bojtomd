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

    if text:
        if text[0] != '\n':
            text = '\n' + text
        if text[-1] != '\n':
            text += '\n'
    else:
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

        sub_text = ''
        has_sub = False

        if len(line) > 1:
            for sub in line:
                if sub.name == 'ol':
                    sub_text += get_ol(sub, depth + 1)
                    has_sub = True
                elif sub.name == 'ul':
                    sub_text += get_ul(sub, depth + 1)
                    has_sub = True

        if has_sub:
            text += '\t' * depth + '%c. %s  \n' % (chr(num), str(line).split('\n')[0].strip().replace(' ', ' ')[4:]) + sub_text
        else:
            text += '\t' * depth + '%c. %s  \n' % (chr(num), str(line).strip().replace(' ', ' ')[4:-5])
        num += 1

    return text.rstrip()

def get_ul(child, depth):
    text = ''

    for line in child:
        if line.text.strip() == '':
            continue

        sub_text = ''
        has_sub = False

        if len(line) > 1:
            for sub in line:
                if sub.name == 'ol':
                    sub_text += get_ol(sub, depth + 1)
                    has_sub = True
                elif sub.name == 'ul':
                    sub_text += get_ul(sub, depth + 1)
                    has_sub = True

        if has_sub:
            text += '\t' * depth + '* %s  \n' % str(line).split('\n')[0].strip().replace(' ', ' ')[4:-5] + sub_text
        else:
            text += '\t' * depth + '* %s  \n' % str(line).strip().replace(' ', ' ')[4:-5]

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