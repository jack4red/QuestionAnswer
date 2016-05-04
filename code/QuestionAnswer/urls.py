from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from QuestionAnswer import views

urlpatterns = patterns('',
	# /QuestionAnswer/
	url(r'^$', views.index, name='index'),
	url(r'^theme_detail/', views.theme_detail),
	url(r'^question_detail/', views.question_detail),
	url(r'^answer_detail/', views.answer_detail),
	url(r'^add_question/', views.add_question),
)

urlpatterns += staticfiles_urlpatterns()
