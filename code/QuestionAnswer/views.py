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
		page = int(request.POST.get('page'))
		latest_news,is_end = collect_news(request.user.id,page)
		response = create_response(200)
		response.data.latest_news = latest_news
		response.data.is_end = is_end
		return response.get_response()
	else:
		latest_news,is_end = collect_news(request.user.id,0)

		c = RequestContext(request, {
			'latest_news':latest_news,
			'is_end':is_end,
		})
		return render_to_response('index.html', c)

def collect_news(user_id,page,count=8):
	cur_user = UserProfile.objects.get(user_id=user_id)
	
	list_question_ids = []
	list_theme_ids = []
	list_user_ids = []
	list_answer_ids = []
	if cur_user.focused_question_ids:
		list_question_ids = cur_user.focused_question_ids.split(',')
	if cur_user.focused_theme_ids:
		list_theme_ids = cur_user.focused_theme_ids.split(',')
	if cur_user.focused_user_ids:
		list_user_ids = cur_user.focused_user_ids.split(',')
	if cur_user.focused_answer_ids:
		list_answer_ids = cur_user.focused_answer_ids.split(',')

	news = NewsToUser.objects.filter(Q(action_user_id__in=list_user_ids)|Q(question_id__in=list_question_ids)|Q(answer_id__in=list_answer_ids)|Q(theme_id__in=list_theme_ids)).order_by('-created_at')
	news_count = news.count()
	news = news[page*count:(page+1)*count]
	news = {new.id:new for new in news}

	is_end = False
	if news_count<=(page+1)*count:
		is_end =True

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

		if news[new].actioned_user_id:
			new_obj['actioned_user_id']=news[new].actioned_user_id
			new_obj['actioned_user_name']=User.objects.get(id=news[new].actioned_user_id).username

		new_obj['action_user']=str(news[new].action_user)
		new_obj['action_type']=news[new].action_type
		new_obj['created_at']=news[new].created_at.strftime('%Y-%m-%d %H:%M')
		
		latest_news.insert(0,new_obj)
		

	return latest_news,is_end

@login_required(login_url='/account/login/')
def theme_detail(request):
	try:
		theme_id = request.GET.get('theme_id','1')
		theme = Theme.objects.get(id=theme_id)

		focused = False
		cur_user = UserProfile.objects.get(user_id=request.user.id)
		focused_theme_ids_list = cur_user.focused_theme_ids.split(',')
		if theme_id in focused_theme_ids_list:
			focused = True

		all_Q = Question.objects.all()
		questions = []
		for q in all_Q:
			owner_theme_ids_list = q.owner_theme_ids.split(',')
			if theme_id in owner_theme_ids_list:
				questions.append({'id':q.id,'title':q.question_title})
		c = RequestContext(request, {
				'questions':questions,
				'theme_name':theme.theme_name,
				'description':theme.description,
				'focused':focused,
				'theme_id':theme_id,
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

		focused = False
		focused_question_ids = UserProfile.objects.get(user_id=request.user.id).focused_question_ids
		focused_question_ids_list =focused_question_ids.split(',')
		if question_id in focused_question_ids_list:
			focused =True

		for answer in answers:
			answer_obj = {}
			answer_obj['id'] = answer
			answer_obj['owner_user_id'] = answers[answer].owner_user_id
			answer_obj['owner_user_name'] = User.objects.get(id=answers[answer].owner_user_id).username

			answer_obj['up_owner_user_ids_num'] = 0
			answer_obj['down_owner_user_ids_num'] = 0
			if answers[answer].up_owner_user_ids:
				answer_obj['up_owner_user_ids_num'] = len(answers[answer].up_owner_user_ids.split(','))
			if answers[answer].down_owner_user_ids:
				answer_obj['down_owner_user_ids_num'] = len(answers[answer].down_owner_user_ids.split(','))

			answer_obj['answer_text'] = answers[answer].answer_text
			answer_obj['created_at'] = answers[answer].created_at
			answer_list.append(answer_obj)
		#sort lambda feature

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
				'answers_num':len(answer_list),
				'focused':focused,
				'question_id':question_id,
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
		owner_user = User.objects.get(id=answer.owner_user_id)
		user_id = str(request.user.id)

		focused_answer_ids_list = UserProfile.objects.get(user_id=user_id).focused_answer_ids.split(',')
		collected_answer_ids_list = UserProfile.objects.get(user_id=user_id).collected_answer_ids.split(',')
		if answer_id in focused_answer_ids_list:
			focused = True
		else:
			focused = False
		if answer_id in collected_answer_ids_list:
			collected = True
		else:
			collected =False

		up_owner_user_ids_num = 0
		down_owner_user_ids_num = 0
		is_in_up_list = False
		is_in_down_list = False

		if answer.up_owner_user_ids:
			up_owner_user_ids_list = answer.up_owner_user_ids.split(',')
			up_owner_user_ids_num = len(up_owner_user_ids_list)
			is_in_up_list = True if user_id in up_owner_user_ids_list else False
		if answer.down_owner_user_ids:
			down_owner_user_ids_list = answer.down_owner_user_ids.split(',')
			down_owner_user_ids_num = len(down_owner_user_ids_list)
			is_in_down_list = True if user_id in down_owner_user_ids_list else False
		
		comments = [{'comment_user_name':comment.owner_user_name,'comment_text':comment.comment_text} for comment in comments]

		c = RequestContext(request, {
				'question_id':answer.question_id,
				'question_title':question.question_title,
				'question_text':question.question_text,
				'created_at':answer.created_at,
				'answer_id':answer_id,
				'focused':focused,
				'collected':collected,
				'answer_text':answer.answer_text,
				'answer_user_name':owner_user.username,
				'answer_user_id':owner_user.id,
				'up_owner_user_ids_num':up_owner_user_ids_num,
				'down_owner_user_ids_num':down_owner_user_ids_num,
				'comments':comments,
				'comments_num':len(comments),
				'is_in_up_list':is_in_up_list,
				'is_in_down_list':is_in_down_list,
			})
		return render_to_response('answer_detail.html', c)
	
@login_required(login_url='/account/login/')
def add_theme(request):
	if request.POST:
		theme_title = request.POST.get('theme_title','')
		description = request.POST.get('description','')
		new_T = Theme.objects.create(theme_name=theme_title,description=description)
		response = create_response(200)
		response.data.theme_id = new_T.id
		return response.get_response()
	else:
		c = RequestContext(request, {
			})
		return render_to_response('add_theme.html', c)
	
@login_required(login_url='/account/login/')
def add_question(request):
	if request.POST:
		question_title = request.POST.get('question_title','')
		description = request.POST.get('description','')
		belone_theme = request.POST.get('belone_theme','')
		user_id = request.user.id

		New_Q = Question.objects.create(owner_theme_ids=belone_theme,owner_user_id=user_id,question_title=question_title,question_text=description)

		user = UserProfile.objects.get(user_id=user_id)

		focused_question_ids_list = []
		if user.focused_question_ids:
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
		question_id = request.POST.get('question_id','1')
		user_id = request.user.id
		answer_text = request.POST.get('answer_text','')

		new_A = Answer.objects.create(question_id=question_id,answer_text=answer_text,owner_user_id=user_id)
		NewsToUser.objects.create(action_user_id=user_id,answer_id=new_A.id,question_id=question_id,action_type=3)
		user = UserProfile.objects.get(user_id=user_id)
		focused_answer_ids_list = []
		focused_question_ids_list = []
		if user.focused_answer_ids:
			focused_answer_ids_list = user.focused_answer_ids.split(',')
		if user.focused_question_ids:
			focused_question_ids_list = user.focused_question_ids.split(',')
		focused_answer_ids_list.append(str(new_A.id))
		focused_question_ids_list.append(question_id)
		user.focused_answer_ids = ','.join(focused_answer_ids_list)
		user.focused_question_ids = ','.join(focused_question_ids_list)
		user.save()

		response = create_response(200)
		response.data.answer_id=new_A.id
		return response.get_response()
	else:
		pass

@login_required(login_url='/account/login/')
def add_comment(request):
	if request.POST:
		answer_id = request.POST.get('answer_id')
		owner_user_name = str(request.user)
		comment_text = request.POST.get('comment_text')
		Comment.objects.create(answer_id=answer_id,owner_user_name=owner_user_name,comment_text=comment_text)

		question_id = Answer.objects.get(id=answer_id).question_id
		NewsToUser.objects.create(action_user_id=request.user.id,answer_id=answer_id,question_id=question_id,action_type=4)
		response = create_response(200)
		return response.get_response()
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
				focused_theme_ids_list = []
				if user.focused_theme_ids:
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
				focused_question_ids_list = []
				if user.focused_question_ids:
					focused_question_ids_list = user.focused_question_ids.split(',')
				if not question_id in focused_question_ids_list:
					focused_question_ids_list.append(question_id)
					NewsToUser.objects.create(action_user_id=user_id,question_id=question_id,action_type=0)
				else:
					focused_question_ids_list.remove(question_id)
				user.focused_question_ids = ','.join(focused_question_ids_list)
				user.save()

			elif action_type == 'user':
				actioned_user_id = request.POST.get('actioned_user_id')

				user = UserProfile.objects.get(user_id=user_id)
				focused_user_ids_list = []
				if user.focused_user_ids:
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
				focused_answer_ids_list = []
				if user.focused_answer_ids:
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
		user_id = str(request.user.id)
		action_type = request.POST.get('action_type')

		answer = Answer.objects.get(id=answer_id)
		up_owner_user_ids_list = []
		down_owner_user_ids_list = []
		if answer.up_owner_user_ids:
			up_owner_user_ids_list = answer.up_owner_user_ids.split(',')
		if answer.down_owner_user_ids:
			down_owner_user_ids_list = answer.down_owner_user_ids.split(',')

		is_in_up_list = False
		is_in_down_list = False

		if action_type == 'up':
			if not user_id in up_owner_user_ids_list:
				up_owner_user_ids_list.append(user_id)
				is_in_up_list = True
				NewsToUser.objects.create(action_user_id=user_id,answer_id=answer_id,action_type=5)
			else:
				up_owner_user_ids_list.remove(user_id)
			if user_id in down_owner_user_ids_list:
				down_owner_user_ids_list.remove(user_id)

		if action_type == 'down':
			if not user_id in down_owner_user_ids_list:
				down_owner_user_ids_list.append(user_id)
				is_in_down_list = True
				NewsToUser.objects.create(action_user_id=user_id,answer_id=answer_id,action_type=6)
			else:
				down_owner_user_ids_list.remove(user_id)
			if user_id in up_owner_user_ids_list:
				up_owner_user_ids_list.remove(user_id)

		answer.up_owner_user_ids = ','.join(up_owner_user_ids_list)
		answer.down_owner_user_ids = ','.join(down_owner_user_ids_list)
		answer.save()

		response = create_response(200)
		response.data.is_in_up_list = is_in_up_list
		response.data.is_in_down_list = is_in_down_list
		response.data.up_num = len(up_owner_user_ids_list)
		response.data.down_num = len(down_owner_user_ids_list)
		return response.get_response()

@login_required(login_url='/account/login/')
def search_action(request):
	if request.POST:
		pass
	else:
		user_id = str(request.user.id)
		search_word = request.GET.get('search_word')
		search_type = request.GET.get('search_type')
		result_list = search_method(user_id,search_word,search_type,0)

		c = RequestContext(request, {
			'search_type':search_type,
			'result_list':result_list
		})
		return render_to_response('search_action.html', c)

def search_method(user_id,search_word,search_type,search_num):
	result_list = []
	if search_type == 'theme':
		if search_num:
			themes = Theme.objects.filter(theme_name__contains=search_word)[0:search_num]
		else:
			themes = Theme.objects.filter(theme_name__contains=search_word)
		focused_theme_ids_list = []
		cur_user_focused_ids = UserProfile.objects.get(user_id=user_id).focused_theme_ids
		if cur_user_focused_ids:
			focused_theme_ids_list = cur_user_focused_ids.split(',')

		for theme in themes:
			if str(theme.id) in focused_theme_ids_list:
				result_list.append({'id':theme.id,'name':theme.theme_name,'focused':True})
			else:
				result_list.append({'id':theme.id,'name':theme.theme_name,'focused':False})
	if search_type == 'question':
		if search_num:
			questions = Question.objects.filter(question_title__contains=search_word)[0:search_num]
		else:
			questions = Question.objects.filter(question_title__contains=search_word)
		focused_question_ids_list = []
		cur_user_focused_ids = UserProfile.objects.get(user_id=user_id).focused_question_ids
		if cur_user_focused_ids:
			focused_question_ids_list = cur_user_focused_ids.split(',')
		for question in questions:
			if str(question.id) in focused_question_ids_list:
				result_list.append({'id':question.id,'name':question.question_title,'focused':True})
			else:
				result_list.append({'id':question.id,'name':question.question_title,'focused':False})

	if search_type == 'user':
		if search_num:
			users = User.objects.filter(username__contains=search_word)[0:search_num]
		else:
			users = User.objects.filter(username__contains=search_word)
		focused_user_ids_list = []
		cur_user_focused_ids = UserProfile.objects.get(user_id=user_id).focused_user_ids
		if cur_user_focused_ids:
			focused_user_ids_list = cur_user_focused_ids.split(',')
		for user in users:
			if str(user.id) in focused_user_ids_list:
				result_list.append({'id':user.id,'name':user.username,'focused':True})
			else:
				result_list.append({'id':user.id,'name':user.username,'focused':False})

	return result_list

@login_required(login_url='/account/login/')
def collect_answer(request):
	if request.POST:
		user_id = request.user.id
		answer_id = request.POST.get('answer_id')
		user = UserProfile.objects.get(user_id=user_id)
		collected_answer_ids_list = []
		if user.collected_answer_ids:
			collected_answer_ids_list = user.collected_answer_ids.split(',')
		if answer_id in collected_answer_ids_list:
			collected_answer_ids_list.remove(answer_id)
		else:
			collected_answer_ids_list.append(answer_id)
		user.collected_answer_ids = ','.join(collected_answer_ids_list)
		user.save()
		response = create_response(200)
		return response.get_response()
	else:
		pass
