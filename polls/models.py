from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


USER_STATUSES = [
    ('Beginner', 'Beginner'),
    ('Amateur', 'Amateur'),
    ('PRO', 'PRO'),
    ('BEST', 'BEST'),
]


class Score(models.Model):
    """ Таблица для подсчета баллов """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0, help_text='Баллы')
    counter_bool = models.IntegerField(
        default=0, help_text='Счетчик отвеченных вопросов правда или ложь')
    counter_multiple = models.IntegerField(
        default=0,
        help_text='Счетчик отвеченных вопросов с вариантами ответов')


class Question(models.Model):
    """ Таблица для сохранения вопросов """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(
        blank=True, max_length=100, help_text='Категория')
    question_type = models.CharField(
        blank=True, max_length=100, help_text='Тип вопроса')
    difficulty = models.CharField(
        blank=True, max_length=100, help_text='Сложность')
    text = models.CharField(blank=True, max_length=1000, help_text='Вопрос')
    correct_answer = models.CharField(
        blank=True, max_length=100, help_text='Правильный ответ')
    wrong_answer = models.CharField(
        blank=True, max_length=100, help_text='Некорректный ответ')
    answer1 = models.CharField(blank=True, max_length=100, help_text='1 Ответ')
    answer2 = models.CharField(blank=True, max_length=100, help_text='2 Ответ')
    answer3 = models.CharField(blank=True, max_length=100, help_text='3 Ответ')
    answer4 = models.CharField(blank=True, max_length=100, help_text='4 Ответ')


class Status(models.Model):
    """ Таблица для статусов пользователей """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=8,
        blank=False,
        choices=USER_STATUSES,
        default='Beginner',
        help_text='Статус пользователя'
    )
