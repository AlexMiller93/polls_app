from django.urls import path

from polls.views import index, quiz, quiz_multiple

app_name = 'polls'

urlpatterns = [
    path('', index, name='index'),
    path('quiz/', quiz, name='quiz'),
    path('quiz_multiple/', quiz_multiple, name='quiz_multiple'),
]
