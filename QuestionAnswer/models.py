from django.db import models

# Create your models here.

class Question(models.Model):
	question_text = models.CharField(max_length=100)
	pub_date = models.DateTimeField('date posted')

	def __str__(self):
		return self.question_text

class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer_text = models.CharField(max_length=100)
	pub_date = models.DateTimeField('date posted')

	def __str__(self):
		return self.answer_text
