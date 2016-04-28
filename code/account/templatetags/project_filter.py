# -*- coding:utf-8 -*-

import time
import os
from datetime import timedelta, datetime, date

from django import template
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from core import emotion

from datetime import datetime

register = template.Library()

@register.filter(name='load_termite_dialog')
def load_termite_dialog(name):
	dialog_dir_path = os.path.join(settings.TERMITE_HOME, 'termite/js/dialog', name)
	if not os.path.isdir(dialog_dir_path):
		return ''

	template_path = os.path.join(dialog_dir_path, 'dialog.html')
	src_file = open(template_path, 'rb')
	template_source = src_file.read()
	src_file.close()

	js = '<script type="text/javascript" src="/termite_static/termite/js/dialog/%s/dialog.js"></script>' % name
	
	return '%s\n%s' % (template_source, str(js))


ALL_TEMPLATES_CONTENT = None
@register.filter(name='load_templates')
def load_templates(name):
	global ALL_TEMPLATES_CONTENT
	if not ALL_TEMPLATES_CONTENT:
		templates_file_path = os.path.join(settings.PROJECT_HOME, '../templates/all_merged_templates.html')
		src_file = open(templates_file_path)
		ALL_TEMPLATES_CONTENT = src_file.read()
		src_file.close()

	return ALL_TEMPLATES_CONTENT