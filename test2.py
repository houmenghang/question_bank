import asyncio

import pyppeteer
from pyppeteer import launch
from pyquery import PyQuery as pq

# 官方文档
# https://miyakogi.github.io/pyppeteer/reference.html

url = "https://dynamic2.scrape.center/"


# 粒子01
async def main1():
    # launch 方法会新建一个 Browser 对象，其执行后最终会得到一个 Browser 对象，
    # 然后赋值给 browser。这一步就相当于启动了浏览器
    browser = await launch()
    # 然后 browser 调用 newPage  方法相当于浏览器中新建了一个选项卡，同时新建了一个 Page 对象，
    # 这时候新启动了一个选项卡，但是还未访问任何页面，浏览器依然是空白
    page = await browser.newPage()
    # 随后 Page 对象调用了 goto 方法就相当于在浏览器中输入了这个 URL，浏览器跳转到了对应的页面进行加载。
    await page.goto(url)
    # Page 对象调用 waitForSelector 方法，传入选择器，那么页面就会等待选择器所对应的节点信息加载出来，
    # 如果加载出来了，立即返回，否则会持续等待直到超时。此时如果顺利的话，页面会成功加载出来。
    await page.waitForSelector(".item .name")
    # 页面加载完成之后再调用 content 方法，可以获得当前浏览器页面的源代码，这就是 JavaScript 渲染后的结果。
    doc = pq(await page.content())
    # 然后进一步的，我们用 pyquery 进行解析并提取页面的电影名称，就得到最终结果了。
    names = [item.text() for item in doc(".item .name").items()]
    print("Names: ", names)
    await browser.close()


# asyncio.get_event_loop().run_until_complete(main1())

# 粒子02
width, height = 1366, 768


async def main2():
    # browser = await launch(headless=False)  # 有界面的，创建一个空白的浏览器
    # browser = await launch(devtools=True)  # 有界面的，创建一个空白的浏览器,右侧直接打开调试工具
    # browser = await launch(headless=False, args=["--disable-infobars"])  # 有界面的，创建一个空白的浏览器,右侧直接打开调试工具
    # 使得浏览器的窗口和打开的标签内的网页大小一致
    # browser = await launch(headless=False,
    #                        args=["--disable-infobars", f'--window-size={width},{height}'])  # 有界面的，创建一个空白的浏览器,右侧直接打开调试工具
    # userDataDir读取本地浏览器配置信息，可以缓存cookies，再次运行程序会读取这些配置
    browser = await launch(headless=False, userDataDir='./userdata', args=['--disable-infobars'])
    # browser = await launch()

    # 无痕模式 使用context对象创建page选项卡
    # context = await browser.createIncognitoBrowserContext()
    # page = await context.newPage()

    page = await browser.newPage()
    # 防止浏览器检测webdriver
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
    await page.setViewport({"width": width, "height": height})  # 设置窗口大小
    await page.goto(url)
    await page.waitForSelector(".item .name")
    await asyncio.sleep(2)
    await page.screenshot(path="example.png")
    dimensions = await page.evaluate("""() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }""")
    print(dimensions)  # {'width': 1366, 'height': 768, 'deviceScaleFactor': 1} 网页宽高和像素
    await browser.close()


#
#
# asyncio.get_event_loop().run_until_complete(main2())


# 粒子03 Page选择器
async def main3():
    browser = await launch()
    page = await browser.newPage()
    await page.goto("https://dynamic2.scrape.center/")
    await page.waitForSelector(".item .name")
    #  J 方法传入一个选择器 Selector，则能返回对应匹配的第一个节点，等价于 querySelector。
    #  如 JJ 方法则是返回符合 Selector 的列表，类似于 querySelectorAll。
    j_result1 = await page.J(".item .name")
    j_result2 = await page.querySelector(".item .name")
    jj_result1 = await page.JJ(".item .name")
    jj_result2 = await page.querySelectorAll(".item .name")
    print("J Result1:", j_result1)
    print("J Result2:", j_result2)
    print("JJ Result1:", jj_result1)
    print("JJ Result2:", jj_result2)
    await browser.close()


# asyncio.get_event_loop().run_until_complete(main3())


# 粒子04 选项卡操作
async def main4():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto("https://www.baidu.com")
    page = await browser.newPage()
    await page.goto("https://www.bing.com")
    pages = await browser.pages()  # 获取所有选项卡
    print("Pages:", pages)
    page1 = pages[1]  # 选择准备切换到的选项卡
    await page1.bringToFront()  # 切换到对应的选项卡
    await asyncio.sleep(10)


# asyncio.get_event_loop().run_until_complete(main4())

# 粒子05 page页面常规操作
async def main5():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('https://dynamic1.scrape.center/')
    await page.goto('https://dynamic2.scrape.center/')
    await page.goBack()  # 后退
    await page.goForward()  # 前进
    await page.reload()  # 刷新
    await page.pdf()  # 保存pdf
    await page.screenshot()  # 截图
    await page.setViewport("<h2>Hello World</h2>")  # 设置页面HTML
    await page.setUserAgent("python")  # 设置ua
    await page.setExtraHTTPHeaders(headers={})  # 设置headers
    await page.close()  # 关闭
    await browser.close()


# asyncio.get_event_loop().run_until_complete(main5())

# 粒子06 模拟点击操作
async def main6():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto("https://dynamic2.scrape.center/")
    await page.waitForSelector(".item .name")
    await page.click(".item .name", options={
        "button": "right",  # 鼠标按钮，分为 left、middle、right
        "clickCount": 1,  # 1或2 双击、单击
        "delay": 3000  # 毫秒 延迟点击
    })
    # await page.type('#q', 'iPad')  # 定位 输入文本  如send_keys,这里是type方法
    # print('HTML:', await page.content())  # 获取整个网页源代码，需要配合pq解析
    # print('Cookies:', await page.cookies())   # 获取cookies
    await browser.close()


asyncio.get_event_loop().run_until_complete(main6())
# 除了 waitForSelector 方法，还有很多其他的等待方法，介绍如下。
# waitForFunction：等待某个 JavaScript 方法执行完毕或返回结果。
# waitForNavigation：等待页面跳转，如果没加载出来就会报错。
# waitForRequest：等待某个特定的请求被发出。
# waitForResponse：等待某个特定的请求收到了回应。
# waitFor：通用的等待方法。
# waitForSelector：等待符合选择器的节点加载出来。
# waitForXPath：等待符合 XPath 的节点加载出来。
# 通过等待条件，我们就可以控制页面加载的情况了。

