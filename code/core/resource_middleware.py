# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

from core import resource

RESOURCE_NAMES = set(['termite2', 'weixin2', 'stats'])

#===============================================================================
# RestfulUrlMiddleware : 处理request.path_info的middleware
#===============================================================================
class RestfulUrlMiddleware(object):
	def process_request(self, request):
		path_info = request.path_info
		pos = path_info.find('/', 2)
		app = str(path_info[:pos+1])
		if not app in resource.RESTFUL_APP_SET:
			if app in RESOURCE_NAMES:
				data = {
					'path_info': path_info,
					'app': app,
					'resource': resource.RESTFUL_APP_SET
				}
				# watchdog_fatal(str(data), type='RESTFUL_MIDDLEWARE')
			return None

		method = request.META['REQUEST_METHOD']
		if method == 'POST' and '_method' in request.REQUEST:
			_method = request.REQUEST['_method']
			method = _method.upper()

		request.original_path_info = path_info
		if path_info[-1] == '/':
			request.path_info = '%s%s' % (path_info, method)
		else:
			request.path_info = '%s/%s' % (path_info, method)

		# if 'new_weixin' in path_info:
		# 		data = {
		# 			'path_info': path_info,
		# 			'new_path_info': request.path_info,
		# 			'app': app,
		# 			'resource': resource.RESTFUL_APP_SET
		# 		}
		# 		watchdog_info(str(data), type='RESTFUL_MIDDLEWARE')

		return None


#===============================================================================
# ResourceJsMiddleware : 返回resource js文件
#===============================================================================
class ResourceJsMiddleware(object):
	def process_request(self, request):
		if '/resource_js/' == request.path_info:
			from core import resource
			buf = ['ensureNS("W.resource");']
			for _, class_info in resource.APPRESOURCE2CLASS.items():
				buf.append('ensureNS("W.resource");')
				buf.append(class_info['js'])
		
			return HttpResponse('\n'.join(buf), 'text/javascript')


if settings.RESOURCE_LOADED:
	print '[!!!!!!!!!!!!!!!!!!!!!!] already loaded'
else:
	for resource_module in settings.RESOURCES:
		print '[resource middleware] load ', resource
		exec('import %s' % resource_module)
		settings.RESOURCE_LOADED = True