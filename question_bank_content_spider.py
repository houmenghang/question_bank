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

data = json.load(open('output\yizhandaodi2021.json', 'r'))
print(data)