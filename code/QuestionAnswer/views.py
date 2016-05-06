# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
from django.db.models import Q,Sum
from core.jsonresponse import create_response

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
	u'话题下有新问题',
	u'关注了用户',
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
	try:
		theme_id = request.GET.get('theme_id','1')
		theme = Theme.objects.get(id=theme_id)
		c = RequestContext(request, {
				'theme_name':theme.theme_name,
				'description':theme.description,
			})
	except Exception, e:
		c = RequestContext(request, {
				'error_message':True,
			})
	return render_to_response('theme_detail.html', c)

@login_required(login_url='/account/login/')
def question_detail(request):
	if request.POST:
		pass
	else:
		question_id = request.GET.get('question_id','1')
		question = Question.objects.get(id=question_id)
		answers = Answer.objects.filter(question_id=question_id)
		answers = {answer.id:answer for answer in answers}
		answer_list = []
		for answer in answers:
			answer_obj = {}
			answer_obj['id'] = answer
			answer_obj['owner_user_id'] = answers[answer].owner_user_id
			answer_obj['owner_user_name'] = User.objects.get(id=answers[answer].owner_user_id).username
			answer_obj['up_owner_user_ids_num'] = len(answers[answer].up_owner_user_ids.split(','))
			answer_obj['down_owner_user_ids_num'] = len(answers[answer].down_owner_user_ids.split(','))
			answer_obj['answer_text'] = answers[answer].answer_text
			answer_obj['created_at'] = answers[answer].created_at
			answer_list.append(answer_obj)

		theme_ids = question.owner_theme_ids.split(',')
		theme_names = []
		for theme_id in theme_ids:
			theme_names.append(Theme.objects.get(id=theme_id).theme_name)

		owner_user_name = User.objects.get(id=question.owner_user_id).username

		c = RequestContext(request, {
				'question_title':question.question_title,
				'question_text':question.question_text,
				'created_at':question.created_at,
				'question_owner_user_id':question.owner_user_id,
				'question_owner_user_name':owner_user_name,
				'theme_names':theme_names,
				'answers':answer_list,
			})
		return render_to_response('question_detail.html', c)

@login_required(login_url='/account/login/')
def answer_detail(request):
	if request.POST:
		pass
	else:
		answer_id = request.GET.get('answer_id','1')
		answer = Answer.objects.get(id=answer_id)
		question = Question.objects.get(id=answer.question_id)
		comments = Comment.objects.filter(answer_id=answer_id).order_by('-created_at')
		owner_user =User.objects.get(id=answer.owner_user_id)

		up_owner_user_ids_num = len(answer.up_owner_user_ids.split(','))
		down_owner_user_ids_num = len(answer.down_owner_user_ids.split(','))

		comments = [{'comment_user_name':comment.owner_user_name,'comment_text':comment.comment_text} for comment in comments]

		c = RequestContext(request, {
				'question_title':question.question_title,
				'question_text':question.question_text,
				'created_at':answer.created_at,
				'answer_text':answer.answer_text,
				'answer_user_name':owner_user.username,
				'up_owner_user_ids_num':up_owner_user_ids_num,
				'down_owner_user_ids_num':down_owner_user_ids_num,
				'comments':comments,
			})
		return render_to_response('answer_detail.html', c)
	
@login_required(login_url='/account/login/')
def add_question(request):
	if request.POST:
		question_title = request.POST.get('question_title','')
		description = request.POST.get('description','')
		belone_theme = request.POST.get('belone_theme','')
		user_id = request.user.id

		New_Q = Question.objects.create(owner_theme_ids=belone_theme,owner_user_id=user_id,question_title=question_title,question_text=description)

		user = UserProfile.objects.get(user_id=user_id)
		focused_question_ids_list = user.focused_question_ids.split(',')
		focused_question_ids_list.append(str(New_Q.id))
		user.focused_question_ids = ','.join(focused_question_ids_list)
		user.save()
		belone_theme_list = belone_theme.split(',')
		for theme in belone_theme_list:
			NewsToUser.objects.create(action_user_id=user_id,question_id=New_Q.id,theme_id=theme,action_type=7)

		response = create_response(200)
		response.data.question_id=New_Q.id
		return response.get_response()
	else:
		c = RequestContext(request, {
				'username':request.user,
				'user_id':request.user.id,
			})
		return render_to_response('add_question.html', c)
					
@login_required(login_url='/account/login/')
def add_answer(request):
	if request.POST:
		question_id = request.POST.get('question_id')
		user_id = request.user.id
		answer_text = request.POST.get('answer_text')

		new_A = Answer.objects.create(question_id=question_id,answer_text=answer_text)
		NewsToUser.objects.create(action_user_id=user_id,answer_id=new_A.id,question_id=question_id,action_type=3)

		response = create_response(200)
		response.data.answer_id=new_A.id
		return response.get_response
	else:
		pass

@login_required(login_url='/account/login/')
def add_comment(request):
	if request.POST:
		answer_id = request.POST.get('answer_id')
		owner_user_name = request.user
		comment_text = request.POST.get('comment_text')
		Comment.objects.create(answer_id=answer_id,owner_user_name=owner_user_name,comment_text=comment_text)

		response = create_response(200)
		return response.get_response
	else:
		pass

@login_required(login_url='/account/login/')
def focuse_action(request):
	user_id = request.user.id
	if request.POST:
		action_type = request.POST.get('action_type','')
		if action_type:
			if action_type == 'theme':
				theme_id = request.POST.get('theme_id')

				user = UserProfile.objects.get(user_id=user_id)
				focused_theme_ids_list = user.focused_theme_ids.split(',')
				if not theme_id in focused_theme_ids_list:
					focused_theme_ids_list.append(theme_id)
					NewsToUser.objects.create(action_user_id=user_id,theme_id=theme_id,action_type=1)
				else:
					focused_theme_ids_list.remove(theme_id)
				user.focused_theme_ids = ','.join(focused_theme_ids_list)
				user.save()


			elif action_type == 'question':
				question_id = request.POST.get('question_id')

				user = UserProfile.objects.get(user_id=user_id)
				focused_question_ids_list = user.focused_question_ids.split(',')
				if not theme_id in focused_question_ids_list:
					focused_question_ids_list.append(question_id)
					NewsToUser.objects.create(action_user_id=user_id,question_id=question_id,action_type=0)
				else:
					focused_question_ids_list.remove(question_id)
				user.focused_question_ids = ','.join(focused_question_ids_list)
				user.save()

			elif action_type == 'user':
				actioned_user_id = request.POST.get('actioned_user_id')

				user = UserProfile.objects.get(user_id=user_id)
				focused_user_ids_list = user.focused_user_ids.split(',')
				if not actioned_user_id in focused_user_ids_list:
					focused_user_ids_list.append(actioned_user_id)
					NewsToUser.objects.create(action_user_id=user_id,actioned_user_id=actioned_user_id,action_type=8)
				else:
					focused_user_ids_list.remove(actioned_user_id)
				user.focused_user_ids = ','.join(focused_user_ids_list)
				user.save()

			elif action_type == 'answer':
				answer_id = request.POST.get('answer_id')

				user = UserProfile.objects.get(user_id=user_id)
				focused_answer_ids_list = user.focused_answer_ids.split(',')
				if not answer_id in focused_answer_ids_list:
					focused_answer_ids_list.append(answer_id)
				user.focused_answer_ids = ','.join(focused_answer_ids_list)
				user.save()

				NewsToUser.objects.create(action_user_id=user_id,answer_id=answer_id,action_type=2)
			else:
				pass
		response = create_response(200)
		return response.get_response()

@login_required(login_url='/account/login/')
def up_or_down_answer(request):
	if request.POST:
		answer_id = request.POST.get('answer_id')
		user_id = request.user.id
		action_type = request.POST.get('action_type')

		answer = Answer.objects.get(id=answer_id)
		up_owner_user_ids_list = answer.up_owner_user_ids.split(',')
		down_owner_user_ids_list = answer.down_owner_user_ids.split(',')

		if action_type == 'up':
			if not user_id in up_owner_user_ids_list:
				up_owner_user_ids_list.append(user_id)
			if user_id in down_owner_user_ids_list:
				down_owner_user_ids_list.remove(user_id)
			NewsToUser.objects.create(action_user_id=user_id,answer_id=answer_id,action_type=5)

		if action_type == 'down':
			if not user_id in down_owner_user_ids_list:
				down_owner_user_ids_list.append(user_id)
			if user_id in up_owner_user_ids_list:
				up_owner_user_ids_list.remove(user_id)
			NewsToUser.objects.create(action_user_id=user_id,answer_id=answer_id,action_type=6)

		answer.up_owner_user_ids = ','.join(up_owner_user_ids_list)
		answer.down_owner_user_ids = ','.join(down_owner_user_ids_list)

		response = create_response(200)
		return response.get_response()
