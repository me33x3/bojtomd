def get_content(tag):
    content = ''
    for child in tag:
        if child.name == 'p':
            content += get_p(child) + '\n\n'
        elif child.name == 'pre':
            content += get_pre(child) + '\n\n'
        elif child.name == 'ol':
            content += get_ol(child) + '\n\n'
        elif child.name == 'ul':
            content += get_ul(child) + '\n\n'
        elif child.name == 'table':
            content += get_table(child) + '\n\n'

    return content

def get_p(child):
    # 이미지
    if child.find('img'):
        if 'http' not in child.img['src']:
            child.img['src'] = 'https://www.acmicpc.net' + child.img['src']

    text = str(child)
    if text[:3] == '<p>':
        text = text[3:-4]

    return text

def get_pre(child):
    text = '\n'.join([line.rstrip() for line in child.text.split('\n')])

    if text[-1] != '\n':
        text += '\n'

    return '```%s```' % text

def get_ol(child):
    text = ''
    for i, line in enumerate(child.text.lstrip().rstrip().split('\n')):
        text += '%d. %s\n' % (i + 1, line)

    return text.rstrip()

def get_ul(child):
    text = ''
    for line in child.text.lstrip().rstrip().split('\n'):
        text += '* %s\n' % line

    return text.rstrip()

def get_table(child):
    return '\n'.join([line for line in str(child).split('\n')])