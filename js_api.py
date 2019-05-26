import flask
from flask import request
from test import jk_info, down_pz
import json
import redis
from shanxi_spider_sw import shanxi_spider, dowonload
from switch import digital_to_chinese
from urllib.parse import quote
import time

r = redis.Redis(host='127.0.0.1', port=6379)
t = time.time()  # 时间戳
t = time.localtime(t)  # 通过time.localtime将时间戳转换成时间组
t = time.strftime("%Y-%m-%d", t)  # 再将时间组转换成指定格式
server = flask.Flask(__name__)


# 缴款查询api
@server.route('/info', methods=['get'])
def info():
    date1 = request.values.get('date1')
    date2 = request.values.get('date2')
    date3 = request.values.get('date3')
    date4 = request.values.get('date4')
    if date3 is None:
        date3 = t.split('-')[0] + '-01' + '-01'
    if date4 is None:
        date4 = t
    date = [date1, date2, date3, date4]
    result = jk_info()
    result = json.dumps(result)
    return result


# 缴款凭证下载api
@server.route('/items', methods=['get'])
def items():
    item_infos = r.get('2019-04-012019-04-302019-01-012019-05-31')
    item_infos = str(item_infos, encoding='utf-8')
    print(item_infos)
    item_infos = eval(item_infos)
    info_list = item_infos['taxML']['body']['taxML']['jsxxList']['jsxx']
    jexx = 0
    xml_fw = '<?xml version="1.0" encoding="UTF-8"?><taxML><head><publichead><nsrsbh>91610113MA6W58N53C</nsrsbh><nsrmc>西安沪友发展信息科技有限公司</nsrmc><jgmc>国家税务总局西安市雁塔区税务局电子城税务所</jgmc><yhzh>61050176004300000319</yhzh><dyrq>{}</dyrq><pzbh></pzbh><gdslxDm>1</gdslxDm></publichead></head><body><pageggxx><printCount></printCount><pageoneprintflag></pageoneprintflag><pagetwoprintflag></pagetwoprintflag><pagethreeprintflag></pagethreeprintflag><pageCount></pageCount><pagexml></pagexml></pageggxx><pageone><pagexx><jexx>{}</jexx><jedx>{}</jedx><pageCount></pageCount><jkxx>'
    xml_af = '</jkxx></pagexx></pageone></body></taxML>'
    for info in info_list:
        xtsph = info['dzsphm']
        sfzmc = info['zsxmmc']
        spmmc = info['zspmmc']
        ssqqz = info['skssqq'] + '至' + info['skssqz']
        jkrq = info['kjrq']
        jkje = round(float(info['sjje']), 2)
        jexx += jkje
        pdf_data = '<jkxxmi><xtsph>{}</xtsph><sfzmc>{}</sfzmc><spmmc>{}</spmmc><ssqqz>{}</ssqqz><jkrq>{}</jkrq><jkje>{}</jkje></jkxxmi>'.format(
            xtsph, sfzmc, spmmc, ssqqz, jkrq, jkje)
        xml_fw += pdf_data
    jedx = digital_to_chinese(round(jexx, 2))
    data = xml_fw + xml_af
    data = data.format(t, round(jexx, 2), jedx)
    # print(data)

    data = quote(data)
    pdf_data = down_pz(data)
    return pdf_data


# 获取下载列表并返回
@server.route('/pgd', methods=['get'])
def gbk():
    # url = 'http://127.0.0.1:8000/pgd?startime=2018-12-01&endtime=2019-05-01'
    date1 = request.args.get('startime')
    date2 = request.args.get('endtime')
    result = shanxi_spider(date1, date2)
    return json.dumps(result)


# 接收下载项，完成下载
@server.route('/pgd/download', methods=['get'])
def dowmload():
    # url = 'http://127.0.0.1:8000/pgd/download?ysqxxid_list=01944D9B7F0000013BEF9D20A977BCB1
    date1 = request.args.get('ysqxxid_list')
    # list = [l[1:-1] for l in date1[1:-1].split(',')]
    list = [i for i in date1.split('@')]
    result = dowonload(list)
    return str(result)


server.run(port=8000, debug=True, host='0.0.0.0')
url = '0.0.0.0:8000/info'
