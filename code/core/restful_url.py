# -*- coding: utf-8 -*-
from django.core.urlresolvers import ResolverMatch, Resolver404
from core import resource as resource_util

class DataObj(object):
	def __init__(self):
		self.pattern = ''

class RestfulURLPattern(object):
	def __init__(self, app_name):
		self.app_name = app_name
		self.is_func_loaded = False
		self.name2func = {}
		self.loaded_file_set = None
		self.regex = DataObj()
		self.callback = None
		self.default_args = []
		self.name = app_name
		self.empty_dict = {}
		self.valid_methods = set(['get', 'post', 'put', 'delete', 'api_get', 'api_post', 'api_put', 'api_delete'])

	def __raise_404(self, path):
		tried = []
		valid_methods = self.valid_methods
		if len(resource_util.APPRESOURCE2CLASS) > 0:
			for app_resource, class_info in resource_util.APPRESOURCE2CLASS.items():
				for key, value in class_info['cls'].__dict__.items():
					if not key in valid_methods:
						continue
					tried.append([{'regex':{'pattern': '^{}:{}'.format(app_resource, key)}}])
		else:
			tried.append([{'regex':{'pattern': 'None'}}])

		raise Resolver404({'tried': tried, 'path' : path})

	def resolve(self, path):
		method = None
		app_resource = None
		func = None
		try:
			items = path.split('/')
			method = items[-1].lower()
			if items[0] == 'api':
				resource = '/'.join(items[1:-1])
				method = 'api_%s' % method
			else:
				resource = '/'.join(items[:-1])

			app_resource = '%s-%s' % (self.app_name, resource)
			class_info = resource_util.APPRESOURCE2CLASS.get(app_resource, None)
			# print '-*-' * 20
			# print 'path: ', path
			# print 'method: ', method
			# print 'app_resource: ', app_resource
			# print '-$-' * 20
			if class_info:
				if not class_info['instance']:
					class_info['instance'] = class_info['cls']
				resource_instance = class_info['instance']
				func = getattr(resource_instance, method, None)
				if func:
					return ResolverMatch(func, (), {}, path)
				else:
					self.__raise_404(path)
			else:
				self.__raise_404(path)
		except:
			context = {
				'path': path,
				'method': method,
				'app_resource': app_resource,
				'func': func,
				'APPRESOURCE2CLASS': resource_util.APPRESOURCE2CLASS
			}
			# notify_message = u"RESTful url2 route failed, context:{}\ncause:\n{}".format(str(context), unicode_full_stack())
			# watchdog_fatal(notify_message, type='URL_ROUTE', noraise=True)
			self.__raise_404(path)


class RestfulUrl(object):
	def __init__(self, app_name):
		self.app_name = app_name
		self.url_patterns = None

	@property
	def urlpatterns(self):
		if not self.url_patterns:
			self.url_patterns = [RestfulURLPattern(self.app_name)]

		return self.url_patterns


def restful_url(app_name):
	return (RestfulUrl(app_name), app_name, '')