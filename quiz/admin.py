from django.contrib import admin
from .models import Question, Answer, TestSubmission


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class TestSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_answers')

    def get_answers(self, obj):
        return ", ".join([str(answer) for answer in obj.answers.all()])

    get_answers.short_description = 'Answers'


admin.site.register(Question, QuestionAdmin)
admin.site.register(TestSubmission, TestSubmissionAdmin)
