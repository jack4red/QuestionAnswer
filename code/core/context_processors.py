# -*- coding: utf-8 -*-

from weapp import export
from weapp.order import weapp_export as mall_export

def first_navs(request):
	"""
	根据request.path_info获取对应的first navs
	"""
	result = {}
	result['first_navs'] = export.FIRST_NAVS
	return result

def weapp_first_navs(request):
	"""
	根据request.path_info获取对应的first navs
	"""
	result = {}
	result['weapp_first_navs'] = mall_export.FIRST_NAVS
	return result
