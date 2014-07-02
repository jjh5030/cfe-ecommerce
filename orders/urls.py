from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('orders.views',
       url(r'^$', 'view_orders', name="orders"),

)
