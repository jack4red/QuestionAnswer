from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic

import django.utils.timezone as timezone


from QuestionAnswer.models import Question, Answer

# Create your views here.

class IndexView(generic.ListView):
	template_name = 'QuestionAnswer/index.html'
	context_object_name = 'latest_questions'

	def get_queryset(self):
		"""Get the 5 most recently added questions"""
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'QuestionAnswer/detail.html'

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
					


