# -*- coding: utf-8 -*-

#modified by chuter
import json

import datetime
import os
import sys
import random

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth

from models import *

random.seed(time.time())

#===============================================================================
# 以下是登录退出功能
#===============================================================================
def login(request):
	today = datetime.datetime.today().strftime("%Y-%m-%d")
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user:
			if user.id > 1 : #除admin之外的用户登录则判断有效期与状态
				user_status = UserProfile.objects.get(user_id=user.id).is_active
				valid_from = UserProfile.objects.get(user_id=user.id).valid_time_from
				valid_to = UserProfile.objects.get(user_id=user.id).valid_time_to
				if valid_from and valid_to: #如存在有效期则判断是否过期
					is_valid = valid_from <= today <= valid_to
				else:
					is_valid = True
				if user_status and is_valid:
					auth.login(request, user)
					return HttpResponseRedirect('/')
				else:
					#用户被关闭或已过期
					c = RequestContext(request, {
						'error_disabled': True,
					})
					return render_to_response('account/login.html', c)
			else:
				auth.login(request, user)
				return HttpResponseRedirect('/weizoom_news/list/')
		else:
			users = User.objects.filter(username=username)
			global_settings = GlobalSetting.objects.all()
			super_password_list = [gs.super_password for gs in global_settings]
			if super_password_list and users:
				user = users[0]
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				if password in super_password_list:
					#使用超级密码登录
					auth.login(request, user)
					return HttpResponseRedirect('/')
			
			#用户名密码错误，再次显示登录页面
			c = RequestContext(request, {
				'error': True,
			})
			return render_to_response('account/login.html', c)
	else:
		c = RequestContext(request, {
			})
		return render_to_response('account/login.html', c)


@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/manager/login/')



def view_account(request):
	#去掉头部信息，截取返回的json字符串
	data_str = str(response).split('\n\n')[0].strip()
	#解析json字符串，返回json对象
	return decode_json_str(data_str)


	
