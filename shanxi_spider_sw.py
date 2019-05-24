# -*-coding:utf-8-*-
import json
import re

import redis
import requests
import time
from http import cookiejar
from selenium import webdriver
from test import update_cookie, get_cookies

session = requests.session()
pool = redis.ConnectionPool(host='127.0.0.1', password='', port=6379, db=1)


# 保存数据到redis数据库
def redis_save(xsq_list):
    r = redis.Redis(connection_pool=pool)
    for i in xsq_list:
        name = i['ysqxxid']
        r.set(name, str(i))


def redis_get(choice_list):
    r = redis.Redis(connection_pool=pool)
    L = []
    for l in choice_list:
        s = r.get(l).decode('utf-8')
        L.append(eval(s))
    print(L)
    return L


# 申报查询
def shanxi_spider(startime, endtime):
    # get_cookies()
    c = update_cookie()
    session.cookies.update(c)
    # 登陆后页面
    url = 'https://etax.shaanxi.chinatax.gov.cn/sbzs-cjpt-web/nssb/sbxx/getsbxx.do?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    }
    params = {
        'gdbz': '0',
        'skssqq': '',
        # 'skssqz': '',
        # 'gdslxDm': 3,
        # 'ywbm': '',
        'sbrqq': startime,
        'sbrqz': endtime,
        'reqParamsJSON': '{"gsDjxh":"10116101010000359426","dsDjxh":"10126101010000361431","gsNsrsbh":"91610113MA6W58N53C","dsNsrsbh":"91610113MA6W58N53C","gsZgswjdm":"16101130000","dsZgswjdm":"00000000000","gsSwjgDm":"16101134900","dsSwjgDm":"00000000000"}'
    }
    res = session.get(url, headers=headers, verify=False, params=params)
    print(res.url)
    # res.encoding = 'utf8'
    # print(res.text)
    try:
        html = json.loads(res.text)
    except:
        get_cookies()
        c = update_cookie()
        session.cookies.update(c)
        res = session.get(url, headers=headers, verify=False, params=params)
        print(res.url)
        res.encoding = 'utf8'
        html = json.loads(res.text)
    sbxxList = html['sbxxList']
    xsq_list = []
    xsq_dict = {}
    # print(len(sbxxList),sbxxList)
    for i in sbxxList:
        try:
            xsq_dict['ysqxxid'] = re.search(r'ysqxxid=(.*?)&.*?ywbm=(.*?) ', i['dyurl']).group(1)
            xsq_dict['ywbm'] = re.search(r'ysqxxid=(.*?)&.*?ywbm=(.*?) ', i['dyurl']).group(2)
            xsq_dict['yzpzzlmc'] = i['yzpzzlmc']
            xsq_dict['sbrq'] = i['sbrq']
            xsq_list.append((xsq_dict))
            xsq_dict = {}
        except Exception:
            pass
    if len(xsq_list) == 0:
        s = '没有可下载信息'
        return s
    # print(len(xsq_list), xsq_list)
    redis_save(xsq_list)

    return xsq_list


# 下载保存到电脑
def dowonload(ysqxxid_list):
    choice_list = redis_get(ysqxxid_list)
    c = update_cookie()
    session.cookies.update(c)
    url = 'https://etax.shaanxi.chinatax.gov.cn/zlpz-cjpt-web/zlpz/viewOrDownloadPdfFile.do?'
    dict = {}
    for y in choice_list:
        name = y['yzpzzlmc'][1:-1] + y['sbrq'] + y['ysqxxid'][:-5]
        params = {
            'ysqxxid': y['ysqxxid'],
            'viewOrDownload': 'download',
            'gdslxDm': '1',
            'ywbm': y['ywbm'],
            'DZSWJ_TGC': 'a8e41e16ae09406287e6c38bbc4064c1'
        }
        headers = {
            'User-Agent': 'Mowindowszilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }
        res = session.get(url, headers=headers, verify=False, params=params)
        if res.status_code != 200:
            get_cookies()
            c = update_cookie()
            session.cookies.update(c)
            res = session.get(url, headers=headers, verify=False, params=params)
        dict[name] = res.content
        print(res.content)
        try:
            with open('%s.pdf' % name, 'wb') as f:
                f.write(res.content)
                print('%s保存成功' % name)
        except Exception:
            print('下载失败')
        # res.encoding = 'utf8'
        # html = res.text
        # print(html, type(html))
    s = '成功下载%s项' % len(choice_list)
    return dict
