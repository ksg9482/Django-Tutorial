from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote')
]

#최상위 URLconf에서 polls.urls 모듈을 바라보게 설정해야 한다.
#mysite/urls.py에 설정한다.