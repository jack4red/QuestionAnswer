from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from QuestionAnswer import views

urlpatterns = patterns('',
	# /QuestionAnswer/
	url(r'^$', views.index, name='index'),
	url(r'^theme_detail/', views.theme_detail),
	url(r'^(?P<question_id>\d+)/view_answer/$', views.view_answer, name='view_answer'),
	url(r'^new_question/$', views.new_question, name='new_question'),
)

urlpatterns += staticfiles_urlpatterns()
