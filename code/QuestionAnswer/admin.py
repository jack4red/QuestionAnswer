from django.contrib import admin
from QuestionAnswer.models import Question, Answer

# Register your models here.

class AnswerInline(admin.TabularInline):
	model = Answer
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	fields = ['question_text']
	inlines = [AnswerInline]
	
	list_display = ('question_text', 'pub_date')
	list_filter = ['pub_date']
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
