# -*- coding: utf-8 -*-

from django.conf.urls import *

import views

urlpatterns = patterns('',
    (r'^user/list/', views.index),
	(r'^create/$', views.create_accounts),
	(r'^reset_password/', views.reset_password),
	(r'^change_account_status/', views.change_account_status),
	(r'^view_account/', views.view_account),
	(r'^view_history/', views.view_history),
	(r'^add_info/', views.add_info),
	(r'^upload/', views.get_file),
    (r'^version_read/',views.version_read),
)