from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse

import django.utils.timezone as timezone


from QuestionAnswer.models import Question, Answer

# Create your views here.

def index(request):
	latest_questions = Question.objects.order_by('-pub_date')[:5]
	context = {
		'latest_questions': latest_questions
		}

	return render(request, 'QuestionAnswer/index.html', context)

def detail(request, question_id):
	question = get_object_or_404(Question, pk = question_id)

	return render(request, 'QuestionAnswer/detail.html', {
			'question': question}
		)	

def view_answer(request, question_id):
	q = get_object_or_404(Question, pk = question_id)
	answer_text = request.POST['answer_text']

	q.answer_set.create(answer_text=answer_text, pub_date=timezone.now())

	return HttpResponseRedirect(reverse('QuestionAnswer:detail', 
					args=(question_id,)))
	

	


