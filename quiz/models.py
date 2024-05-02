from django.db import models
from custom_auth.admin import CustomUser


# Create your models here.
class Question(models.Model):
    text = models.TextField()


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField()


class TestSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer, related_name='submissions')
