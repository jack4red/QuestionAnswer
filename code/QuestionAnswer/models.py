# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group, User
from models import *

# Create your models here.

class Question(models.Model): #问题
	owner_theme_ids = models.TextField() #所属话题
	owner_user = models.ForeignKey(User)
	question_text = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'qa_question'

class Answer(models.Model): #答案
	question = models.ForeignKey(Question)
	owner_user = models.ForeignKey(User)
	answer_text = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'qa_answer'

class Comment(models.Model): #评论
	answer = models.ForeignKey(Answer)
	owner_user = models.ForeignKey(User)
	comment_text = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'qa_comment'

class Theme(models.Model): #话题
	name = models.CharField(max_length=100) #名字
	description = models.TextField() #描述

	class Meta(object):
		db_table = 'qa_theme'