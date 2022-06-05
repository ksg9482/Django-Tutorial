# 첫번째 장고 앱 작성하기 part 4

## 템플릿 작성과 소스코드 단축
### polls/detail.html 수정
템플릿에 HTML <form> 요소를 포함시킨다.
```html
<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
<fieldset>
    <legend><h1>{{ question.question_text }}</h1></legend>
    {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
</fieldset>
<input type="submit" value="Vote">
</form>
```
* 라디오 버튼중 하나를 선택하여 폼을 제출하면 POST 데이터인 choice=#을 보낸다. 여기서 #은 선택한 항목의 id이며 이것이 HTML 폼의 기본 개념이다.
* 데이터 서버측을 변경하는 양식을 만들 때마다 POST 메서드를 사용하는 것이 좋다. 이는 Django에만 국한된 것이 아니라 일반적인 좋은 웹 개발 관행이다.
* POST 양식을 만들고 있기 때문에, 교차 사이트 요청 위조(Cross Site Request Forgeries)에 대해 신경써야 하지만 Django는 그로부터 보호하는 시스템을 가지고 있다. 내부 URL을 대상으로 하는 모든 POST 양식은 {% csrf_token %} 템플릿 태그를 사용해야 한다.

### 제너릭 뷰
지금까지 작성한 detail(), result(), index()의 뷰는 간단하고 서로 중복되거나 비슷하다. 이는 URL에 전달된 매개변수에 따라 데이터베이스에서 데이터를 가져오고, 템플릿을 로드하고, 렌더링된 템플릿을 반환하는 기본적인 웹개발이다. Django는 이런 흔한 패턴을 간단하게 만들어주는 generic views를 제공한다. 제너릭 뷰는 일반적인 패턴을 추상화하여 개발에 소모되는 시간을 줄여준다.

#### 제너릭 뷰의 적용
우선, polls/urls.py URLconf을 수정한다.
```python
# Before
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
# After
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
```
*  두번째와 세번째 path의 경로 문자열이 'question_id'에서 'pk'로 변경되었다.

다음으로  polls/views.py의 index, detail, results 뷰를 제거하고 제너릭 뷰를 대신 사용한다. 각각 def index, def detail, def results가 class IndexView, class DetailView, class ResultsView로 변한다.

```python
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
```
* ListView, DetailView의 2가지 제너릭 뷰를 사용하고 있다.
  * ListView는 개체 목록 표시를 추상화 한다.
  * DetailView는 특정 개체에 대한 세부 정보 표시를 추상화 한다.
* model: 각 제너릭 뷰는 어떤 모델을 적용할지 입력해야 한다.
* template_name: Django에게 자동 생성 된 기본 템플릿 이름 대신에 특정 템플릿 이름을 사용하도록 알려주기 위해 사용된다.
  * DetailView는 <app name>/<model name>_detail.html 템플릿을 사용한다.
  * ListView도 마찬가지로 <app name>/<model name>_list.html 템플릿을 기본으로 사용한다.
* DetailView는 URL에서 캡처된 기본 키 값이 pk라 기대하기 때문에 question_id를 pk로 변경한 것이다.

### 
이전에 템플릿은 question 및 latest_question_list 컨텍스트 변수를 포함하는 컨텍스트와 함께 제공되었다.   
DetailView의 경우 question 변수가 자동으로 제공되는데, 이는 Django 모델(Question)을 사용하고 있기 때문에 Django가 컨텍스트 변수의 적절한 이름을 결정할 수 있다. 그러나 ListView의 경우 자동으로 생성되는 컨텍스트 변수는 question_list이다.   
이것을 덮어 쓰려면 context_object_name 속성을 제공하고, 대신에 latest_question_list 를 사용하도록 지정해야 한다. 새로운 기본 컨텍스트 변수와 일치하도록 템플릿을 변경할 수도 있지만, 원하는 변수를 사용하도록 지시하는 것이 훨씬 쉽다.