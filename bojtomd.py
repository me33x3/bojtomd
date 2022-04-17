import os
import requests
import json
from bs4 import BeautifulSoup

import util
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

    file.write('<center>\n\n')
    file.write('|시간 제한|메모리 제한|\n')
    file.write('|:---:|:---:|\n')
    file.write('|%s|%s|\n\n' % (problem_info[0].text, problem_info[1].text))
    file.write('</center>\n\n')

    # 문제
    problem_description = soup.select_one("#problem_description")

    # print(problem_description)

    file.write('### 문제\n\n')
    file.write('***\n\n')
    file.write(util.get_content(problem_description))

    # 입력
    problem_input = soup.select_one("#problem_input")

    file.write('### 입력\n\n')
    file.write('***\n\n')
    file.write(util.get_content(problem_input))

    # 출력
    problem_output = soup.select_one("#problem_output")

    file.write('### 출력\n\n')
    file.write('***\n\n')
    file.write(util.get_content(problem_output))

    # 제한
    problem_limit = soup.select_one("#problem_limit")

    # 예제
    problem_sample = soup.select(".sampledata")

    file.write('### 예제\n\n')
    file.write('***\n\n')
    file.write('|입력|출력|\n')
    file.write('|:---|:---|\n')

    for i in range(0, len(problem_sample), 2):
        file.write('|%s|%s|\n' % (problem_sample[i].text.rstrip().replace('\r\n', '<br/>').replace('\n', '<br/>'), problem_sample[i+1].text.rstrip().replace('\r\n', '<br/>').replace('\n', '<br/>')))
    file.write('\n')

    # 힌트

    # 알고리즘 분류
    file.write('### 알고리즘 분류\n\n')
    file.write('***\n\n')
    for i in range(len(data['tags'])):
        file.write('* %s\n' % data['tags'][i]['displayNames'][1]['name'])
    file.write('\n')

    # 시간 제한
    problem_time_limit = soup.select_one("#problem-time-limit")

    if problem_time_limit:
        file.write('### 시간 제한\n\n')
        file.write('***\n\n')
        file.write(util.get_content(problem_time_limit))
        print(problem_time_limit)

    file.close()

    return os.getcwd() + path[1:]
