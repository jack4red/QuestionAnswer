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


#===============================================================================
# 以下是登录退出功能
#===============================================================================
def login(request):
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user:
			if user.id > 1 : #除admin之外的用户登录则判断有效期与状态
				user_status = UserProfile.objects.get(user_id=user.id).is_active
				if user_status:
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
				return HttpResponseRedirect('/')
		else:			
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
	return HttpResponseRedirect('/account/login/')



def view_account(request):
	return HttpResponseRedirect('/account/login/')

def signup(request):
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		if User.objects.filter(username=username).exists():
			c = RequestContext(request, {
				'error':True,
			})
			return render_to_response('account/signup.html', c)
		else:
			User.objects.create_user(username, 'feature_function@gmail.com', password)
			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)
			return HttpResponseRedirect('/')
	else:
		c = RequestContext(request, {
			})
		return render_to_response('account/signup.html', c)