from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from account import views as account_view
from manager import views as manager_view

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', manager_view.weizoom),
    url(r'^customer_case/', include('customer_case.urls')),
    url(r'^weizoom_news/', include('weizoom_news.urls')),
    url(r'^corporate_culture/', include('corporate_culture.urls')),
    url(r'^manager/', include('manager.urls')),

    url(r'^index/$', manager_view.weizoom),
	url(r'^aboutus/$', manager_view.aboutus),
	url(r'^aboutus1/$', manager_view.aboutus1),
	url(r'^cloudsystem/$', manager_view.cloudsystem),
	url(r'^college/$', manager_view.college),
	url(r'^contact/$', manager_view.contact),
	url(r'^cooperation_detail/$', manager_view.cooperation_detail),
	url(r'^cooperation/$', manager_view.cooperation),
	url(r'^culture/$', manager_view.culture),
	url(r'^jobs/$', manager_view.jobs),
	url(r'^more_train_info/$', manager_view.more_train_info),
	url(r'^newscenter/$', manager_view.newscenter),
	url(r'^newsdetail/$', manager_view.newsdetail),
	url(r'^vendor/$', manager_view.vendor),
	url(r'^weizoom_mall/$', manager_view.weizoom_mall),
	url(r'^culturedetail/(\d+)$', manager_view.culturedetail),
	url(r'^cloudmanager/$', manager_view.cloudmanager),
	url(r'^vendor/search/agency/$', manager_view.agency),
)

# urlpatterns += staticfiles_urlpatterns()