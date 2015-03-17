from django.conf.urls import patterns, url

from QuestionAnswer import views

urlpatterns = patterns('',
	# /QuestionAnswer/
	url(r'^$', views.index, name='index'),
	# /QuestionAnswer/1
	url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
	# /QuestionAnswer/1/answers
	url(r'^(?P<question_id>\d+)/answers/$', views.answers, name='answers'),
	# /QuestionAnswer/1/write_answer
	url(r'^(?P<question_id>\d+)/write_answer/$', views.write_answer, name='write_answer'),
)
