from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from QuestionAnswer import views

urlpatterns = patterns('',
	# /QuestionAnswer/
	url(r'^$', views.index, name='index'),
	# /QuestionAnswer/1
	# url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	# /QuestionAnswer/1/view_answer
	url(r'^(?P<question_id>\d+)/view_answer/$', views.view_answer, name='view_answer'),
	# /QuestionAnswer/new_question
	url(r'^new_question/$', views.new_question, name='new_question'),
)

urlpatterns += staticfiles_urlpatterns()
