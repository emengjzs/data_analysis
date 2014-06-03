#-*- coding:utf-8 -*-
__author__ = 'jzs'

import numpy as np

import func
import api


def get_brand_commodity_list(brand_name, field=[]):
    """
    根据商标名返回商品列表
    """
    field.extend(['ASIN', 'productInfo', 'review.publishTime'])
    clist = api.advanced_search({'category.0': api.cat,
                                 'productInfo.brand.name': brand_name},
                                field)
    if brand_name == 'Sony':
        clist.extend(api.advanced_search({'category.0': api.cat,
                                          'productInfo.brand.name': 'Sony Ericsson'},
                                         field))
    clist.sort(key=lambda x: len(x['review']), reverse=True)
    for c in clist:
        c['img'] = api.get_low_img(c['ASIN'])
    return clist


# 品牌分析
class Brand:
    name = ''
    c_list = []

    def __init__(self, brand_name):
        self.name = brand_name
        self.c_list = get_brand_commodity_list(brand_name, ['stats_info.avg_info', 'review.star', 'review.publishTime'])

    def get_sales_analysis(self):
        """
        销量分析
        """
        import brand_portion_trend

        brand_portion_trend.init_commodity_list()
        brand_portion_trend.count_portion_by_time()
        b = brand_portion_trend.brand_list.index(self.name)
        return {'date_list': [[d.year, d.month, d.day] for d in brand_portion_trend.date_list],
                'count_list': [brand_portion_trend.one_time_count_list[i][b]
                               for i in range(len(brand_portion_trend.date_list))]
                }

    def get_hot_commodity(self):
        """
        给出该品牌五大热门手机
        评论数最多， 且在今年仍有评论的手机
        """



    def get_stars_analysis(self):
        """
        评分分析
        """
        avg_star_list = []
        star_list = [0, 0, 0, 0, 0]
        for c in self.c_list:
            avg_star_list.append(float(c['stats_info']['avg_info']))
            for r in c['review']:
                star_list[func.get_star(r) - 1] += 1
        print star_list
        n, bins = np.histogram(avg_star_list, 5)
        return {'count': list(n), 'range': list(bins)}

    def get_prices_analysis(self):
        """
        价格分布分析
        """
        import price_distribution_redef

        return price_distribution_redef.get_price_list(self.c_list)


def test():
    clist = get_brand_commodity_list('Samsung')
    for c in clist:
        print len(c['review'])
    b = Brand('Samsung')
    func.print_info(b.get_sales_analysis())
    func.print_info(b.get_stars_analysis())
