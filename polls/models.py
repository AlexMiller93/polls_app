from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS = [
    ('BEGINNER', 'Beginner'),
    ('AMATEUR', 'Amateur'),
    ('PRO', 'PRO'),
    ('BEST', 'BEST'),
]

TYPES = [
    ('BOOLEAN', 'Boolean'),
    ('MULTIPLE  ', 'Multiple')
]

DIFF_LEVELS = [
    ('EASY', 'Easy'),
    ('MEDIUM', 'Medium'),
    ('HARD', 'Hard'),
]


class Category(models.Model):
    """ Таблица для сохранения категорий """
    
    name = models.CharField(
        max_length=100, help_text='Категория вопроса')


class Question(models.Model):
    """ Таблица вопросов """

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_type = models.CharField(
        choices=TYPES, max_length=10, help_text='Тип вопроса')
    difficulty = models.CharField(
        choices=DIFF_LEVELS, max_length=100, help_text='Сложность вопроса')
    text = models.CharField(max_length=1000, help_text='Текст вопроса')
    correct_answer = models.CharField(
        max_length=100, help_text='Правильный ответ')
    answer1 = models.CharField(max_length=100, help_text='1 Ответ')
    answer2 = models.CharField(max_length=100, help_text='2 Ответ')
    answer3 = models.CharField(max_length=100, help_text='3 Ответ')
    answer4 = models.CharField(max_length=100, help_text='4 Ответ')


class Answer(models.Model):
    """ Таблица ответов на вопросы для каждого пользователя """
    
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    attempt = models.IntegerField(default=0)


class Profile(models.Model):
    """ Таблица профиля пользователя """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0, help_text='Баллы')
    status = models.CharField(
        max_length=8,
        blank=False,
        choices=STATUS,
        default='Beginner',
        help_text='Статус пользователя'
    )
    counter_bool = models.IntegerField(
        default=0, 
        help_text='Счетчик отвеченных вопросов правда или ложь')
    counter_multiple = models.IntegerField(
        default=0,
        help_text='Счетчик отвеченных вопросов с вариантами ответов')


