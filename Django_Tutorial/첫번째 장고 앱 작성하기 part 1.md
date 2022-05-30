# 첫번째 장고 앱 작성하기 part 1

## 프로젝트 시작 
### 명령어 실행: python django-admin startproject mysite

```python
mysite/
    manage.py
    mysite/
        __init__.py
        setting.py
        urls.py
        asgi.py
        wsgi.py
```
* mysite/ 
  * 디렉토리 밖은 프로젝트를 담는 공간. 이름은 Django와 상관 없으니 변경해도 된다.
* manage.py 
  * Django 프로젝트와 다양한 방법으로 상호작용하는 커맨드라인의 유틸리티.
* mysite/\_\_init\_\_.py
  * Python에게 이 디렉토리를 패키지처럼 다루라고 알려주는 용도의 빈 파일.
* mysite/settings.py
  * 현재 Django 프로젝트의 환경 및 구성을 저장한다.
* mysite/urls.py
  * 현재 Django 프로젝트의 URL을 선언한다.
* mysite/asgi.py 
  * 현재 프로젝트를 서비스하기 위한 ASGI 호환 웹서버의 진입점.
* mysite/wsgi.py
  * 현재 프로젝트를 서비스하기 위한 WSGI 호환 웹서버의 진입점.
___
### 서버 실행
```python
python manage.py runserver
```
단, 개발시에는 runserver로 서버를 구동해도 되나 실제 배포에는 Nginx 등 다른 방법을 사용해야 한다. Django는 웹 프레임워크이다.

#### 포트변경
```python
python manage.py runserver 8080
```
커맨드 라인에 인수를 전달하면 된다.   
만약 가능한 모든 공용 ip를 받으려면 '0:8000'을 전달하면 된다.
___
#### 투표 어플리케이션 제작을 위한 폴더 생성
```python
python3 manage.py startapp polls

polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    test.py
    views.py
```
뷰를 호출하려면 이와 연결된 URL이 있어야 하는데 이를 위해 URLconf가 사용된다.

polls 디렉토리에서 URLconf를 생성하려면 urls.py를 생성해야 한다.

polls/urls.py에는 이와 같은 코드가 포함되어 있다.
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
최상위 URLconf에서 polls.urls 모듈을 바라보게 설정하기 위해 
mysite/urls.py 파일을 설정한다.

