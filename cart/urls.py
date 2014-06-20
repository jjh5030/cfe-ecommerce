from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('cart.views',
    url(r'^add$', 'add_to_cart'),
    url(r'^view$', 'view_cart', name="view_cart"),

)
