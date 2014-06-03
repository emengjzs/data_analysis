import api
import random
import cPickle
import func
import cStringIO
"""
import api
c_list = api.get_all_commodity_list(['review.timestamp'])
r_list = [len(x['review']) for x in c_list]
r_list.sort(reverse=True)
r_set = list(set(r_list))
r_set.sort(reverse=True)
count_list = [0] * len(r_set)
for r in r_list:
    count_list[r_set.index(r)] += 1
del c_list, r_list
print r_set
rank = sum(count_list[0:r_set.index(0)]) + 1
print rank
"""
class A:
    a = 1
    def __init__(self):
        return
A1 = A()
A1.a = 2
A2 = A()
print A2.a
        


"""
index = 13
page = 2
n = 0
page = input("page\n")
n = input("no\n")
c_list = api.get_commodity_list(index, page, ['ASIN',
                                              'productInfo.name',
                                              'stats_info.keywords'
                                 #'review.content'
                                 ])
api.print_commodity_info(c_list[n])

i = 0
img = func.load('commodity_img_url')
print len(img)
s_date = func.load('feature_score_list')
#for page in range(1, 28):
#    commodity_list = api.get_commodity_list(13, page, ['ASIN', 'productInfo.name', 'review.star'])
for n in range(1,len(s_date)):
    #time.sleep(random.randint(5, 10))
    #api.get_commodity_img(c['ASIN'])
    c = s_date[-n]
    if c[1] not in img:
        print api.get_commodity_info(c[1], ['productInfo.name'])['productInfo'][0]['name']
        img_url = raw_input("url: ")
        if img_url == 'exit':
            exit()
        f = open('commodity_img_url', 'wb')
        img[c[1]] = img_url
        cPickle.dump(img, f)
    print i
    i += 1
f.close()
"""
