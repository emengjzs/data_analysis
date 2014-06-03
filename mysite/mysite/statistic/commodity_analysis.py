#-*- coding:utf-8 -*-
__author__ = 'jzs'
import re
import numpy as np
import api
import func


# 手机配置汇总数据文件名
feature_list = ['rom_list', 'res_list', 'cpu_list', 'battery_list', 'screen_list']
feature_name = ['ROM', 'Res', 'CPU', 'Battery', 'Screen']
feature_fun = [func.get_rom_num, func.get_Res_num, func.get_cpu_num,
               func.get_battery_num, func.get_screen_num]
para_text = ['OS', 'Screen', 'RAM', 'CPU', 'Res', 'Battery', 'ROM']
para_tran = {'OS': u'操作系统', 'Screen': u'屏幕大小', 'RAM': u'内存', 'CPU': u'处理器', 'Res': u'屏幕分辨率',
             'Battery': u'电池容量', 'ROM': u'储存空间'}
# num = 0
review_url = r'http://www.amazon.com/product-reviews'

class Commodity:
    c_data = {}
    feature_rank = {}

    def __init__(self, ASIN):
        #self.c_data = {}
        self.c_data = api.get_commodity_info(ASIN)
        # func.print_info(self.c_data)
        self.feature_rank = {}

    def get_info(self):
        """
        返回商品全部信息
        """
        return self.c_data

    def get_modified_review_analysis(self):
        """
        修正评分走势
        返回{'date_list': 日期数组, 'avg_list': 评分数组}
        """
        import modified_review_point

        return modified_review_point.get_review_analysis(self.c_data)

    def get_key_words_analysis(self):
        """
        词频分析
        """
        import word_frequency

        return word_frequency.get_review_sentence_analysis(self.c_data)


    def get_near_keywords_commodity(self, top_list):
        """
        参数top_list 为get_key_words_analysis（）的返回结果
        得到具有与此手机相同关键词的商品，最多三个，可能没有！！！
        字典
        'ASIN'
        'name' 商品名
        'img' 商品图片url
        其它信息请用api通过ASIN再获取
        """
        import word_frequency
        return word_frequency.get_near_keywords_commodity(self.name(), top_list)

    def get_features(self):
        """
        得到手机配置参数（string类型，未转为量化数字）
        OS 操作系统
        Screen 屏幕大小
        RAM 内存
        CPU 主频
        Res 屏幕分辨率
        Battery 电池容量
        ROM 储存空间大小
        ['ROM', '16GB','87'],...
        """
        para = []
        des = self.description()
        os = re.search(r'([Aa]ndroid(\s?\d\.\d(\.\d)?))' +
                       #r'|Android' +
                       r'|([Ww]indows\s?[Pp]hone\s?\d\.?\d?)' +
                       r'|([Bb]lackBerry\sOS\s\d(\.\d)?)' +
                       r'|[Ss]ymbian', des)
        if not os:
            os = re.search(r'[Aa]ndroid\s?', des)
        Screen = re.search(r'\d\.?\d?\d?[\n-]inch', des)
        RAM = re.search(r'((\d\s?[Gg][Bb])|(\d\d\d\s?MB))\s?[a-z]*\s?(RAM|ram)', des)
        CPU = re.search(r'((\d(\.\d\d?)?(\s)?[Gg])|(\d\d\d\s?M))[Hh]z', des)
        Res = re.search(r'\d{3,4}\s?[xX*]\s?\d{3,4}', des)
        Battery = re.search(r'\d,?\d{2,3}\s?mAh', des)
        ROM = re.search(r'\d{1,3}\s?[MG]B', self.name())
        if not ROM:
            ROM = re.search(
                r'((\d\s?[Gg][Bb])|(\d\d\d\s?MB))\s?[a-z]*\s?(ROM|rom|[Mm]emory|(SD\s?[Cc]ard)|(([Ss]torage|data) capabilit(y|ies)))',
                des)
        para.extend([os, Screen, RAM, CPU, Res, Battery, ROM])
        para_dict = {}
        for i in range(0, len(para_text)):
            if para[i]:
                para_dict[para_text[i]] = para[i].group()
            else:
                para_dict[para_text[i]] = 'Unknown'
        for i in range(len(feature_name)):
            if para_dict[feature_name[i]] != 'Unknown':
                f_list = func.load(feature_list[i])
                fuc = feature_fun[i]
                self.feature_rank[feature_name[i]] = func.get_rank(f_list, fuc(para_dict[feature_name[i]]))
                #if len(rank) >= 4:
            #    num += 1
        return [[para_tran[para], para_dict[para], self.feature_rank.get(para)] for para in para_text if
                para_dict[para] != 'Unknown']

    def get_feature_rank(self):
        """
        得到配置排名
        'ROM'
        'Res'     '
        'CPU'
        'Battery'
        'Screen'
        例如若['ROM'] = 87 则表示ROM配置高于约87%的手机
        """
        if self.feature_rank == {}:
            self.get_features()
        f_list = self.feature_rank.items()
        return {para_tran[f[0]]: f[1] for f in f_list}

    def get_feature_score(self):
        """
        得到手机配置评价系数
        eg: 488
        返回int
        """
        if self.feature_rank == {}:
            self.get_features()
        if self.feature_rank == {}:
            return 0
        return int(np.mean(self.feature_rank.values()) * 5)

    def description(self):
        """
        返回商品描述
        """
        r = self.c_data['productInfo'][0].get('productDescription')
        if r:
            return r
        else:
            return ""


    def name(self):
        """
        返回商品名
        """
        r = self.c_data['productInfo'][0].get('name')
        if r:
            return r
        else:
            return ""

    def ASIN(self):
        return self.c_data['ASIN']

    def brand(self):
        return self.c_data['productInfo'][0]['brand']['name']

    def get_prices_analysis(self):
        """
        价格分析：价格走势与价格分布
        返回结果
        {'date_list': [[年， 月， 日] , ...],
         'max_list': 最大价格列表,
         'min_list': 最小价格列表,
         'avg_list': 平均价格列表
            }
        """
        import prices_redef

        return prices_redef.analyse(self.c_data)

    def get_star_analysis(self):
        """

        """
        import stars_redef

        return stars_redef.get_review_star_analysis(self.c_data)

    def get_sales_analysis(self):
        """
        评论总数走势分析
        返回结果：
        {'date_list': [[年, 月] , ...],
         'count_list': 数量列表，对应日期之前的评论总和}
        """
        import sales_redef

        return sales_redef.sell_count(self.c_data)

    def get_img(self):
        """
        得到商品图片url
        """
        return api.get_img(self.c_data['ASIN'])

    def get_near_feature_commodity(self):
        """
        得到与此手机配置相近的推荐商品
        字典
        'ASIN'
        'name' 商品名
        'img' 商品图片url
        其它信息请用api通过ASIN再获取
        """
        score_data = func.load('feature_score_list')
        score = self.get_feature_score()
        i = 3
        n_list = []
        s = 0
        import random
        while len(n_list) < 3:
            for d in score_data:
                if s == 0 and score == d[0] and d[1] != self.c_data['ASIN']:
                    n_list.append([d[1], api.get_commodity_info(d[1], ['productInfo.name'])['productInfo'][0].get('name')])
                    print d[0]
                    s = -1
                    continue
                if 1 <= abs(score - d[0]) <= i and d[1] != self.c_data['ASIN'] and d[1] not in n_list:
                    name = api.get_commodity_info(d[1], ['productInfo.name'])['productInfo'][0].get('name')
                    sp = str(name).split(',')[0]
                    r = True
                    for n in n_list:
                        if sp == n[1].split(',')[0]:
                            r = False
                            if random.random() > 0.45:
                                n[0] = d[1]
                                n[1] = name
                            break
                    if r:
                        print d[0]
                        n_list.append([d[1], name])
                    else:
                        continue
            i += 2
        near_asin_list = random.sample(n_list, 3)
        # c = api.get_commodity_info(near_asin, ['productInfo.name'])
        return [{'ASIN': near_asin[0],
                 'name':  near_asin[1],
                 'img': api.get_low_img(near_asin[0]),
                 } for near_asin in near_asin_list]

    def get_hot_review(self):
        """获取热门评论前10条
        [{"star": 1,
          "helpRate": "",
          "publishTime": "",
          "summary": "",
          "content": "",
          "consumer": "",
          "profileUrl": ""
          "isSubjective" Ture/False 此評論是否可能過於主观
          "polarity"    评论感情值范围[-1, 1]负，负面感情，正，正面感情
         }, {}...],
        """
        self.c_data['review'].sort(cmp=lambda x, y: cmp(func.review_rank(x), func.review_rank(y)), reverse=True)
        r_list = self.c_data['review']
        i = 0
        l = 0
        re_list = []
        for r in r_list:
            if l >= 10:
                break
            if r['content'] == '' and i < 4:
                i += 1
                l += 1
                r['content'] = r['summary'] + ' See more details in ' + review_url + '/'+self.ASIN()
                re_list.append(r)
            elif r['content'] != '':
                re_list.append(r)
                l += 1

        from textblob import TextBlob
        for r in re_list:
            tb = TextBlob(r['content'])
            sentiment = tb.sentiment
            r['polarity'] = round(sentiment[0],2)
            if sentiment[1] >= 0.75:
                r['isSubjective'] = True
            else:
                r['isSubjective'] = False
        return re_list


# 测试用
num = 0


def test():
    print "Fuck you!"
    for i in range(2, 3):
        print "Fuck you!"
        c_list = api.get_commodity_list(13, i, ['review'])
        for c in c_list:
            #c = c_list[19]
            cm = Commodity(c['ASIN'])
            func.print_info(cm.get_features())
            func.print_info(cm.name())
            print cm.get_feature_rank()
            print cm.get_feature_score()
            print "------------------------------------"


def test2():
    c = Commodity('B005SLHL1W')
    print c.get_img()
    # print c.c_data['productInfo'][0]['feature']
    print c.get_sales_analysis()
    print c.get_prices_analysis()
    print c.get_star_analysis()

    func.print_info(c.get_features())
    print c.get_feature_rank()
    print c.get_feature_score()
    print c.get_near_feature_commodity()

    top_list = c.get_key_words_analysis()
    print top_list
    print c.get_near_keywords_commodity(top_list)
    print c.get_modified_review_analysis()
    func.print_info(c.get_hot_review())


