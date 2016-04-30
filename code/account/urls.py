# -*- coding: utf-8 -*-

from django.conf.urls import *

import views

urlpatterns = patterns('',
	(r'^view_account/', views.view_account),
	(r'^login/', views.login),
	(r'^logout/', views.logout),
	(r'^signup/', views.signup),
)