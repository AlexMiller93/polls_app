from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.

USER_STATUSES = [
    ('Beginner', 'Beginner'),
    ('Amateur', 'Amateur'),
    ('PRO', 'PRO'),
    ('BEST', 'BEST'),
]


class Score(models.Model):
    """ """
    points = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Question(models.Model):
    """ """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(blank=True, max_length=100)
    question_type = models.CharField(blank=True, max_length=100)
    difficulty = models.CharField(blank=True, max_length=100)
    text = models.CharField(blank=True, max_length=1000)
    correct_answer = models.CharField(blank=True, max_length=100)
    wrong_answer = models.CharField(blank=True, max_length=100)
    answer1 = models.CharField(blank=True, max_length=100)
    answer2 = models.CharField(blank=True, max_length=100)
    answer3 = models.CharField(blank=True, max_length=100)
    answer4 = models.CharField(blank=True, max_length=100)


class Status(models.Model):
    """ """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        blank=False,
        choices=USER_STATUSES,
        default='Beginner',
    )
