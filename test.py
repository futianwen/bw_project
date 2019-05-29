import requests
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
import json
import time
import redis
import random
from user_agent import user_agent
# from get_cookies import get_cookies
from io import BytesIO
from PIL import Image
from lxml import etree
t = time.time()  # 时间戳
t = time.localtime(t)  # 通过time.localtime将时间戳转换成时间组
t = time.strftime("%Y-%m-%d", t)  # 再将时间组转换成指定格式
ua = random.choice(user_agent)
headers = {
    'Host': 'etax.shaanxi.chinatax.gov.cn',
    'User-Agent': ua
}
login_url = 'https://etax.shaanxi.chinatax.gov.cn/sso/login'
session = requests.session()


def get_cookies():
    response = session.get(url=login_url, headers=headers, verify=False)
    cookie_dict = requests.utils.dict_from_cookiejar(response.cookies)
    print(cookie_dict)
    html = etree.HTML(response.text)

    lt = html.xpath("//input[@name='lt']/@value")[0]
    execution = html.xpath("//input[@name='execution']/@value")[0]
    _eventId = 'submit'
    _llqmc = 'Chrome'
    _llqbb = '74.0.3729.169'
    _czxt = 'Mac'
    _czxtbb = 'Unknown'
    csessionid = ''
    sig = ''
    token = ''
    scene = ''
    loginType = '0'
    authencationHandler = html.xpath("//input[@name='authencationHandler']/@value")[0]
    userName = ''
    passWord = ''
    sjly = '2'

    yzm_url = 'https://etax.shaanxi.chinatax.gov.cn/sso/base/captcha.do'
    image = session.get(yzm_url, headers=headers).content
    image = BytesIO(image)
    image = Image.open(image)
    image.show()
    yzm = input('yzm:')
    data = {
        'lt': lt,
        'execution': execution,
        '_eventId': _eventId,
        '_llqmc': _llqmc,
        '_llqbb': _llqbb,
        '_czxt': _czxt,
        '_czxtbb': _czxtbb,
        'csessionid': csessionid,
        'sig': sig,
        'token': token,
        'scene': scene,
        'loginType': loginType,
        'authencationHandler': authencationHandler,
        'userName': userName,
        'passWord': passWord,
        'sjly': sjly,
        'captchCode': yzm
    }
    # login_url = 'https://etax.shaanxi.chinatax.gov.cn/sso/login'
    lg_resp = session.post(login_url, headers=headers, data=data)
    cookies = requests.utils.dict_from_cookiejar(lg_resp.cookies)
    cookie_dict.update(cookies)
    with open('cookie.json', 'w') as f:
        f.write(json.dumps(cookie_dict))


# def update_cookie():
#     # get values of cookies from cookie.json and save to CookieJar object
#     c = requests.cookies.RequestsCookieJar()
#     with open('cookie.json', 'r') as f:
#         a = json.loads(f.read())
#         for i in a:
#             c.set(i, a[i])
#     return c
# 登录并获取cookie，将cookie值保存
# def get_cookies():
#     # creat a class options
#     chrome_options = webdriver.ChromeOptions()
#     # 无头模式
#     # chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     # creat driver object and send a requestion
#     driver = webdriver.Chrome(chrome_options=chrome_options)
#     driver.get(login_url)
#     # login
#     WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.ID, 'userName'))
#     )
#     # username.send_keys('91610113MA6W58N53C')
#     # 5秒内获取所需要的元素，如果没找到，等待5秒，报错
#     WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.ID, 'passWord'))
#     )
#     # password.send_keys('425607')
#     username = driver.find_element_by_id('userName')
#     password = driver.find_element_by_id('passWord')
#     username.send_keys('91610113MA6W58N53C')
#     password.send_keys('425607')
#     yzm = input('yzm:')
#     yzm_tag = driver.find_element_by_id('captchCode')
#     yzm_tag.send_keys(yzm)
#     driver.find_element_by_id('upLoginButton').click()
#     # get and save cookies
#     cookie = driver.get_cookies()
#     cookie_dict = {}
#     for i in cookie:
#         a = {i['name']: i['value']}
#         cookie_dict.update(a)
#     with open('cookie.json', 'w') as f:
#         f.write(json.dumps(cookie_dict))
#     time.sleep(10)
    # driver.quit()


# 更新cookie
def update_cookie():
    # get values of cookies from cookie.json and save to CookieJar object
    c = requests.cookies.RequestsCookieJar()
    with open('cookie.json', 'r') as f:
        a = json.loads(f.read())
        for i in a:
            c.set(i, a[i])
    return c


# 读取cookie值并进行发出查询请求
def jk_info(date_list):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)

    # update cookies in session
    c = update_cookie()
    session.cookies.update(c)
    # date_list = ['2019-04-01', '2019-04-30', '2019-01-01', '2019-05-31']
    url = 'https://etax.shaanxi.chinatax.gov.cn/sbzs-cjpt-web/tycx/query.do?bw=%7B%22taxML%22:%7B%22head%22:%7B%22gid%22:%22311085A116185FEFE053C2000A0A5B63%22,%22sid%22:%22gjyy.yhscx.SBZS.YJSKCX%22,%22tid%22:%22+%22,%22version%22:%22%22%7D,%22body%22:%7B%22gdbz%22:%22%22,%22jkrqq%22:%22{}%22,%22jkrqz%22:%22{}%22,%22skssqq%22:%22{}%22,%22skssqz%22:%22{}%22%7D%7D%7D&djxh=10116101010000359426&gdslxDm=1'.format(
        date_list[0], date_list[1], date_list[2], date_list[3])
    resp = session.get(url, headers=headers, allow_redirects=False)
    if resp.status_code == 302:
        while True:
            print('cookie过期')
            get_cookies()
            c = update_cookie()
            session.cookies.update(c)
            resp = session.get(url, headers=headers, allow_redirects=False)
            if resp.status_code == 200:
                break
    elif resp.status_code == 500:
        print('服务器故障')
        resp = session.get(url, headers=headers, allow_redirects=False)
    resp = json.loads(resp.text)
    info_list = resp['taxML']['body']['taxML']['jsxxList']['jsxx']
    ser = 1
    info_dict = {}
    for info in info_list:
        i = {ser: info}
        info_dict.update(i)
        ser += 1
    r.set(''.join(date_list), str(info_dict))
    return info_dict


# 下载凭证
def down_pz(data):
    c = update_cookie()
    session.cookies.update(c)
    print(data)
    params = {
        'xsltPath': '/sw.sb.dzjkpz.pdf',
        'qrcodeContent': '',
        'data': data,
        'gdslxDm': '1'
    }
    id_url = 'https://etax.shaanxi.chinatax.gov.cn/sbzs-cjpt-web/tycx/hcJkpzPdf.do'
    yzqxxid = session.post(id_url, headers=headers, data=params, allow_redirects=False)
    print(yzqxxid.status_code)
    if yzqxxid.status_code == 302:
        print('cookie过期')
        while True:
            get_cookies()
            c = update_cookie()
            session.cookies.update(c)
            yzqxxid = session.post(id_url, headers=headers, data=params, allow_redirects=False)
            if yzqxxid.status_code == 200:
                break

    yzqxxid = json.loads(yzqxxid.text)
    print(yzqxxid)
    yzqxxid = yzqxxid['yzqxxid']
    pdf_url = 'https://etax.shaanxi.chinatax.gov.cn/zlpz-cjpt-web/zlpz/showPdfByYzqxxidAndDzbzdszlDm.do?yzqxxid={}&viewOrDownload=download&dzbzdszlDm=jkpzdy&gdslxDm=1'.format(
        yzqxxid)
    print(pdf_url)
    r = session.post(pdf_url, headers=headers)
    print(r.content)
    with open('jkpz.pdf', 'wb') as f:
        f.write(r.content)
    return r.content
