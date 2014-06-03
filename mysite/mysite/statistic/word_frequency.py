#-*- coding:utf-8 -*-
from __future__ import division, unicode_literals
__author__ = 'jzs'

import func
import math


"""
评论词频基于整个分类统计的TF-IDF方法统计分析
过滤常用词及商品名称中出现的词汇
"""

mobile_phone_index = 13                                            # 目录编号
top_num = 15                                                       # 每个商品选出词数
min_review_num = 0                                                 # 筛选评论数大于此数的商品


################ TF-IDF 统计函数 start ############################
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

count = 0

def tfidf(word, blob, bloblist):
    global count
    count += 1
    print count
    return tf(word, blob) * idf(word, bloblist)

################ TF-IDF 统计函数 end ############################


blob_list = []
review_dict = []
load_data = False
# 测试用，实际上并不需要人工去除高频副词
#words_list = ['a', 'an', 'the', 'for', 'they', 'me', 'i', 'am', 'it', 'to',
#              'in', 'for', 'and', 'or','is', 'was', "it's", 'too', 'you',
#              'are', 'were', 'of', 'this', 'that', 'with', 'these',
#              'have', 'but', 'get', 'out', 'go', 'my', 'not', 'can', 'has',
#              'will', 'if', 'so', 'as', 'be']

key_words_dict = func.load('key_words')

def get_data():
    import cPickle
    import api
    from textblob import TextBlob
    blob_dict = []
    try:
        f = open('review_data', 'rb')
        blob_dict = cPickle.load(f)
        f.close()
    except IOError, e:
        for each_page in range(1, api.page_size):
            print 'prepare for the data: %.2f ' % ((each_page + 1) / 28 * 100.0) + '%'
            c_list = api.get_commodity_list(mobile_phone_index, each_page, ['review.content'])
            for p in c_list:
                if len(p['review']) > 1:    # 需要去除没有评论的商品
                    review_text = " ".join([r['content'].lower() for r in p['review']])
                    tb = TextBlob(review_text)
                    blob_dict.append(tb)
        f = open('review_data', 'wb')
        cPickle.dump(blob_dict, f)
        f.close()
    return blob_dict




def get_commodity(ASIN):
    import api
    return api.get_commodity_info(ASIN, ['ASIN', 'review.publishTime', 'productInfo.name'])


def get_review_sentence_analysis(c):
    if c['ASIN'] in key_words_dict:
        return key_words_dict[c['ASIN']]
    from textblob import TextBlob
    global blob_list
    if len(blob_list) == 0:
        blob_list = get_data()
    print c['productInfo'][0]['name'], len(c['review'])
    top_list = []
    text = " ".join([r['content'].lower() for r in c['review']])
    tb = TextBlob(text)
    w_list = list(set(tb.words))
    scores = {word: tfidf(word, tb, blob_list) for word in w_list if word.isalpha()}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    n = 0
    for word, score in sorted_words:
        if word not in c['productInfo'][0]['name'].lower() and '.' not in word and ',' not in word:
            #and word not in words:
            print "\tWord: {}  \tTF-IDF: {}".format(word, round(score, 5))
            top_list.append([word, round(score, 5)])
            # print top_list
            n += 1
            if n > top_num:
                break
    return top_list


def get_near_keywords_commodity(asin, top_list):
    import api
    a_list = []
    for (a, k) in key_words_dict.items():
        if a != asin:
            num = 0
            for w in k:
                for word in top_list:
                    if word[0] == w[0]:
                        num += 1
                        break
            if num > 0:
                a_list.append([a, num])
    a_list.sort(key=lambda x: x[1], reverse=True)
    a_list = a_list[0: min(3, len(a_list))]
    return [{'ASIN': a[0],
              'name': api.get_commodity_info(a[0], ['productInfo.name'])['productInfo'][0]['name'],
              'img': api.get_low_img(a[0])
             } for a in a_list]


def draw_graph(top_list):
    import matplotlib.pyplot as plt
    plt.bar(range(len(top_list)), [word[1] for word in top_list], align='center', figure=[6, 5])
    plt.xticks(range(len(top_list)), [word[0] for word in top_list])
    plt.xlabel("Word")
    plt.ylabel("TF-IDF")
    #plt.title(c['productInfo'][0]['name'])
    plt.show()


