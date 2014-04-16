__author__ = 'Evren Esat Ozkan'
from django.conf.urls import *


urlpatterns = patterns('umatik.views',
                       url(r'get_all_records/$', 'get_all_records'),
                       url(r'get_image_list/$', 'get_image_list'),
                       url(r'pack_image_list/$', 'pack_image_list'),
                       url(r'save_client_error/$', 'save_client_error'),
                       url(r'save_feedback/$', 'save_feedback'),
                       # url(r'save_order/$', 'save_order'),
                       url(r'map_graph/$', 'get_map_graph'),
                       url(r'get_css/$', 'get_theme_css'),
                       url(r'get_css_for_web/$', 'get_theme_css_for_web'),
                       url(r'get_version/$', 'get_version'),
                       url(r'gettext/(?P<lang>.*)/$', 'gettext'),
                       url(r'settext/(?P<lang>.*)/$', 'settext'),

)

urlpatterns += patterns('at_shop_order.views',
                       url(r'save_order/$', 'save_order'),

)
