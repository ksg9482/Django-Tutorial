# Django-Tutorial

### 서버 실행
```python
python3 manage.py runserver
```
단, 개발시에는 runserver로 서버를 구동해도 되나 실제 배포에는 Nginx 등 다른 방법을 사용해야 한다. Django는 웹 프레임워크이다.

#### 포트변경
```python
python3 manage.py runserver 8080
```
커맨드 라인에 인수를 전달하면 된다.   
만약 가능한 모든 공용 ip를 받으려면 '0:8000'을 전달하면 된다.

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
