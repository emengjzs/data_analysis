#-*- coding:utf-8 -*-
import api
import func
import numpy as np

from datetime import timedelta, date
"""
修正评分走势折线图
第n个修正评分 = （1-alpha）* 第n-1个修正评分 + alpha * 第n个平均评分数
"""
mobile_phone_index = 13     # 目录号
page_size = api.page_size   # 查询页数

alpha = 0.3                 # 系数
day_gap = 10                # 时间间隔
min_review_count = 0        # 筛选评论数大于此数的商品

start_avg = 4
start_star = 4

description = [u'评分较为稳定',
               u'最近受到连续好评',
               u'与以前相比，最近获得更好的评价',
               u'与以前相比，最近获得较差的评价, 可能出现质量下降问题']

def get_review_analysis(commodity):
    star_list = []
    date_list = []
    avg_list = []
    avg_date_star_list = []
    if len(commodity['review']) > min_review_count:
        commodity['review'].sort(key=lambda x: x['publishTime'])
        start_date = func.get_review_date(commodity['review'][0]) + timedelta(day_gap)
        star_list.append([])
        date_list.append(start_date)
        for single_review in commodity['review']:
            if start_date >= func.get_review_date(single_review):
                star_list[-1].append(func.get_star(single_review))
            else:
                while start_date < func.get_review_date(single_review):
                    start_date = start_date + timedelta(day_gap)
                star_list.append([func.get_star(single_review)])
                date_list.append(start_date)
        # func.print_info(date_list)
        star_count = 0
        for st in star_list:
            print st
        for n in range(len(date_list)):
            star_count += len(star_list[n])                     # 计算总评论数
            temp_avg = star_count / float(n + 1)                # 计算平均评论数
            dis = len(star_list[n]) - float(temp_avg)           # 计算现评论数与平均评论数之差
            avg_date_star_list.append(np.mean(star_list[n]))    # 计算现平均评分
            if n == 0:
                avg_list.append(round((avg_date_star_list[0] + start_star) / 2.0, 2))
            else:
                avg_list.append(round(avg_list[-1] * (1-alpha) + avg_date_star_list[n] * alpha, 2))
    # avg_star = commodity["stats_info.avg_info"]
    return {'date_list': [[d.year, d.month, d.day] for d in date_list], 'avg_list': avg_list}


def get_commodity(asin):
    return api.get_commodity_info(asin, ['review.star',                # 星级
                                         'review.publishTime',
                                         'productInfo.name',            # 时间
                                         'stats_info.avg_info'])        #


def draw_graph(date_list, avg_list, commodity):
    import matplotlib.pyplot as plt
    plt.plot([date(d[0], d[1], d[2])for d in date_list], avg_list, '-o')
    plt.xlabel(commodity['productInfo'][0]['name'] + '\n current review point:%d' % (avg_list[-1] * 100))
    plt.ylabel('review point')
    ax = plt.gca()
    ax.set_yticks(np.linspace(0, 6, 7))
    plt.gcf().autofmt_xdate()                   # 自动调整日期显示的格式
    plt.show()


