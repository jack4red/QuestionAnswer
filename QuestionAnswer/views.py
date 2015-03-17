from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import Http404


from QuestionAnswer.models import Question

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

def write_answer(request, question_id):
	return HttpResponse('Write an answer for question: %s' % question_id)


