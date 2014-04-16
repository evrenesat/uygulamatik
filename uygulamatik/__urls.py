from django.conf.urls import patterns, include, url
from uygulamatik import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
   )

urlpatterns += patterns('',
	url(r'^index/$', 'icerik.views.index'),
	url(r'^geribildirim/$', 'icerik.views.geribildirim'),
	url(r'^birbakista/$', 'icerik.views.birbakista'),
	url(r'^karekod/$', 'icerik.views.karekod'),
	url(r'^kampanyalar/$', 'icerik.views.kampanyalar'),
	url(r'^paylasim/$', 'icerik.views.paylasim'),
	url(r'^iletisim/$', 'icerik.views.iletisim'),

	url(r'^$', 'icerik.views.index'),
)
