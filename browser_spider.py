# -*- coding: UTF-8 -*-
import asyncio
from bs4 import BeautifulSoup
import logging
import tkinter
import re
import os
import json
import random
 
from pyppeteer import launcher
# 第一步 去除浏览器自动化参数
# 必须在 from pyppeteer import launch 前去除参数
# 去除自动化 启动参数
launcher.DEFAULT_ARGS.remove('--enable-automation')

from pyppeteer import launch
from lxml import etree

# 第二步，修改 navigator.webdriver检测
# 其实各种网站的检测js是不一样的，这是比较通用的。有的网站会检测运行的电脑运行系统，cpu核心数量，鼠标运行轨迹等等。
# 反爬js
js_text = """
() =>{ 
    Object.defineProperties(navigator,{ webdriver:{ get: () => false } });
    window.navigator.chrome = { runtime: {},  };
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], });
 }
"""

proxy_list = [
    '115.231.128.79:8080',
    '166.111.77.32:80',
    '43.240.138.31:8080'
]

mfw_url = r'http://www.mafengwo.cn/search/q.php?q={}'


def get_city_list():
    #cities = json.load(open('city_list.json', encoding='utf-8'))
    #random.shuffle(cities)
    cities = ['杭州']
    return cities

async def main():
    # 浏览器 启动参数
    start_parm = {
        # 启动chrome的路径
        "executablePath": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        # 关闭无头浏览器
        "headless": False,
        "args": [
            '--disable-infobars',  # 关闭自动化提示框
            # '--window-size=1920,1080',  # 窗口大小
            '--log-level=30',  # 日志保存等级， 建议设置越好越好，要不然生成的日志占用的空间会很大 30为warning级别
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',  # UA
            '--no-sandbox',  # 关闭沙盒模式
            '--start-maximized',  # 窗口最大化模式
            #'--proxy-server=115.231.128.79:8080'  # 代理
        ],
        "userDataDir": "./temp",
    }

    browser = await launch(**start_parm)
    page = await browser.newPage()

    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    await page.setViewport(viewport={'width': width, 'height': height})
    await page.evaluateOnNewDocument(js_text)  # 本页刷新后值不变，自动执行js

    cities = get_city_list()
    for city in cities:
        city_dir = 'city_intros/{}'.format(city)
        os.makedirs(city_dir, exist_ok=True)
        city_url = mfw_url.format(city)
        print(city_url)
        await page.goto(city_url)
        await page.waitFor(300)
        page_text = await page.content()
        soup = BeautifulSoup(page_text, 'html.parser')
        places = soup.findAll(class_='top_pois common')
        #import ipdb; ipdb.set_trace()
        await asyncio.sleep(random.uniform(1.0, 9.0))
        for pl in places:
            spot_name = pl.find(class_='title').get_text()
            city_file = '{}/{}.txt'.format(city_dir, spot_name)
            if os.path.exists(city_file):
                print('{} already finished'.format(city_file))
                continue
            url = pl['href']
            await page.goto(url)
            print(page)
            await page.waitFor(2000)
            page_txt = await page.content()
            sp = BeautifulSoup(page_txt, 'html.parser')
            intro = sp.find('script', text=re.compile("#_j_sharecnt"))
            if intro is None:
                continue
            cont = intro.decode_contents()
            txt = cont.split("'")[-2].replace(r'\n', '').replace(' ', '')
            if len(txt.strip()) == 0:
                continue
            # save txt
            with open(city_file, 'w', encoding='utf-8') as f:
                f.write(txt)
            print('{} {} done'.format(city, spot_name))
            await asyncio.sleep(random.uniform(1.1, 5.4))
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())