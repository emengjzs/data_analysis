#-*- coding:utf-8 -*-
__author__ = 'jzs'

import api

c_list = api.get_all_commodity_list(['productInfo.name', 'review.publishTime', 'offer'])


def get_purchase_distribution_analysis():
    """
    购买力人群分布
    返回结果：
    {'count':[数量,...],
     'range':[价格,...]
     'price' [价格,...]
     }
     处于['range'][i]与['range'][i+1]区间的数量为count[i]
     分析结果
     ['price'][0] 低端价位
     ['price'][1] 主流价位
     ['price'][2] 高端价位
    """
    import purchase_distribution
    return purchase_distribution.analysis(c_list)


def get_price_distribution_analysis():
    """
    商品价格分布
    返回结果：
    {'count':[数量,...],
     'range':[价格,...]
     }
     """
    import price_distribution_redef
    return price_distribution_redef.get_price_list(c_list)


def get_brand_list():
    """
    商标列表
    """
    import brand_portion_trend

    return brand_portion_trend.brand_list


def get_current_portion_analysis():
    """
    计算现在各品牌份额
    返回数组[{'brand':品牌，'count':份额数量}, ...]
    """
    import brand_portion_trend

    brand_portion_trend.commodity_list = c_list
    return brand_portion_trend.count_current_portion()


def get_portion_trend_analysis():
    """
    计算现在各品牌份额随时间走势
    s_date 统计开始日期
    返回数组{'date_list' :[[年，月，日] ,...]
            'brand_list':[{'brand':      品牌名
                           'count_list': [数量,...]
                          }
                         ,...]
    """
    import brand_portion_trend

    brand_portion_trend.commodity_list = c_list
    return brand_portion_trend.count_portion_by_time()


def get_sale_analysis():
    """
    总体手机分类每月销售数，不是总评论数，柱状图
    'date_list'
    'count_list'
    'change' 上一月的销售增幅百分比
    """
    from datetime import date
    import func
    start_date = date(2012, 1, 1)
    s_date = date(2012, 1, 1)
    date_list = []
    count_list = []
    from dateutil.relativedelta import relativedelta
    e_date = date(date.today().year, date.today().month, 1)
    while s_date < e_date:
        date_list.append(s_date)
        count_list.append(0)
        s_date = s_date + relativedelta(months=1)
    for c in c_list:
        for r in c['review']:
            date = func.get_review_date(r)
            if date < start_date:
                continue
            else:
                for i in range(len(date_list)):
                    if date_list[i].year == date.year and date_list[i].month == date.month:
                        count_list[i] += 1
                        break
    return {'date_list': [[d.year, d.month] for d in date_list],
            'count_list': count_list,
            'change': round(100 * ((count_list[-1] - count_list[-2]) / float(count_list[-2])), 1)
            }


def test():
    """
    {'count_list': count_list,
            'gap_list': gap_list,
            'num': num
            }
    """
    import  func
    func.print_info(get_purchase_distribution_analysis())
    func.print_info(get_price_distribution_analysis())
    func.print_info(get_sale_analysis())
    func.print_info(get_current_portion_analysis())
    func.print_info(get_portion_trend_analysis())