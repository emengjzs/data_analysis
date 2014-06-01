#-*- coding:utf-8 -*-
#
#   api函数化接口
#   请通过import api使用
#
import urllib2
import urllib
import json
import func
URL                  = 'http://112.124.1.3:8004'        # 主url
Category_URL         = URL + '/api/commodity'           # 商品类别目录url
mobile_phone_index   = 13
mobile_category_name = "Cell Phones & Accessories>Cell Phones>Contract Cell Phones"
cat = ['Cell Phones & Accessories', 'Cell Phones', 'Contract Cell Phones']
page_size            = 28
# img = func.load('commodity_img_url')


def get_category_list():                        # 得到所有商品类别目录 接口1
    category_list = json.loads(urllib.urlopen(Category_URL).read())
    return category_list

category_list = []      # get_category_list()             # 总目录


def get_single_category(i):                     # 得到第i个目录名
    if i == 13:
        return mobile_category_name
    else:
        global category_list
        category_list = get_category_list()
        return category_list[i]['name']


def get_commodity_list(i, page=1, field=[]):    # 得到某个分类目录下的所有商品列表 接口2
    """
    得到某个分类目录下的所有商品列表,图片['img']
    i       目录索引
    page    页索引  
    field   商品json属性，空时默认至少有商品ASIN码和商品名称
    """
    url = Category_URL + "/?"
    name = ['ASIN', 'productInfo.name']
    for f in field:
        if 'productInfo' in f:
            del name[1]
            break
    name.extend(field)
    para = urllib.urlencode({'category_name': get_single_category(i),
                             'page'         : page,
                             'field'        : name
                             })
    commodity_list = json.loads(urllib2.urlopen(url + para).read())
    for c in commodity_list:
        c['img'] = get_low_img(c['ASIN'])
    return commodity_list


def get_all_commodity_list(field=[]):
    """
    得到所有商品信息,图片['img']
    field   商品json属性，空时默认至少有商品ASIN码和商品名称
    """
    print 'FUCK'
    para = ['ASIN', 'productInfo.name']
    para.extend(field)
    commodity_list = advanced_search({'category.0': cat}, field=para)
    #p = 0
    #page = float(page_size)
    #while p <= page:
    #    print 'init progress: %.2f ' % (p / page * 100.0) + '%'
    #    p += 1
    #    commodity_list.extend(get_commodity_list(mobile_phone_index,
    #                                            p,
    #                                            field=field
    #                                            ))
    for c in commodity_list:
        c['img'] = get_low_img(c['ASIN'])
    return commodity_list


def get_commodity_list_size(i):                 # 得到某个分类目录下的所有商品总数 接口3
    url = Category_URL + "/count/?"
    para = urllib.urlencode({'category_name': get_single_category(i)})
    list = json.loads(urllib.urlopen(url + para).read())
    return list['count']


def get_commodity_info(ASIN, field=[]):         # 获取某一个指定ASIN的商品信息 接口4
    '''
    ASIN    商品ASIN码
    field   所需查询的商品json属性，空时默认为全部商品信息
    '''
    url = Category_URL + '/' + ASIN + '/?'
    if field:
        para = urllib.urlencode({'field': field})
    else:
        para = ''
    return json.loads(urllib2.urlopen(url + para).read())


def print_commodity_info(commodity):            # 打印某个商品所有信息
    print json.dumps(commodity, sort_keys=False, indent=4)


def get_commodity_field():                      #没什么作用 接口5
    url = Category_URL + '/field'
    print json.loads(urllib.urlopen(url).read())


def advanced_search(query={}, field=[], page=0):#接口6
    '''
    query   查询语句
    page    页数
    field   所需查询的商品json属性，空时默认为全部商品信息
    '''
    ret = {f: 1 for f in field}
    url = ''.join([URL, '/api/custom/?'])
    # query['stats_info.review_count'] = {'$gt': '19'}
    para = urllib.urlencode({'query': query,
                             'ret'  : str(ret),
                             'page' : page
                             })
    return json.loads(urllib2.urlopen(url + para).read())


def get_low_img(ASIN):
    return 'http://images.amazon.com/images/P/' + ASIN + '.01.LZZZZZZZ.jpg'


def get_img(ASIN):
    """
    得到商品图片url
    """
    url = 'http://ec4.images-amazon.com/images/P/'
    url = url + ASIN + '.01.MAIN._SCRM_.jpg'
    # print urllib2.urlopen(url).headers['Content-Length']
    if int(urllib2.urlopen(url).headers['Content-Length']) < 45:
        return 'http://images.amazon.com/images/P/' + ASIN + '.01.LZZZZZZZ.jpg'
    return url
    #if ASIN in img:
    #    return img[ASIN]
