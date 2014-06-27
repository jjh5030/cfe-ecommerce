from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
    }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^products/', include('products.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^contact/', 'contact.views.contact_us', name='contact_us'),
    url(r'^checkout/', 'cart.views.checkout', name='checkout'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'products.views.all_products'),
)
