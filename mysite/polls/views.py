from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")

# 뷰를 호출하려면 연결된 URL이 있어야 한다.
