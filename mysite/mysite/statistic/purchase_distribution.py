__author__ = 'jzs'
#-*- coding:utf-8 -*-
'''
购买力人群分布直方图
因数据不全，过滤掉价格为0的商品
'''
import func

import numpy as np


gap = 50
prices_list = [gap * i for i in range(1000 / gap)]
count_list = [0 for i in range(len(prices_list))]

def analysis(commodity_list):
    prices_list = [gap * i for i in range(1000 / gap)]
    count_list = [0 for i in range(len(prices_list))]
    """
    购买力人群分布
    返回结果：
    {'count':[数量,...],
     'range':[价格,...]
     }
     处于['range'][i]与['range'][i+1]区间的数量为count[i]
    """
    data = []
    clear_list()
    for c in commodity_list:
        c['offer'].sort(key=lambda x: x['timestamp'])
        #api.print_commodity_info(c['offer'])
        for r in c['review']:
            r_time = func.get_review_date(r)
            price = get_price(c, r_time)
            if price > 0:
                data.append(price)
            #count(price)
    #p_list = np.array(data)
    #mean = p_list.mean()
    #std = p_list.std()
    #up = mean + std
    #down = mean - std
    #print down, mean, up
    n, bins = np.histogram(data, 15)
    c_list = list(n)[:]
    c_list.sort(reverse=True)
    max_three_list = c_list[0:3]
    max_three_list[2] = c_list[3]
    # print max_three_list
    range_list = [round((bins[list(n)[:].index(c)] +
                  bins[list(n)[:].index(c) + 1]) / 2, -1)
                  for c in max_three_list]
    range_list.sort()
    print range_list
    #draw_graph(n, bins)
    return {'count': list(n), 'range': list(bins), 'price': range_list}


def clear_list():
    for n in range(len(count_list)):
        count_list[n] = 0


# 仅测试用，画图没有用到此数组
def count(price):
    if price <= 0.1:
        return
    for i in range(len(prices_list) - 1):
        if prices_list[i] <= price < prices_list[i+1]:
            count_list[i] += 1
            return
    count_list[-1] += 1


def get_price(commodity, date):
    #print str(date) + "==="
    for i in range(1, len(commodity['offer']) + 1):
        if func.get_date(commodity['offer'][-i]['timestamp']) <= date:
            price_list = []
            for one_price in commodity['offer'][-i]['info']:
                price = float(one_price['price'])
                if price > 0:
                    price_list.append(price)
            if len(price_list) == 0:
                continue
            else:
                return np.mean(price_list)
    return 0


def draw_graph(n, bins):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import matplotlib.path as path
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    fig, ax = plt.subplots()
    top = bottom + n
    XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T
    barpath = path.Path.make_compound_path_from_polys(XY)
    patch = patches.PathPatch(barpath)
    ax.add_patch(patch)
    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max() + 50)
    plt.xlabel("Price")
    plt.ylabel("Count")
    plt.show()



