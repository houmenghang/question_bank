# -*- coding: UTF-8 -*-
import asyncio
from bs4 import BeautifulSoup
import tkinter
import json
from time import sleep, time
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

mfw_url = r'https://api.cntv.cn/NewVideo/getVideoListByColumn?id=TOPC1451557052519584&n=20&sort=desc&p={}&mode=0&serviceId=tvcctv&d={}'


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
    bjjt_info = []
    data = json.load(open('bjjt_totle.json', 'r'))
    for key in data.keys():
        i = 1
        while i <= data[key]:  
            url = mfw_url.format(str(i), key)
            await page.goto(url)
            await page.waitFor(2000)
            await asyncio.sleep(1)
            page_text = await page.content()
            bs = BeautifulSoup(page_text,'html.parser')
            try:
                sleep(5)
                bs_dict = eval(bs.pre.text)
                bjjt_info.append({key+'_'+str(i):bs_dict})
            except:
                with open('bjjt2.log', 'a+') as f:
                    f.write('error info key:{} paging: {} \n'.format(key, str(i)))
            i+=1
    with open('bjjt_info3.json', 'w+') as f:
        json.dump(bjjt_info, f)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
