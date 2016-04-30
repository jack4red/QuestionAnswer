# -*- coding: utf-8 -*-
from django.db.models import signals


from django.db import models
from django.contrib.auth.models import Group, User


#===============================================================================
# 创建消息记录
#===============================================================================
class UserOperationLog(models.Model):
	user_id = models.IntegerField() #记录用户ID
	user_name = models.CharField(max_length=64) #用户名
	operater_id = models.IntegerField() #操作者ID
	operater_name =  models.CharField(max_length=64) #操作者名
	log = models.CharField(max_length=64) #操作
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	
	class Meta(object):
		db_table = 'account_user_operation_log'

#hack: 修改User的属性, 增加一个profile
User.profile = property(lambda u: UserProfile.objects.get(user=u))