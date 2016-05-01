# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
import django.utils.timezone as timezone
from django.db.models import Q,Sum

from models import *
from account.models import *

# Create your views here.
ACTION_TYPE=(
	u'关注问题',
	u'关注话题',
	u'关注答案',
	u'回答问题',
	u'评论答案',
	u'点赞答案',
	u'反对答案',
	)

@login_required(login_url='/account/login/')
def index(request):
	if request.POST:
		pass
	else:
		latest_news = collect_news(request.user.id,0)

		c = RequestContext(request, {
			'latest_news':latest_news,
		})
		return render_to_response('index.html', c)

def collect_news(user_id,page,count=8):
	cur_user = UserProfile.objects.get(user_id=user_id)
	
	list_question_ids = cur_user.focused_question_ids.split(',') if cur_user.focused_question_ids else []
	list_theme_ids = cur_user.focused_theme_ids.split(',') if cur_user.focused_theme_ids else []
	list_user_ids = cur_user.focused_user_ids.split(',') if cur_user.focused_user_ids else []
	list_answer_ids = cur_user.focused_answer_ids.split(',') if cur_user.focused_answer_ids else []
	list_user_ids.append(user_id)

	news = NewsToUser.objects.filter(Q(action_user_id__in=list_user_ids)|Q(question_id__in=list_question_ids)|Q(answer_id__in=list_answer_ids)|Q(theme_id__in=list_theme_ids)).order_by('-created_at')[page*count:(page+1)*count]
	news = {new.id:new for new in news}

	latest_news = []
	for new in news:
		new_obj = {}
		if news[new].theme_id:
			new_obj['theme_id']=news[new].theme_id
			new_obj['theme_name']=Theme.objects.get(id=news[new].theme_id).theme_name

		if news[new].comment_id:
			new_obj['comment_id']=news[new].comment_id
			new_obj['comment_text']=Comment.objects.get(id=news[new].comment_id).comment_text

		if news[new].question_id:
			new_obj['question_id']=news[new].question_id
			new_q = Question.objects.get(id=news[new].question_id)
			new_obj['question_title']=new_q.question_title
			new_obj['question_text']=new_q.question_text

		if news[new].answer_id:
			new_obj['answer_id']=news[new].answer_id
			new_obj['answer_text']=Answer.objects.get(id=news[new].answer_id).answer_text

		if news[new].actioned_user:
			new_obj['actioned_user']=news[new].actioned_user

		new_obj['action_user']=news[new].action_user
		new_obj['action_type']=ACTION_TYPE[news[new].action_type]
		new_obj['created_at']=news[new].created_at
		
		latest_news.append(new_obj)
		

	return latest_news

@login_required(login_url='/account/login/')
def theme_detail(request):
	theme_id = request.GET.get('theme_id','1')
	theme = Theme.objects.get(id=theme_id)
	c = RequestContext(request, {
			'theme_name':theme.theme_name,
			'description':theme.description,
		})
	return render_to_response('theme_detail.html', c)


@login_required(login_url='/account/login/')
def view_answer(request, question_id):
	q = get_object_or_404(Question, pk = question_id)
	answer_text = request.POST['answer_text']

	q.answer_set.create(answer_text=answer_text, pub_date=timezone.now())

	return HttpResponseRedirect(reverse('QuestionAnswer:detail', 
					args=(question_id,)))
	

def new_question(request):
	qtext = request.POST['question_text']

	q = Question(question_text=qtext, pub_date=timezone.now())
	q.save()

	return HttpResponseRedirect(reverse('QuestionAnswer:index'))
					
	

