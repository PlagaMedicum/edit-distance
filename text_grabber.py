import re
import requests
from bs4 import BeautifulSoup


BLACKLIST = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head',
    'input',
    'script',
    'style',
    'displaystyle',
]
WORDS = re.compile(r'\W+')

def grab_text(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    for t in text:
        if t.parent.name not in BLACKLIST:
            output += '{} '.format(t)

    output = ' '.join(output.split())
    return WORDS.split(output)
