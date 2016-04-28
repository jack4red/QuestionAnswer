# -*- coding: utf-8 -*-
from __future__ import division

import time
import urllib
import os
import sys
import random
from PIL import Image

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth
from core.jsonresponse import create_response
from models import *
import corporate_culture
FIRST_NAV_NAME = corporate_culture.CORPORATE_CULTURE_LEADER
SECOND_NAVS = corporate_culture.get_second_navs()

#===============================================================================
# jobs_list : 任务列表
#===============================================================================
@login_required(login_url='/manager/login/')
def corporate_culture_list(request):
	c = RequestContext(request, {
		'jobs':CorporateCulture.objects.all().order_by('-time'),
		'first_nav_name': FIRST_NAV_NAME,
		'second_nav_name': corporate_culture.CORPORATE_CULTURE_LEADER,
		'second_navs': SECOND_NAVS,
	})
	return render_to_response('corporate_culture/corporate_culture_list.html', c)

@login_required(login_url='/manager/login/')
def corporate_culture_create(request):
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_nav_name': corporate_culture.CORPORATE_CULTURE_LEADER,
		'second_navs': SECOND_NAVS,
	})
	return render_to_response('corporate_culture/corporate_culture_create.html', c)


def corporate_culture_ajax(request):
	if request.POST:
		if request.POST['title'] and request.POST['pic'] and request.POST['time']:
			created_time_add_loc = request.POST['time']+' '+time.strftime("%H:%M:%S",time.localtime(time.time()))
			# request.POST['html']=request.POST['html'].decode('gb2312').encode('utf-8')
			if request.POST['news_id']!='':
				CorporateCulture.objects.filter(id=request.POST['news_id']).update(file_url=request.POST['pic'],content=request.POST['html'],title=request.POST['title'],time=created_time_add_loc)
			else:
				CorporateCulture.objects.create(title=request.POST['title'],file_url=request.POST['pic'],content=request.POST['html'],time=created_time_add_loc)
			return HttpResponse('ok')

@login_required(login_url='/manager/login/')
def corporate_culture_delete(request,num):
	try:
		CorporateCulture.objects.get(id=num).delete()
		return HttpResponse('ok')
	except Exception, e:
		return HttpResponse(e)

@login_required(login_url='/manager/login/')
def get_file(request):
	file = request.FILES.get('file',None)
	if file:
		import os,time
		second_dir = time.strftime("%Y_%m_%d_%H_%M_%S")
		saved_dir = '%s/%s/' % (settings.UPLOAD_DIR,second_dir)
		if not os.path.exists(saved_dir):
			os.makedirs(saved_dir)
		saved_path = os.path.join(saved_dir,file.name)
		try:
			saved_file = open(saved_path,'wb')
			saved_file.write(file.read())
			saved_file.close()
			response = create_response(200)
			response.data.saved_path = '/static/upload/%s/%s' % (second_dir,file.name)
		except Exception,e:
			response = create_response(500)
			response.data.errMsg = u'上传路径错误'
	else:
		response = create_response(500)
		response.data.errMsg = u'上传路径错误'
	return response.get_response()

@login_required(login_url='/manager/login/')
def corporate_culture_edit(request,num):
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_nav_name': corporate_culture.CORPORATE_CULTURE_LEADER,
		'second_navs': SECOND_NAVS,
		'news':CorporateCulture.objects.get(id=num),
	})

	return render_to_response('corporate_culture/corporate_culture_create.html', c)