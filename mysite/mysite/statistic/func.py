__author__ = 'jzs'
#-*- coding:utf-8 -*-
# 实用函数
import json
from datetime import datetime,  date
import re
import cPickle
mobile_phone_index = 13
page_size = 28


def print_info(data):            # 打印某个商品所有信息
    print json.dumps(data, sort_keys=False, indent=4, cls=CJsonEncoder)


def get_star(review):            # 得到评论的评星
    return int(review['star'][0])


def review_rank(review):
    r = get_helpRate(review)
    if r[1] == 0:
        r[1] = 1
    return r[0] * r[0] / r[1]


def get_helpRate(review):       # 得到评论的帮助率
    rate = str(review['helpRate']).replace("\n        ", "")
    r = rate.split("of")
    return [int(r[0]), int(r[1])]


def get_review_date(review):   # 得到评论日期类型
    return datetime.strptime(review['publishTime'],
                             '%Y-%m-%d %H:%M:%S').date()


def get_commodity_name(commodity):
    return commodity['productInfo'][0]['name']


def get_date(data_str):         # 得到日期类型
    return datetime.strptime(data_str,
                             '%Y-%m-%d %H:%M:%S').date()


def get_last_price(c):
    offer_list = sorted(c['offer'], key=lambda x: x['timestamp'], reverse=True)   # sort                          # record if price has changed
    for offer in offer_list:
        for info in offer['info']:
            if info:                                # if has info
                p = get_price(info['price'])
                if p > 0.01:
                    return p
    return 0


def get_price(p_str):
    return float(str(p_str).replace(',', '').replace('$', ''))


def date_to_list(date):
    return [date.year, date.month, date.day]


class CJsonEncoder(json.JSONEncoder):
    """
    date类型转json
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



def get_Res_num(r_str):
    r = re.findall(r'\d{3,4}',r_str)
    if r:
        return int(r[0]) * int(r[1])


def get_battery_num(b_str):
    b_str = b_str.replace(',', '')
    r = re.search(r'\d{3,4}', b_str)
    if r:
        return int(r.group())


def get_screen_num(screen_cpu):
    r = re.search(r'\d\.?\d?\d?', screen_cpu)
    if r:
        return float(r.group())


def get_cpu_num(cpu_str):
    if 'G' in cpu_str or 'g' in cpu_str:
        r = re.search(r'\d\.?\d?\d?', cpu_str)
        if r:
            return float(r.group())
    if 'M' in cpu_str:
        r = re.search(r'\d{2,3}', cpu_str)
        if r:
            return float(r.group()) / 1000.0


def get_rom_num(rom_str):
    if 'GB' in rom_str or 'gb' in rom_str:
        r = re.search(r'\d{1,3}\.?\d?\d?', rom_str)
        if r:
            return float(r.group())
    if 'MB' in rom_str or 'mb' in rom_str:
        r = re.search(r'\d{2,3}', rom_str)
        if r:
            return float(r.group()) / 1000.0

#del del_bad_commodity(c_list):
#    for c in c_list:


def save(name, data):
    f = open('data\\' + name, 'wb')
    cPickle.dump(data, f)
    f.close()


def load(name):
    f = open('data\\' + name, 'rb')
    r = cPickle.load(f)
    f.close()
    return r


def get_rank(f_list, f):
    length = len(f_list)
    for i in range(0, length):
        if f_list[i] > f:
            r = i / float(length)
            return int(r * 100)
    return 99