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

#### render
context를 템플릿으로 표현한 결과를 HttpResponse 객체와 함께 돌려주는 것은 자주 쓰는 용법이다. Django는 이 기능에 대해 단축 기능을 제공한다.

```python
from django.shortcuts import render
from .models import Question

# loader를 통해 템플릿을 불러오고, HttpResponse를 통해 context에 템플릿을 적용하여 반환한다.
latest_question_list = Question.objects.order_by('-pub_date')[:5]
template = loader.get_template('polls/index.html')
context = {
    'latest_question_list': latest_question_list,
}
return HttpResponse(template.render(context, request))

#위 코드를 render를 이용해 단축 할 수 있다.
latest_question_list = Question.objects.order_by('-pub_date')[:5]
context = {'latest_question_list': latest_question_list}
return render(request, 'polls/index.html', context)
```
render() 함수는 request 객체를 첫번째 인수, 템플릿 이름을 두번째 인수로 받고, context 객체를 선택적인 인수로 받는다.   
   
render를 모든 뷰에 적용한다면 loader와 HttpResponse 할 필요가 없다.   
단, detail, results, vote에서 stub 메소드를 가지고 있다면 HttpResponse를 유지할 필요가 있다.   
   
#### 404에러 발생시키기
만약 객체가 존재하지 않을 때 get()을 사용하여 예외를 발생시키는 것은 자주 쓰이는 용법이다. Django는 이 기능에 대해 단축 기능을 제공한다.
```python
from django.shortcuts import get_object_or_404, render

# 요청된 질문의 아이디가 없을 경우 Http404를 발생시킨다.
try:
  question = Question.objects.get(pk=question_id)
except Question.DoesNotExist:
  raise Http404("Question does not exist")

# 위 내용을 Django의 단축 기능을 통해 단축하면 아래처럼 된다.
question = get_object_or_404(Question, pk=question_id)

return render(request, 'polls/detail.html', {'question': question})
```
get_object_or_404() 함수는 Django 모델을 첫번째 인자로 받고, 몇개의 kwargs를 모델 관리자의 get() 함수에 넘긴다. 만약 객체가 존재하지 않을 경우 Http404 예외가 발생한다.

##### 왜  get_object_or_404() 또는 Http404를 사용하는가?
상위 계층에서 ObjectDoesNotExist 예외를 자동으로 잡아 내는 대신 get_object_or_404() 도움 함수(helper functoin)를 사용하거나,  ObjectDoesNotExist 예외를 사용하는 대신 Http404 를 사용하는 이유는 다음과 같다.
* 모델 계층을 뷰 계층에 연결하는 방법이다.
* Django의 중요한 설계 목표는 약결합(loose coupling)을 관리하는 데에 있다.

### URL의 이름 공간(name space) 정하기
실제 Django 프로젝트에는 앱이 여러개 있을텐데 Django는 이 앱들의 URL을 어떻게 구별해 낼까? Django가 {% url %} 템플릿 태그를 사용할 때, 어떤 앱의 뷰에서 URL을 생성할지 알 수 있는 방법이 있을까?

* URLconf에 이름 공간(name space)을 추가하면 된다.
  *  polls/urls.py 파일에 app_name을 추가하여 어플리케이션의 이름공간을 설정할 수 있다.

```python
app_name = 'polls' # 앱 이름을 polls로 설정했다
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
```
polls/urls.py에 앱 이름을 설정하고 polls/template/polls/index.html에 url 'detail'을 바라보도록 한 것을 'polls:detail'로 설정한다.

```html
<a href="{% url 'detail' question.id %}">
  {{ question.question_text }}
</a>
<!-- 'detail'을 'polls:detail'로 재설정-->
<a href="{% url 'polls:detail' question.id %}">
  {{ question.question_text }}
</a>
```