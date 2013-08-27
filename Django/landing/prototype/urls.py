from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'accounts.views.account_subscribe'),
    #url(r'^$', 'morbid.views.index'),

    url(r'^subscribe/$', 'accounts.views.account_subscribe'),
    url(r'^thanks/$', 'accounts.views.account_subscribe_after'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^cRJCoGxGZh/', include(admin.site.urls)),

    # API
    # url(r'^api/feature_analytic_ticker/(?P<analytic_slug>[^/]+)/(?P<ticker_slug>[^/]+)/(?P<feature_id>\d+)/(?P<value>[^/]+)/$', feature_analytic_ticker_resource)
    #url(r'^api/', include('api.urls')),

    # Screen page
    #url(r'^screen/$', 'morbid.views.screen'),

    # Graph
    #url(r'^graph_01/$', 'morbid.views.graph_01'),
)

# Statics (need for gunicorn)
urlpatterns += staticfiles_urlpatterns()
