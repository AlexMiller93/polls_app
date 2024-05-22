from django.urls import path

from polls.views import index

app_name = 'polls'

urlpatterns = [
    path('', index, name='index')
]
