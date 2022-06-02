from django.shortcuts import render, get_object_or_404

# Django의 단축기능으로 대체되었다.
from re import template
from django.http import Http404, HttpResponse
from django.template import loader

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request, 'polls/index.html', context)
    
# context는 템플릿에서 쓰이는 변수명과 Python 객체를 연결하는 사전형(dict) 값이다.

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# get_object_or_404() 함수처럼 동작하는 get_list_or_404()도 있다.
# 차이점은 get() 대신 filter()를 쓴다는 것이다. 