#-*- coding:utf-8 -*-
__author__ = 'jzs'
import api
import func


def get_price():
    price_list =[]
    change_list = []
    date_list = []
    c_list = api.get_all_commodity_list(['offer'])
    num = 0
    for c in c_list:
        p_list = []
        d_list = []
        c['offer'].sort(key=lambda x: x['timestamp'])   # sort                          # record if price has changed
        for offer in c['offer']:
            for info in offer['info']:
                if info:                                # if has info
                    p = func.get_price(info['price'])
                    if p_list:
                        if p - p_list[-1] < 0:
                            print "down! " + str(p_list[-1]) + " \t" + str(p) + " \t" + str(p - p_list[-1]) + "  \t" + str(
                                func.get_date(info['timestamp']) - d_list[-1])
                            price_list.append(int(p_list[-1] / 100))
                            change_list.append((p - p_list[-1]) / p_list[-1])
                            date_list.append((func.get_date(info['timestamp']) - d_list[-1]).days)
                            num += 1
                        #if p - p_list[-1] > 0:
                        #    print "up! " + str(p_list[-1]) + "\t" + str(p) + "\t" + str(p - p_list[-1]) + " \t" + str(
                        #        func.get_date(info['timestamp']) - d_list[-1])
                        #    num += 1
                    p_list.append(p)
                    d_list.append(func.get_date(info['timestamp']))

                    break
    print num
    import matplotlib
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(price_list, date_list)
    plt.show( )
    import numpy as np
    n, bins = np.histogram(date_list, 20)
    import purchase_distribution
    purchase_distribution.draw_graph(n,bins)
