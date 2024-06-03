from django.contrib import admin

from polls.models import (
    Question
    )

# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'text', 'question_type', 'difficulty')


admin.site.register(Question, QuestionAdmin)
