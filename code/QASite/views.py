# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import time
import os
import json


@login_required(login_url='/account/login/')
def upload_rich_text_image(request):
	"""
	上传富文本图片
	返回参数：{
            "state" : stateInfo,
            "url" : fullName,
            "title" : 新文件名,
            "original" : 原始文件名,
            "type" : fileType,
            "size" : fileSize
        }
	:param request:
	:return: HttpResponse(JSON格式)
	"""
	action = request.POST.get('action','')
	file = request.FILES.get('upfile',None)
	return_dict = {}
	if file:
		filename = file.name
		second_dir = time.strftime("%Y_%m_%d_%H_%M_%S")
		saved_dir = '%s/%s/%s' % (settings.UPLOAD_DIR,second_dir,action)
		if not os.path.exists(saved_dir):
			os.makedirs(saved_dir)
		saved_path = os.path.join(saved_dir,filename)
		try:
			saved_file = open(saved_path,'wb')
			saved_file.write(file.read())
			saved_file.close()
			return_dict['state'] = u'SUCCESS'
			return_dict['url'] = '/static/upload/%s/%s/%s' % (second_dir,action,filename)
			return_dict['title'] = filename
			return_dict['original'] = filename
			return_dict['type'] = filename[filename.rindex('.')+1:]
			return_dict['size'] = file.size
		except:
			print_stack_trace()
			return_dict['state'] = 'ERROR_WRITE_CONTENT'
	else:
		return_dict['state'] = u'没有文件被上传'
	return HttpResponse(json.JSONEncoder().encode(return_dict))