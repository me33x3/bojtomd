import requests
from bs4 import BeautifulSoup

def crawl(problem_id):
    url = 'https://www.acmicpc.net/problem/%d' % problem_id
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    return [response.status_code, BeautifulSoup(response.text.rstrip(), 'html.parser')]