# 첫번째 장고 앱 작성하기 part 2

## 데이터베이스 연결

##### setting.py 파일이란?
Django 설정을 모듈변수로 표현한 보통의 Python 모듈이다.   
default로 SQLite를 사용하도록 되어있고, SQLite는 파이썬에서 기본으로 제공하기 때문에별도로 설치할 필요가 없다.   
그러나 실제 프로젝트를 시작 할 때에는 적절한 데이터베이스를 사용하는 것이 좋다.

##### INSTALLED_APPS
현재 Django 인스턴스에서 활성화된 모든 Django 어플리케이션의 이름이 담겨있다. 앱들은 다수의 프로젝트에서 사용 될 수 있고, 다른 프로젝트에서 쉽게 사용될 수 있도록 패키징하여 배포 할 수 있다.

___
### 데이터베이스 테이블 생성
```python
python manage.py migrate
```
migrate 명령은 INSTALLED_APPS 설정을 탐색하여 mysite/settings.py의 데이터베이스 설정과 함께 제공되는 database migration에 따라 필요한 데이터베이스 테이블을 생성한다.

#### 모델 만들기
polls/models.py 에서 작성한다.   
모델을 통해 데이터베이스 스키마 생성, 데이터베이스에 접근하기 위한 API 생성등을 할 수 있다.   
이를 위해선 가장 먼저 INSTALLED_APPS에 경로를 추가하여 현재 프로젝트에게 polls 앱이 설치되어 있음을 알려야 한다.   
   
polls 디렉토리, apps.py 파일, PollsConfig 클래스이기 때문에 입력해야 할 경로는 'polls.apps.PollsConfig'가 된다.
   
```python
python manage.py makemigrations polls
```
   
makemigrations를 실행시켜 모델을 변경한(새로 만든) 사실과 이 변경사항을 
migration으로 저장시키고 싶다는 것을 Django에게 알려준다.

```python
python manage.py sqlmigrate polls 0001
```
sqlmigrate명령은 migration 이름을 인수로 받아 실행하는 SQL문장을 출력한다. 위 명령은 makemigrations명령으로 생성된 0001_initial.py 파일을 실행할 경우 입력될 SQL을 보여준다. 실제로 migrate를 실행하는 명령어는 migrate이다.

```python
python manage.py migrate
```

migrate 명령은 아직 적용되지 않은 마이그레이션을 모두 수집해 이를 실행하고 (Django의 경우 django_migrations 테이블을 두어 마이그레이션 적용 여부를 추적한다.) 이 과정을 통해 모델에서의 변경사항과 데이터베이스 스키마의 동기화가 이뤄진다. 

##### 모델의 변경을 만드는 3가지 지침
1. (models.py 에서) 모델을 변경.
2. python3 manage.py makemigrations 명령으로 변경사항에 대한 마이그레이션 생성
3. python3 manage.py migrate 명령으로 변경사항을 데이터베이스에 적용


### 대화식 Python 쉘
```python
python manage.py shell
```
단순히 python이 아니라 이것을 사용한 이유는 manage.py에 설정된 DJANGO_SETTINGS_MODULE 환경변수 때문이다. 이 변수는 Django에게 mysite/settings.py의 python 가져오기 경로를 제공한다.

## 관리자 페이지
### 개요
Django는 모델에 대한 관리용 인터페이스를 자동으로 생성한다. '컨텐츠 게시자'와 '공개 사이트'구분이 명확하며, 사이트 관리자는 컨텐츠를 시스템에 추가하고 그렇게 추가된 컨텐츠는 공개 사이트에 노출된다.

```python
python manage.py createsuperuser
```
명령어를 입력하고 세부 설정한다.
* Username: admin
* Email address: 'admin@example.com'
* Password: **********
  * Password (again): *********

비밀번호가 8자리 이하, 너무 평범하거나, 숫자만 있으면 경고문이 나온다.
   
로컬도메인의 /admin/으로 이동하면 관리자의 로그인 화면이 나온다. 로그인하면 관리 인덱스 페이지에 접속된다.
   
편집 가능한 그룹과 사용자와 같은 컨텐츠를 볼 수 있고 이것들은  django.contrib.auth에서(Django에서) 제공되는 인증 프레임워크이다.

### 관리 사이트에서 poll app 을 변경가능하도록 만들기
처음에는 poll app이 관리페이지에서 보이지 않는다. 관리 인터페이스에 poll app에서 작성한 Question이 있다고 알려주어야 하는데 이는 polls/admin.py에서 설정한다.

#### 알아둘 점
* Question에 해당하는 관리페이지 서식은 Question 모델에서 자동으로 생성되었다.
* 모델의 각 필드 유형들은 적절한 HTML 입력 위젯으로 표현된다.(용도에 맞게 필드 유형을 설정해야 한다.)
* 각각의 DateTimeField 는 JavaScript 로 작성된 단축 기능과 연결된다.
* 하단의 작업 후 옵션
  * 저장(Save) - 변경 사항을 저장하고 변경된 목록 페이지를 보인다.
  * 저장 및 편집 계속(Save and continue editing) - 변경 사항을 저장하고 편집창을 갱신한다.
  * 저장 및 다른 이름으로 추가(Save and add another) - 변경 사항을 저장하고 이 유형과 같은 새로운(비어있는) 입력창을 불러온다.
  * 삭제(Delete) - 삭제를 확인하는 페이지를 띄운다.
