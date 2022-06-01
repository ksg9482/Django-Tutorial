from re import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        "latest_question_list": latest_question_list
    }
    return HttpResponse(template.render(context, request))

# 뷰를 호출하려면 연결된 URL이 있어야 한다.
# polls/template를 불러온 후 context를 전달한다. 
# context는 템플릿에서 쓰이는 변수명과 Python 객체를 연결하는 사전형(dict) 값이다.
