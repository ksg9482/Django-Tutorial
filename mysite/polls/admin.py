from django.contrib import admin
from .models import Question, Choice

# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    # Choice 객체는 Question 관리자 페이지에서 편집된다. 
    # 기본으로 3가지 선택 항목을 제공한다.
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
"""
관리사이트에 Question 클래스가 있음을 알려준다.
"""