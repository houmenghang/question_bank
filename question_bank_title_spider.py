import json
import re
import threading
import requests
from bs4 import BeautifulSoup
import os

from requests.api import head

lock = threading.Lock()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

start = 1
end = 620
count = 620*30
url_list = []
while start<=end:
    url = 'https://m.jhq8.cn/daan/tiku/200/%s.html' % str(start)
    response = requests.get(url, headers=HEADERS)
    html = response.content.decode('gbk')
    bs = BeautifulSoup(html,"html.parser")
    for a in bs.find_all('a', href = re.compile('/daan/*'))[3:33]:
        url_dict = {} 
        url_dict['title'] = a.string
        url_dict["url"] = 'https://m.jhq8.cn%s' % a['href']
        url_list.append(url_dict)
        print(url_dict['title'],url_dict["url"])
    start +=1

with open('output\yizhandaodi\2021.json', 'w+') as f:
    json.dump(url_list, f, ensure_ascii=False)