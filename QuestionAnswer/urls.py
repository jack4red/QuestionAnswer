from django.conf.urls import patterns, url

from QuestionAnswer import views

urlpatterns = patterns('',
	# /QuestionAnswer/
	url(r'^$', views.IndexView.as_view(), name='index'),
	# /QuestionAnswer/1
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	# /QuestionAnswer/1/view_answer
	url(r'^(?P<question_id>\d+)/view_answer/$', views.view_answer, name='view_answer'),
)
