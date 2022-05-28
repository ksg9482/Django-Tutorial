from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index')
]

#최상위 URLconf에서 polls.urls 모듈을 바라보게 설정해야 한다.
#mysite/urls.py에 설정한다.