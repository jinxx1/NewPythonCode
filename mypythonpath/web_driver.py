#!/usr/bin/env python
# coding:utf-8
import requests
from hashlib import md5
import selenium,time,logging
from PIL import Image
import platform
sys_code = platform.system()

if sys_code == 'Windows':
    chromePath = r"D:\PythonCode\mypythonpath\wd\chromedriver"
    jsPath = r"D:\PythonCode\mypythonpath\wd\stealth.min.js"
elif sys_code == 'Linux':
    jsPath = "/home/terry/anaconda3/lib/python3.7/site-packages/mtools/wd/stealth.min.js"
    chromePath = "/home/terry/anaconda3/lib/python3.7/site-packages/mtools/wd/chromedriver"
else:
    raise 'The System is not Windows or Linux, Exit Program'
    exit()




class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

    def getscore(self):
        r = requests.post('http://upload.chaojiying.net/Upload/GetScore.php', data=self.base_params, headers=self.headers)
        return r.json()

def webdriver_getCookie_fujian(url,path,code):


    # 启动webdrviver仿真，获取cookies用。使用chrmedrvier
    pageUrl = url
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    import os
    root = os.getcwd()
    stealthPath = os.path.join(root, jsPath)
    chrodriverPath = os.path.join(root, chromePath)
    # proxIP = "118.24.219.151:16818"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        'user-agent={}'.format("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"))
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--no-sandbox')

    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = Chrome(chrodriverPath, options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    # driver.set_window_size(1200, 800)
    with open(stealthPath, 'r') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
    try:
        driver.get(pageUrl)
        time.sleep(3)



    except Exception as ff:
        driver.quit()
        return None


    element = driver.find_element_by_id('verifycode')
    element.screenshot(path)


    chaojiying = Chaojiying_Client('18024587265', 'Xey123456', '930314')  # 用户中心>>软件ID 生成一个替换 96001
    im = open(path, 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    im_code = chaojiying.PostPic(im, code)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    print(im_code)

    driver.find_element_by_name("verifycode").clear()

    driver.find_element_by_name("verifycode").send_keys(im_code['pic_str'])  # 这一步是在元素中输入数据
    driver.find_element_by_xpath("//button[@onclick='tj()']").click()
    time.sleep(3)
    c = driver.get_cookies()
    page_html = driver.page_source

    cookies = {}
    # 获取cookie中的name和value,转化成requests可以使用的形式
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    #
    # aa ={'err_no': 0,
    #      'err_str': 'OK',
    #      'pic_id': '1173722138185300963',
    #      'pic_str': '失丛令白',
    #  'md5': '5797832a5d9f5371cc22be0ab7d5421d'}
    ddict = {}
    ddict['pic_str'] = im_code['pic_str']
    ddict['cookies'] = cookies
    ddict['html'] = page_html
    ddict['Referer'] = driver.current_url
    driver.quit()
    return ddict


if __name__ == '__main__':
    chaojiying = Chaojiying_Client('18024587265', 'Xey123456', '930314')  # 用户中心>>软件ID 生成一个替换 96001
    aa = chaojiying.getscore()
    print(aa)

    exit()
    code = 2004
    path = r"D:\PythonCode\MyCrawlFrame\orcpic/code.png"
    url = "http://www.ccgp-fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/"
    aa = webdriver_getCookie_fujian(url,path,code)
    print(aa)
    postUrl = "http://www.ccgp-fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/?page=1"

    brow = requests.get(url=postUrl,cookies=aa['cookies'])
    print(brow.text)