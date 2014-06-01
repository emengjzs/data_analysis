from django.conf.urls import patterns, include, url
from mysite.views import commodity_list,brand_list,hours_ahead,index,commodity_info,category
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    ('^commodity_list/$', commodity_list),
    ('^brand_list/$', brand_list),
    (r'^commodity/$', commodity_info),
    (r'^category/$', category),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
    (r'^index/$', index),
    url(r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
)
 
