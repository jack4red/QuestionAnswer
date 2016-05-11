# -*- coding:utf-8 -*-

from django import template
import re
register = template.Library()
@register.filter(name='pictostr')
def pictostr(val):
	# val = val.replace(' ','').replace('	',''),replace('\n','')
	try:
		val = val.encode("utf-8")
		val = re.sub(r'<\s*img\s+[^>]*?src\s*=\s*(\'|\")(.*?)\1[^>]*?\/?\s*>', '[图片]', val)
		return val
	except Exception, e:
		return val

# <\s*img\s+[^>]*?src\s*=\s*(\'|\")(.*?)\\1[^>]*?\/?\s*>