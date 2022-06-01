# 첫번째 장고 앱 작성하기 part 3

## View 생성

### View
view는 일반적으로 Django 애플리케이션에 있는 웹 페이지에 기능을 제공하는 특정한 템플릿을 가진 "type"이다.
   
예:
* blog 홈페이지 - 가장 최근의 항목들 표시
* 항목 세부 페이지 - 하나의 항목에 연결하는 영구적인 링크 제공
* 일자(년, 월, 일 별) 축적 페이지 - 주어진 일자의 모든 항목 표시
* 댓글 기능 - 특정 항목의 댓글 관리
   
Django에서는 웹페이지와 기타 콘텐츠가 view로 전달된다. 각 view는 Python 함수 혹은 클래스 기반일 경우 메서드로 표현된다. Django는 요청한 URL을 확인하여 보기를 선택하고, URL로부터 view를 얻기 위해 URLconfs를 사용하여 URL 패턴을 뷰에 연결한다.
   
view는 둘 중 한가지를 해야한다. 바로 요청된 페이지의 내용이 담긴 HttpResponse 객체를 반환하거나, Http404 등 예외를 반환해야 한다.

#### view 생성
view는 데이터베이스를 읽거나 어떤 라이브러리를 사용하거나 파일을 생성 할 수 있다. 코드를 그냥 작성할 수 있지만 tempalate 디렉토리를 만드는 것이 좋다. tempalates 디렉토리가 있을 경우 Django는 여기서 템플릿을 찾게 된다.
* tempalate을 작성하는 이유? 
  * Python 코드로부터 디자인을 분리하기 위해서. 만약 하나로 결합되어 있다면 Python 코드 자체를 편집해야 한다.
프로젝트의 templates 설정은 Django가 어떻게 템플릿을 불러오고 렌더링 할 것인지 설명한다. 기본 설정으로 APP_DIRS 옵션이 True인 DjangoTemplates 백엔드를 구성한다. DjangoTemplates는 각 INSTALLED_APPS 디렉토리의 "templates" 하위 디렉토리를 탐색한다.
```python
# 실제로 settings.py에 기본적으로 설정되어 있는 모습
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
* polls 디렉토리를 기준으로 했을 때 템플릿 파일 제작 위치
  * polls/templates/polls/index.html

##### 템플릿 생성시 주의 사항
템플릿을 polls/templates에 직접 넣지 않고 다른 식으로 구성할 수 있지만 권장할 방법은 아니다. Django는 이름이 일치하는 첫번째 템플릿을 선택하는데 만약 다른 어플리케이션에 같은 이름의 템플릿이 있으면 Django는 서로 다른 템플릿을 구분 할 수 없다. 그렇기에 어플리케이션 이름으로 된 디렉토리에 템플릿을 넣어야 한다.