#-*- coding:utf-8 -*-

import api
import func

from datetime import timedelta, date
"""\
手机品牌份额统计及其随时间走势折线图
"""

mobile_phone_index = 13                                             # 目录号
page_size = api.page_size    # 页数
start_date = date(2011, 1, 1)                                       # 计算开始日期范围

brand_list = ['Samsung', 'HTC', 'Motorola', 'LG', 'Nokia',  'Sony', 'BlackBerry', 'Others']

commodity_list = []
count_list = [0] * len(brand_list)
one_time_count_list = []                                            # 这个时间点之前的所有各品牌评论汇总
per_time_count_list = []                                            # 这个时间点之间的所有各品牌评论汇总
date_list = []                                                      # 日期列表
analysis = False
analysis_2 = False


def count_current_portion():
    """
    计算现在各品牌份额
    返回数组[{'brand':品牌，'count':份额数量}, ...]
    """
    global analysis
    if not analysis:
        for asin in commodity_list:
            commodity = asin

            review_count = len(commodity['review'])
            name = commodity['productInfo'][0]['name']
            '''统计份额'''
            result = False
            for brand in brand_list:
                if brand in name:

                    count_list[brand_list.index(brand)] += review_count
                    result = True
            if not result:
                count_list[-1] += review_count
        analysis = True
    result = [{'brand': brand_list[i], 'count': count_list[i]} for i in range(0, len(brand_list))]
    return result


def count_portion_by_time(s_date=start_date):
    """
    计算现在各品牌份额随时间走势
    s_date 统计开始日期
    返回数组{'date_list' :[日期,...]
            'brand_list':[{'brand':      品牌
                           'count_list': [数量...]
                          }
                         ,...]
    """
    global analysis_2
    if not analysis_2:
        from dateutil.relativedelta import relativedelta
        print "processing..."
        while s_date < date.today():
            one_time_count_list.append([0] * len(brand_list))
            per_time_count_list.append([0] * len(brand_list))
            date_list.append(s_date)
            s_date = s_date + relativedelta(months=1)

        one_time_count_list.append([0] * len(brand_list))
        per_time_count_list.append([0] * len(brand_list))
        date_list.append(date.today())
    return count_portion()

###########################################################################################

# 载入data
def init_commodity_list():
    global commodity_list
    commodity_list = api.get_all_commodity_list(['productInfo.name', 'review.publishTime'])


def get_near_day(c_date):
    for i in range(len(date_list)):
        if c_date <= date_list[i] and ((i <= 0 and c_date > date_list[i] - timedelta(30)) or date_list[i-1] < c_date):
            return i
    return -1


def count_review(brand, commodity):
    for r in commodity['review']:
            d = func.get_review_date(r)
            i = get_near_day(d)
            if i >= 0:
                per_time_count_list[i][brand_list.index(brand)] += 1
            for date in date_list:
                if d <= date:
                    temp = one_time_count_list[date_list.index(date)]
                    temp[brand_list.index(brand)] += 1


def count_portion():

    global analysis_2
    if not analysis_2:
        print "processing..."
        for asin in commodity_list:
            commodity = asin
            # print commodity
            name = commodity['productInfo'][0]['name']
            result = False
            for brand in brand_list:
                if brand in name:
                    result = True
                    count_review(brand, commodity)
            if not result:
                count_review(brand_list[-1], commodity)
        analysis_2 = True

    return {'date_list': [[d.year, d.month, d.day] for d in date_list],
            'brand_list':  [{'brand': brand_list[b],
                             'count_list': [one_time_count_list[i][b] for i in range(len(date_list))]
                            } for b in range(len(brand_list))],
            'increase_rate': [round(100 * ((one_time_count_list[-2][b] - one_time_count_list[-3][b]) /
                                      float(one_time_count_list[-3][b])), 1) for b in range(len(brand_list))]
            }


def draw_portion_trend_graph():
    import matplotlib.pyplot as plt
    plt.figure(figsize=[12, 8])
    ax = plt.gca()
    colors = ['SteelBlue', 'SeaGreen', 'Tomato', 'Black', 'BurlyWood', 'Orchid', 'DarkGray', 'MediumPurple']
    ax.set_color_cycle(colors)
    for b in range(len(brand_list)):
        brand_count_list = [one_time_count_list[i][b] for i in range(len(date_list))]
        plt.plot(date_list, brand_count_list, '-o', label=brand_list[b])
    plt.gcf().autofmt_xdate()                   # 自动调整日期显示的格式
    plt.xlabel('Date')
    plt.ylabel('Portion')
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., fontsize=10)
    plt.show()


def draw_sell_trend_graph():
    import matplotlib.pyplot as plt
    plt.figure(figsize=[12, 8])
    ax = plt.gca()
    colors = ['SteelBlue', 'SeaGreen', 'Tomato', 'Black', 'BurlyWood', 'Orchid', 'DarkGray', 'MediumPurple']
    ax.set_color_cycle(colors)
    for b in range(len(brand_list)):
        brand_count_list = [per_time_count_list[i][b] for i in range(len(date_list))]
        plt.plot(date_list, brand_count_list, '-o', label=brand_list[b])
    plt.gcf().autofmt_xdate()                   # 自动调整日期显示的格式
    plt.xlabel('Date')
    plt.ylabel('Per Sell Count')
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., fontsize=10)
    plt.show()


def draw_pie():
    import matplotlib.pyplot as plt
    '''绘制饼状图'''
    count_current_portion()
    labels = brand_list
    sizes = count_list
    colors = ['lightskyblue', 'PaleGreen', 'Tomato', 'Orchid', 'gold', 'lightcyan', 'DarkGray', 'LemonChiffon']
    explode = (0.05, 0, 0, 0, 0, 0, 0, 0)
    fig = plt.figure(figsize=[9, 8])
    fig.patch.set_facecolor('Gainsboro')
    ax = fig.add_subplot(111)
    pie_wedge_collection = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=False, startangle=90, labeldistance=1.05)
    for pie_wedge in pie_wedge_collection[0]:
        pie_wedge.set_edgecolor('FloralWhite')
    plt.axis('equal')
    plt.title(api.get_single_category(mobile_phone_index) + " portion graph")
    plt.show()

if __name__ == '__main__':
    init_commodity_list()
    func.print_info(count_portion_by_time(start_date))
    #draw_portion_trend_graph()
    #draw_sell_trend_graph()
    draw_pie()
