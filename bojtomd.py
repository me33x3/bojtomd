import os
import requests
import json
from bs4 import BeautifulSoup

from config import tier

def crawl_baekjoon(problem_id):
    url = 'https://www.acmicpc.net/problem/%d' % problem_id
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    return BeautifulSoup(res.text.rstrip(), 'html.parser')

def fetch_solvedac(problem_id):
    url = 'https://solved.ac/api/v3/problem/show?problemId=%d' % problem_id
    res = requests.get(url)

    return [res.status_code, res.text]

def write(data):
    data = json.loads(data)
    soup = crawl_baekjoon(data['problemId'])
    print(data)

    base = '.\\files'
    path = base + '\\%s.md' % data['problemId']

    if not os.path.exists(base):
        os.makedirs(base)

    file = open(path, 'w', encoding='UTF-8')

    # 제목 및 티어
    file.write('# %s\n\n' % data['titleKo'])
    file.write('> <img src="https://d2gd6pc034wcta.cloudfront.net/tier/%d.svg" width="16" heigth="21" style = "vertical-align: middle;"/>' % data['level'])
    file.write('&nbsp;')
    file.write('<span style="font-size: 18px; color: %s;">%s</span>\n\n' % (tier[data['level']][1], tier[data['level']][0]))
    file.write('***\n\n')

    # 문제 정보
    problem_info = soup.select('#problem-info > tbody > tr > td')
    print(problem_info)

    file.write('<center>\n\n')
    file.write('|시간 제한|메모리 제한|\n')
    file.write('|:---:|:---:|\n')
    file.write('|%s|%s|\n' % (problem_info[0].text, problem_info[1].text))
    file.write('</center>\n\n')

    file.close()

    return os.getcwd() + path[1:]
