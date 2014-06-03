#-*- coding:utf-8 -*-
from __future__ import division
import func
#import api
#import numpy as np
# import matplotlib.pyplot as plt
from datetime import date
from dateutil.relativedelta import relativedelta


#销量走势分析
def sell_count(p):
    #获得具体商品
    name = p['productInfo'][0]['name']
    print '========'+name+'========'
    p['review'].sort(key=lambda x: x['publishTime'])
    review_list = [func.get_review_date(r) for r in p['review']]
    func.print_info(review_list)
    date_list = []
    count_list = []
    if review_list:
        s_date = date(review_list[0].year, review_list[0].month, 1)
        date_list.append(s_date)
        count_list.append(0)
    for d in review_list:
        if date_list[-1].year == d.year and date_list[-1].month == d.month:
            count_list[-1] += 1
        else:
            while True:
                s_date = s_date + relativedelta(months=1)
                #date_list.append(s_date)
                #count_list.append(0)
                if s_date.year == d.year and s_date.month == d.month:
                    count_list.append(0)
                    count_list[-1] += 1
                    date_list.append(s_date)
                    break
    sum_review_list = [sum(count_list[0:(n+1)]) for n in range(len(count_list))]
    import func
    r_dict = func.load('review_list')
    rank = sum(r_dict['count_list'][0:r_dict['r_set'].index(len(p['review']))])+1
    # print date_list

    # 动态描述
    description = u''
    if review_list:
        last_days = date.today() - review_list[-1]
        if last_days.days >= 30:
            if last_days.days < 90:
                description += u'该手机已超过' + str(last_days.days) + u'天没有增加新的评论。\n'
            elif last_days.days < 360:
                description += u'该手机已超过' + str(int(last_days.days / 30)) + u'月没有增加新的评论。\n'
            else:
                description += u'该手机已超过' + str(int(last_days.days / 360)) + u'年没有增加新的评论, 可能已退市。\n'
        else:
            description += u'该手机在最近' + str(last_days.days) + u'天有新的评论\n'

    increase_rate = 0
    if len(count_list) >= 2:
        increase_rate = round(100 * ((count_list[-1] - count_list[-2]) / float(count_list[-2])), 1)
    print description
    return {'date_list': [[d.year, d.month] for d in date_list],
            'count_list': sum_review_list,
            'rank': rank,
            'increase_rate': increase_rate,
            'description': description}

def test():

    import api
    c_list = api.get_all_commodity_list(['review.timestamp'])
    r_list = [len(x['review']) for x in c_list]
    r_list.sort(reverse=True)
    r_set = list(set(r_list))
    r_set.sort(reverse=True)
    count_list = [0] * len(r_set)
    for r in r_list:
        count_list[r_set.index(r)] += 1
    import func
    dict = {}
    dict['r_set'] = r_set
    dict['count_list'] = count_list
    func.save('review_list', dict)
    del c_list, r_list

    import func
    r_dict = func.load('review_list')
    print r_dict
    rank = sum(r_dict['count_list'][0:r_dict['r_set'].index(100)])+1
    print rank
