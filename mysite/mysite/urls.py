"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]

"""
include()함수는 다른 URLconf들을 참조할 수 있도록 도와준다. 
Django가 함수 include()를 만나면 URL의 그 시점까지 일치하는 부분을 잘라내고 
남은 문자열 부분을 후속처리를 위해 include된 URLconf에 전달한다.

다른 URL 패턴을 포함할 떄 마다 include()를 사용해야 하고, 
admin.site.urls만이 유일한 예외이다.

path에는 필수 인수 2개가 있다.

route - url패턴을 가진 문자열이다. 요청이 처리 될 때
 url패턴의 첫번째 패턴에서 부터 시직해서 일치하는 패턴을 찾을 때까지
 요청된 url을 각 패턴과 리스트의 순서대로 비교한다.
 패턴들은 GET이나 POST 같은 매개변수들, 도메인 이름을 검색하지 않는다.
 https://www.example.com/myapp/ 가 요청된 경우 URLconf는 myapp/만 바라본다.

view - Django에서 일치하는 패턴을 찾으면 HttpRequest 객체를 첫번째 인수로 하고 
경로로 부터 갭처된 값을 키워드 인수로 하여 특청한 view함수를 호출한다.

선택가능한 인수 2개가 있다.
kwargs - 임의의 키워드 인수들은 목표한 view에 사전형으로 전달된다.

name - URL에 이름을 지으면 템플릿을 포함한 Django 어디서나 명확하게 참조할 수 있다.
단 하나의 파일만 수정해도 프로젝트 내의 모든 URL패턴을 바꿀 수 있도록 도와준다.
"""