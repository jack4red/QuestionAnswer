# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group, User
from models import *

# Create your models here.

class Question(models.Model): #问题
	owner_theme_ids = models.TextField() #所属话题
	owner_user = models.ForeignKey(User)
	question_title = models.CharField(max_length=100)
	question_text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'qa_question'

class Answer(models.Model): #答案
	question = models.ForeignKey(Question)
	owner_user = models.ForeignKey(User)
	up_owner_user_ids = models.TextField() #赞同人id
	down_owner_user_ids = models.TextField() #反对人id
	answer_text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'qa_answer'

class Comment(models.Model): #评论
	answer = models.ForeignKey(Answer)
	owner_user_name = models.CharField(max_length=100)
	comment_text = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'qa_comment'

class Theme(models.Model): #话题
	theme_name = models.CharField(max_length=100) #名字
	description = models.TextField() #描述

	class Meta(object):
		db_table = 'qa_theme'


#################################
# 关系表
#################################

# 0:u'关注问题'
# 1:u'关注话题'
# 2:u'关注答案'
# 3:u'回答问题'
# 4:u'评论答案'
# 5:u'点赞答案'
# 6:u'反对答案'
# 7:u'话题下有新问题'
# 8:u'关注了用户'
class NewsToUser(models.Model):
	action_user = models.ForeignKey(User)
	actioned_user = models.CharField(max_length=100,null=True)
	question = models.ForeignKey(Question,null=True)
	answer = models.ForeignKey(Answer,null=True)
	comment = models.ForeignKey(Comment,null=True)
	theme = models.ForeignKey(Theme,null=True)
	action_type = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'newstouser'