# -*- coding: utf-8 -*-
from django.db.models import signals


from django.db import models
from django.contrib.auth.models import Group, User


#===============================================================================
# 创建消息记录
#===============================================================================
class UserProfile(models.Model):
	user = models.ForeignKey(User) #记录用户ID
	user_name = models.CharField(max_length=64) #用户名
	focused_question_ids = models.TextField() #关注的问题id
	focused_theme_ids = models.TextField() #关注的话题id
	focused_user_ids = models.TextField() #关注的用户id
	focused_answer_ids = models.TextField() #关注的答案id
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	
	class Meta(object):
		db_table = 'auth_user_profile'

#===============================================================================
# create_profile : 自动创建user profile
#===============================================================================
def create_profile(instance, created, **kwargs):
	if created:
		if instance.username == 'admin':
			return
		if UserProfile.objects.filter(user=instance).count() == 0:
			profile = UserProfile.objects.create(user = instance,user_name = instance.username)
			

signals.post_save.connect(create_profile, sender=User, dispatch_uid = "account.create_profile")