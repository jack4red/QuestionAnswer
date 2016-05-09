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

from QuestionAnswer.models import *
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


# @login_required(login_url='/account/login/')
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')


@login_required(login_url='/account/login/')
def view_account(request):
	user_id = request.GET.get('user_id','')
	if not user_id:
		user_id = request.user.id
	user = UserProfile.objects.get(user_id=user_id)
	username = user.user_name
	created_at = user.created_at

	focused_question_ids_list = []
	focused_theme_ids_list = []
	focused_user_ids_list = []
	focused_answer_ids_list = []
	if user.focused_question_ids:
		focused_question_ids_list = user.focused_question_ids.split(',')
	if user.focused_theme_ids:
		focused_theme_ids_list = user.focused_theme_ids.split(',')
	if user.focused_user_ids:
		focused_user_ids_list = user.focused_user_ids.split(',')
	if user.focused_answer_ids:
		focused_answer_ids_list = user.focused_answer_ids.split(',')

	tmp_focused_user_ids_list = UserProfile.objects.get(user_id=request.user.id).focused_user_ids.split(',')
	if str(user_id) in tmp_focused_user_ids_list:
		focused = True
	else:
		focused = False

	question_list = []
	theme_list = []
	user_list = []
	answer_list = []
	for focused_question_id in focused_question_ids_list:
		question_name = Question.objects.get(id=focused_question_id).question_title 
		question_list.append({'question_name':question_name,'question_id':focused_question_id})
	for focused_theme_id in focused_theme_ids_list:
		theme_name = Theme.objects.get(id=focused_theme_id).theme_name 
		theme_list.append({'theme_name':theme_name,'theme_id':focused_theme_id})
	for focused_user_id in focused_user_ids_list:
		user_name = User.objects.get(id=focused_user_id).username 
		user_list.append({'user_name':user_name,'user_id':focused_user_id})
	for focused_answer_id in focused_answer_ids_list:
		answer = Answer.objects.get(id=focused_answer_id)
		answer_text = answer.answer_text 
		question_name = Question.objects.get(id=answer.question_id).question_title
		answer_list.append({'question_name':question_name,'answer_text':answer_text,'answer_id':focused_answer_id})

	c = RequestContext(request, {
		'username':username,
		'user_id':user_id,
		'created_at':created_at,
		'question_list':question_list,
		'theme_list':theme_list,
		'user_list':user_list,
		'answer_list':answer_list,
		'focused':focused,
	})
	return render_to_response('account/accounts.html', c)

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