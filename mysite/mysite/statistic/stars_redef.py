#-*- coding:utf-8 -*-
from __future__ import division
# import api
# import matplotlib.pyplot as plt; plt.rcdefaults()
# import numpy as np
# import matplotlib.pyplot as plt
# from datetime import datetime
import string
#星级评分统计


def get_review_star_analysis(p):
    #获得具体商品
    name = p['productInfo'][0]['name']
    print '========'+name+'========'

    #HelpRate分析
    rate_list = []
        
    review_count=-1
    rate_count=-1
    for review in p['review']:
        review_count+=1
        if review['helpRate']!='0 of 0':
            rates=review['helpRate'].strip('\n').strip(' ').split(' of ')
            a=string.atoi(rates[0])
            b=string.atoi(rates[1])

            rate_count+=1
            rate = []
            rate.append(review['star'])
            rate.append(a)
            rate.append(b)
            rate.append(review_count)
            rate.append(rate_count)
            
            rate_list.append(rate)
            #print str(a)+' '+str(b)

        

    stats_info=p['stats_info']

    #获取星级统计
    print '--------'+'star_info'+'--------'
    count = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for rate in rate_list:
        if rate[0]=='1.0 out of 5 stars':
            count[0][0]+=rate[1]
            count[1][0]+=rate[2]
        elif rate[0]=='2.0 out of 5 stars':
            count[0][1]+=rate[1]
            count[1][1]+=rate[2]
        elif rate[0]=='3.0 out of 5 stars':
            count[0][2]+=rate[1]
            count[1][2]+=rate[2]
        elif rate[0]=='4.0 out of 5 stars':
            count[0][3]+=rate[1]
            count[1][3]+=rate[2]
        elif rate[0]=='5.0 out of 5 stars':
            count[0][4]+=rate[1]
            count[1][4]+=rate[2]
            
    for review in p['review']:
        if review['star']=='1.0 out of 5 stars':
            count[2][0]+=1
        elif review['star']=='2.0 out of 5 stars':
            count[2][1]+=1
        elif review['star']=='3.0 out of 5 stars':
            count[2][2]+=1
        elif review['star']=='4.0 out of 5 stars':
            count[2][3]+=1
        elif review['star']=='5.0 out of 5 stars':
            count[2][4]+=1
    
    stars=stats_info['star_info']
    print '一星：'+str(count[2][0])+' '+str(stars['1'])+' '+str(count[0][0])+'/'+str(count[1][0])
    print '二星：'+str(count[2][1])+' '+str(stars['2'])+' '+str(count[0][1])+'/'+str(count[1][1])
    print '三星：'+str(count[2][2])+' '+str(stars['3'])+' '+str(count[0][2])+'/'+str(count[1][2])
    print '四星：'+str(count[2][3])+' '+str(stars['4'])+' '+str(count[0][3])+'/'+str(count[1][3])
    print '五星：'+str(count[2][4])+' '+str(stars['5'])+' '+str(count[0][4])+'/'+str(count[1][4])
    print '平均：'+str(stats_info['avg_info'])
    
    # x_pos = (count[2][0],count[2][1],count[2][2],count[2][3],count[2][4])

    err = []
    i = 0
    while i<5:
        if count[1][i]!=0:
            err.append(count[2][i]*(1-count[0][i]/count[1][i]))
        else:
            err.append(0)
        i+=1
    
    # error=(err[0],err[1],err[2],err[3],err[4])
    
    return {'stars': [count[2][i] for i in range(0,5)],
            'error': err}
