#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from statistic.commodity_analysis import Commodity
import statistic.api
import statistic.category_analysis

def commodity_list(request):
    commodity = statistic.api.get_all_commodity_list()

    return render_to_response('commodity_list.html', locals())

def brand_list(request):
    return render_to_response('brand_list.html', locals())

def commodity_info(request):
    c = Commodity(request.GET.get('ASIN'))
    name = c.name() #商品名
    info = c.get_info() 
    ASIN = request.GET.get('ASIN')
    brand = c.brand() #商标名
    img = c.get_img()
    sta = c.get_star_analysis() #星级分布
    features = c.get_features()
    fr = c.get_feature_rank()
    fs = c.get_feature_score()   #手机配置总评分
    nfc = c.get_near_feature_commodity()
    sa = c.get_sales_analysis()  #评论总数走势分析
    pa = c.get_prices_analysis()  #价格分析
    kwa = c.get_key_words_analysis()   #词频分析
    mra = c.get_modified_review_analysis()   #修正评分走势  
    return render_to_response('commodity_info.html', locals())

def category(request):
    pda = statistic.category_analysis.get_purchase_distribution_analysis();
    prda = statistic.category_analysis.get_price_distribution_analysis();
    return render_to_response('category.html', locals())

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def index(request):
    return render_to_response('index.html', locals())
#    return HttpResponse('index.html')
