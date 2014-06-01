from django.db import models
import statistic.api
import json
# Create your models here.
def get_phone_list():
    return statistic.api.get_commodity_list(13, 7)

def get_commodity_info(ASIN):
    return statistic.api.get_commodity_info(ASIN)

def get_a():
    a={'name': 'Year 1800','data': [20,20,20,20,20]}
    return a
