__author__ = 'jzs'
from  datetime import  date
import func
#data = func.load('feature_score_list')
#func.print_info(data)
import api
key_words_dic = func.load('key_words')
dic = {'3':4, 'y':2}
n = 0
print len(key_words_dic.items())
for (asin, kw) in key_words_dic.items():
    for (a, k) in key_words_dic.items():
        if a != asin:
            num = 0
            for word in kw:
                for w in k:
                    if word[0] == w[0]:
                        num += 1
            if num >= 5:
                n += 1
                print 'Find!'
                break
                #print asin, a
                #print kw
                #print k
print n