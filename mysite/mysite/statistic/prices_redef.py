#-*- coding:utf-8 -*-
from __future__ import division
# import api
import func
import numpy as np
#import matplotlib.pyplot as plt
from datetime import date
# import time

#价格走势及分布


def analyse(p):
    #获得具体商品
    name = p['productInfo'][0]['name']
    print '========'+name+'========'

    #具体商品分析
    date_list = []
    min_list = []
    max_list = []
    avg_list = []
    count_list = []
    # 时间升序排列
    p['offer'].sort(key=lambda x: x['timestamp'])
    # func.print_info(p['offer'])
    for offer in p['offer']:
        one_date = func.get_date(offer['timestamp'])
        pri_list = [float(str(info['price']).replace(',', '').replace('$', '')) for info in offer['info']]
        if not pri_list == []:
            #分析商品价格走势
            max_pri = max(pri_list)
            min_pri = min(pri_list)
            avg_pri = round(np.mean(pri_list), 2)
            count = len(pri_list)
            if count >= 0 and avg_pri > 0.0001:
                if len(date_list) > 0 and one_date == date_list[-1]:
                    min_list[-1] = min(min_list[-1], min_pri)
                    max_list[-1] = max(max_list[-1], max_list)
                    avg_list[-1] = (avg_list[-1] * count_list[-1] + sum(pri_list)) / float(count + count_list[-1])
                    count_list[-1] += count
                else:
                    date_list.append(one_date)
                    print str(one_date)+'\t'+str(max_pri)+'\t'+str(min_pri)+'\t'+str(avg_pri)+' '+str(count)
                    max_list.append(max_pri)
                    min_list.append(min_pri)
                    avg_list.append(avg_pri)
                    count_list.append(count)
    increase_rate = 0
    desciption = u''
    if not date_list == []:
        date_list.append(date.today())
        max_list.append(max_list[-1])
        min_list.append(min_list[-1])
        avg_list.append(avg_list[-1])
        for i in range(1, len(date_list)):
            if avg_list[-i] - avg_list[-i-1] != 0:
                increase_rate = 100 * ((avg_list[-i] - avg_list[-i-1]) / float(avg_list[-i-1]))
                increase_rate = round(increase_rate, 1)
                break
        price_dic = func.load('price_list')
        rank = func.get_rank(price_dic, avg_list[-1])
        if rank <= 25:
            desciption += u'该手机价格低于' + str(100-rank) + u'%的手机，为低价位。\n'
        elif rank <= 75:
            desciption += u'该手机价格高于' + str(rank) + u'%的手机，为主流价位。\n'
        else:
            desciption += u'该手机价格高于' + str(rank) + u'%的手机，为高价位。\n'
    else:
        desciption += u'该手机没有价格信息。'
    print desciption
    return {'date_list': [[d.year, d.month, d.day] for d in date_list],
            'max_list': max_list,
            'min_list': min_list,
            'avg_list': avg_list,
            'increase_rate': increase_rate,
            'description': desciption
            }

