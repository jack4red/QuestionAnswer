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
	url(r'^add_answer/', views.add_answer),
	url(r'^add_comment/', views.add_comment),
	url(r'^add_theme/', views.add_theme),
	url(r'^focuse_action/', views.focuse_action),
	url(r'^search_action/', views.search_action),
	url(r'^collect_answer/', views.collect_answer),
	url(r'^up_or_down_answer/', views.up_or_down_answer),
)

urlpatterns += staticfiles_urlpatterns()
