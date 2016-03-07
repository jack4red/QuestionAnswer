# -*- coding: utf-8 -*-
"""@package core.middleware
"""
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse, Http404
from account.account_util import get_logined_user_from_token

class AuthorizedUserMiddleware(object):
	"""
	根据请求进行自动登录处理的中间件

	@author chuter
	"""
	def process_request(self, request):

		token = request.REQUEST.get('token', None)
		if token is None:
			return None

		request_host = request.get_host()
		authorized_user = get_logined_user_from_token(token, request_host=request_host)
		if authorized_user is None:
			return None

		auth.login(request, authorized_user)
		if request.path_info.endswith('GET'):
			path_info = request.path_info[:request.path_info.find('GET')]
		else:
			path_info = request.path_info

		return HttpResponseRedirect(path_info)