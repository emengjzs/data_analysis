__author__ = 'jzs'
#-*- coding:utf-8 -*-
import api
import func
from commodity_analysis import Commodity
# 数据预处理脚本，请勿执行


def run():
    commodity_list = api.get_all_commodity_list(field=['productInfo', 'ASIN'])
    cpu_list = []
    b_list = []
    s_list = []
    r_list = []
    for c in commodity_list:
        co = Commodity(c['ASIN'])
        co.c_data = c
        para = co.get_features()
        rank = co.get_feature_rank()
        if len(rank) == 5:
            b_list.append([co.get_feature_score(), c['ASIN']])
            #print para
        #print co.description()
        #print para
        n = func.get_cpu_num(para['CPU'])
        if n:
            cpu_list.append(n)
        b = func.get_battery_num(para['Battery'])
        if b:
            b_list.append(b)
        s = func.get_screen_num(para['Screen'])
        if s:
            s_list.append(s)
        r = func.get_Res_num(para['Res'])
        if r:
            r_list.append(r)
    cpu_list.sort()
    b_list.sort()
    s_list.sort()
    r_list.sort()
    print len(cpu_list), len(b_list), len(r_list)
    func.save('feature_score_list', b_list)
    func.save('cpu_list', cpu_list)
    func.save('res_list', r_list)
    func.save('screen_list', s_list)


def run2():
    key_words_dict = {}
    import word_frequency

    commodity_list = api.get_all_commodity_list(field=['ASIN', 'review', 'productInfo.name'])
    for c in commodity_list:
        if c['ASIN'] not in key_words_dict and len(c['review']) >= 30:
            top_list = word_frequency.get_review_sentence_analysis(c)
            key_words_dict[c['ASIN']] = top_list
    import func
    func.save('words_list',key_words_dict)
