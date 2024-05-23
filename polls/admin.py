from django.contrib import admin

from polls.models import (
    Question,
    Status,
    Score
    )

# Register your models here.


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'category', 'difficulty', 'question_type')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')


admin.site.register(Score, ScoreAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Status, StatusAdmin)
