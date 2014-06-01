#-*- coding:utf-8 -*-
from __future__ import division
import func
import numpy as np
num = 0
def get_price_list(c_list):
    """
    "
    """
    price_list = []
    global num
    for c in c_list:
        p = func.get_last_price(c)
        if p > 0 :
            price_list.append(p)
            num += 1
        # func.print_info(p['offer'])
    n, bins = np.histogram(price_list, 10)
    p_list = np.array(price_list)
    mean = p_list.mean()
    std = p_list.std()
    up = mean + std
    down = mean - std
    pce = [down, mean, up]
    pce = [round(r, -1) for r in pce]
    #import purchase_distribution
    #purchase_distribution.draw_graph(n, bins)
    count_list = list(n)
    gap_list = list(bins)
    return {'count': count_list,
            'range': [round(p, 2) for p in gap_list],
            'num': num,
            'price': pce
            }

   #获取所有商品价格
   #                                               # 每件商品
   # p['offer'].sort(key=lambda x: x['timestamp'], reverse=True)     # 价格从新到旧排序
   # result = False
   # for offer in p['offer']:                                        # 找最新的非零价格
   #     if offer['info']:                                           # 一个时间点有信息
   #         for info in offer['info']:                              # 对此时间点的所有非零价格记录
   #             price = func.get_price(info['price'])
   #             #print info['price']
   #             if price > 0.01:
   #                 result = True
   #                 price_list.append(price)
   #         #if result:
   #         #    break
   #