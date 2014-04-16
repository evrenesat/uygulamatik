from django.conf.urls import *
from django.shortcuts import redirect
from django.views.static import serve
from umatik.admin_views import get_defaults
from uygulamatik import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^9oo/(?P<code>\w+)$', 'qurl.views.redirect_id'),
    url(r'^app/default.js', 'umatik.admin_views.get_defaults'),
    url(r"^admin/change_password$", "umatik.admin_views.change_password", name='change_password'),
    url(r"^admin/change_info$", "umatik.admin_views.change_info", name='change_info'),
    url(r'^admin/home/$', 'umatik.admin_views.home', name='home_admin'),
    url(r'^admin/$', 'umatik.admin_views.home_user', name='home_user'),
    url(r'^admin/user_registration/$', 'umatik.admin_views.user_registration'),
    url(r"^admin/application_details/(?P<id>\d+)$", "umatik.admin_views.application_details"),
    url(r'^admin/harita/$', 'umatik.admin_views.map'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/get_app_map$', "umatik.admin_views.get_app_map"),
    url(r'^admin/right_click_context', 'umatik.admin_views.right_click_context'),
    url(r'^admin/get_node_form$', 'umatik.admin_views.get_node_form'),
    url(r'^admin/add_node$', 'umatik.admin_views.add_node'),
    url(r'^admin/update_node$', 'umatik.admin_views.update_node'),
    url(r'^admin/delete_node/(?P<id>\d+)$', 'umatik.admin_views.delete_node'),
    url(r'^admin/get_nodes$', 'umatik.admin_views.get_nodes'),
    url(r'^admin/get_node_update_form/(?P<id>\d+)$', 'umatik.admin_views.get_node_update_form'),
    url(r'^admin/get_store_list$', 'umatik.admin_views.get_store_list'),
    url(r'^admin/get_exhibitor_list$', 'umatik.admin_views.get_exhibitor_list'),
    url(r'^admin/get_icon/(?P<id>\d+)/$', 'umatik.admin_views.get_icon'),
    url(r'^admin/get_neighbours$', 'umatik.admin_views.get_neighbours'),
    url(r'^admin/add_neighbour/(?P<frm>\d+)/(?P<to>\d+)$', 'umatik.admin_views.add_neighbour'),
    url(r'^payment/free/$', "umatik.paymentVies.freePaymentView"),
    url(r'^payment/main/$', "umatik.paymentVies.mainPaymentView"),
    url(r'^aso/main/(?P<appid>\d+)/$', 'at_shop_order.views.orderMain'),
    url(r'^api2/appid_from_domain/(?P<subdomain>\w+)/$', 'umatik.views.appid_from_domain'),
    url(r'^getappid/$', 'umatik.views.getappid'),
    url(r'^aso/list/(?P<appid>\d+)/(?P<status>\d+)/$', 'at_shop_order.views.orderList'),
    url(r'^$', lambda r: redirect('umatik.admin_views.home_user')),
    (r'^localeurl/', include('localeurl.urls')),
)

#urlpatterns += patterns('store.views',
#    url(r'^iletisim/$', 'iletisim'),
#    url(r'^paylasim/$', 'paylasim'),
#    url(r'^kampanyalar/$', 'kampanyalar'),
#    url(r'^geribildirim/$', 'geribildirim'),
#    url(r'^karekod/$', 'karekod'),
#    url(r'^birbakista/$', 'birbakista'),
#    url(r'^neredeyim/$', 'neredeyim'),
#    url(r'^index/$', 'site_index'),
#    url(r'^$', 'site_index'),
#)

from django.views.decorators.cache import never_cache

static_view = never_cache(serve)
if settings.DEVELOPMENT_MODE:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', static_view, {'document_root': settings.MEDIA_ROOT}),
                            url(r'^static/(?P<path>.*)$', static_view, {'document_root': settings.STATIC_ROOT}),

                            url(r'^app/(?P<path>.*)$', static_view,
                                {'document_root': '%s/client/www/' % settings.BASEDIR}),

                            url(r'^apps/(?P<path>.*)$', static_view,
                                {'document_root': '%s/client/apppackages/' % settings.BASEDIR}),
    )

urlpatterns += patterns('',

                        url(r'^api1/(?P<appid>\d+)/', include('umatik.urls')),
                        # url(r'^$', 'umatik.views.main'),

)

