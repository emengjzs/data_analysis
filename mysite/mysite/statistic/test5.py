#-*- coding:utf-8 -*-
import func
import api
import word_frequency
"""
key_words_dict = func.load('key_words')
commodity_list = api.get_all_commodity_list(field=['ASIN', 'review.content', 'productInfo.name'])

for c in commodity_list:
    #if c['ASIN'] in key_words_dict and len(c['review']) >= 30:
    #    print "==========================="
    #    func.print_info(key_words_dict[c['ASIN']])
    if c['ASIN'] not in key_words_dict and 20 <= len(c['review']) < 30:
        top_list = word_frequency.get_review_sentence_analysis(c)
        key_words_dict[c['ASIN']] = top_list
    func.save('key_words', key_words_dict)
"""
"""
all_string = open('keywords', 'r').read()
one_key_words = []
str_split = all_string.split('\tWord: ')
del str_split[0]
length = len(str_split)
x = 0
while x+16 <= length:
    one_key_words.append(str_split[x:x+16])
    x += 16
data_list = []
for words in one_key_words:
    d_list = []
    for word in words:
        word_split = word.split('  \tTF-IDF: ')
        d_list.append([word_split[0], round(float(word_split[1].replace('\n', '')), 5)])
    data_list.append(d_list)


j = 0
for i in range(len(data_list)):
    while len(commodity_list[j]['review']) < 30:
        j += 1
    key_words_dict[commodity_list[j]['ASIN']] = data_list[i]
    j += 1
func.save('key_words', key_words_dict)
"""