# 첫번째 장고 앱 작성하기 part 5

## 자동화된 테스트와 뷰 개선
테스트는 다양한 수준에서 작동한다. 일부 테스트는 작은 세부사항에 적용 될 수 있고, 또다른 테스트는 소프트웨어의 전반적인 작동을 검사 할 수 있다. 자동화된 테스트는 이런 테스트 작업이 시스템에서 수행 된다. 한 번 테스트 세트를 작성한 이후에는 앱을 변경할 때 수동 테스트를 수행하지 않아도 원래 의도대로 코드가 작동하는지 확인 할 수 있다.

### 테스트를 작성해야 하는 이유
#### 결과적으로 시간을 절약 할 수 있다.
특정시점까지는 '제대로 작동하는지 확인'하는 것이 테스트로서 충분하다. 그러나 더 정교한 어플리케이션에서는 구성 요소간에 수십개의 복잡한 상호작용이 있을 수 있고, 이 경우 어느 하나에 대한 변경이 어플리케이션의 동작에 예기치 않은 결과를 가져 올 수 있다.   
코드가 제대로 작동되고 있음을 알 때 테스트를 작성하는 것이 코드를 작성하고 나서 수동으로 테스트하거나 새로 발견된 문제의 원인을 확인하는 것보다 더 효과적이다.
#### 테스트는 문제를 식별하는 것이 아니라 예방한다.
테스트는 어플리케이션의 목적과 의도된 동작이 정확히 무엇을 하고 있는지 선명하게 만들어 준다. 만약 어떤 것이 잘못되었을 때, 그것이 잘못되었음을 깨닫지 못하더라도 테스트는 잘못된 부분을 알려준다.
#### 테스트는 협업을 돕는다.
복잡한 어플리케이션은 팀별로 유지 관리된다. 테스트는 동료가 실수로 코드를 손상시키지 않는 것을 보장하고, 내가 동료의 코드를 손상시키지 않는 것을 보장한다.

### 테스팅 전략
흔하게는 코드를 작성하고 테스트가 필요함을 느껴 테스트 코드를 작성한다. 다른 한편으로는 실제로 코드를 작성하기 전에 미리 테스트를 작성한다. 이것을 TDD(Test-Driven Development 테스트 주도 개발)라고 한다.

### 테스트 작성
#### 버그 식별
polls 어플리케이션에는 지금 시점에 식별할 수 있는 버그가 있다. Question.was_published_recently() 메서드는 Question의 pub_date가 미래로 설정되어 있어도 True를 반환한다.
```python
def was_published_recently(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    # pub_date가 비교대상보다 크거나 작으면 되기 때문에 미래에도 True를 반환한다.
```
python manage.py shell을 통해 미래의 날짜로 메서드를 실행해보면 버그를 확인 할 수 있다.

#### 테스트 파일 만들기
어플리케이션 테스트는 일반적으로 test.py 파일에 있다. 테스트 시스템은 test로 시작하는 파일에서 테스트를 자동으로 찾는다.   
   
테스트를 작성하고 python manage.py test polls를 실행해보면 테스트에 버그가 검출된다.   
* FAIL: test_was_published_recently_with_future_question (polls.tests.QuestionModelTests)   
  * AssertionError: True is not False
   
이는 이하의 과정을 거친 것이다.
* manage.py test polls는 polls 어플리케이션에서 테스트를 찾는다.
* django.test.TestCase 클래스의 하위 클래스인 QuestionModelTests를 찾았다.
* 테스트 목적으로 특별한 데이터베이스를 만든다.
* 이름이 test로 시작하는 테스트 메서드를 찾는다.
* test_was_published_recently_with_future_question 메서드에서 pub_date필드가 30일 미래인 Question 인스턴스를 생성한다.
* assertIs() 메소드를 사용하여, was_published_recently()는 False가 아니라 True를 반환한다는 것을 발견하여 알린다.

##### 위 과정에서 알 수 있는 것
* 테스트 클래스는 TestCase를 상속해야 한다. 
* 테스트 메서드는 이름이 test로 시작해야 한다. 
* assertIs()를 이용하여 원하는 결과와 비교한다.

### 버그 수정
models.py에서 날짜가 과거에 있을 때에만 True를 반환하도록 메소드를 수정한다.
```python
def was_published_recently(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
# 에서

def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now
# 로 수정한다.
```
보다 포괄적인 테스트를 위해, 이 경우에는 과거, 최근, 미래의 question이 올바른 값을 반환한다는 것을 보장하기 위한 테스트를 추가한다.
```python
# polls/tests.py
def test_was_published_recently_with_old_question(self):
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)

    self.assertIs(old_question.was_published_recently(), False)

def test_was_published_recently_with_recent_question(self):
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)

    self.assertIs(recent_question.was_published_recently(), True)
```

### 뷰에 대한 테스트
Django는 뷰 레벨에서 코드와 상호 작용하는 사용자를 시뮬레이트 하기 위해 테스트 클라이언트 클래스 client를 제공한다. 이 테스트 클라이언트는 test.py 또는 shell에서 사용 할 수 있다.

#### shell에서 사용
shell에서 사용하려면 테스트 환경을 구축해야 한다.
```python
# python manage.py shell

from django.test.utils import setup_test_environment
setup_test_environment()
# response.content와 같은 추가적인 속성을 사용할 수 있게 하기 위해서 setup_test_environment()를 사용하여 템플릿 renderer 를 설치한다.

from django.test import Client
client = Client()
# 테스트 클라이언트 클래스를 import한다.

response = client.get('/')
response.status_code
# /를 찾을 수 없다 출력된다.
# 그렇기에 status_code를 물어도 404이다.

from django.urls import reverse
response = client.get(reverse('polls:index'))
response.status_code
# reverse를 사용하여 URL을 입력하면 연결이 되고 status_code는 200이 된다.

response.content
response.context['latest_question_list']
# response의 content를 확인하면 내용이 정상 출력된다.
```

### 뷰 개선
아직 설문조사 목록에 게시되지 않은 설문조사(pub_date가 미래인 설문조사)가 표시된다. 이를 수정해야 한다.
```python
# polls/views.py
# class IndexView의 메서드
def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
    # 가장 나중의 5개를 보여준다. 그러나 그 5개에 장래에 표시되게 할 question이 포함된다.

# 위 메서드를 아래와 같이 변경한다.
def get_queryset(self):
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]
    # filter를 통해 question 중에서 timezone.now보다 pub_date가 작거나 같은 것만을 골라낸다.
```

### 뷰 테스트 작성
shell에서 테스트 한 것을 기반으로 테스트 코드를 작성한다. 이 테스트 코드는 다음을 충족하기 위한 것이다.
* 과거와 미래 날짜의 questions이 생성되고, 퍼블리시된 것들만 리스트에 나타나야 한다. 즉, 과거의 현재의 questions은 나타나되 미래의 questions은 숨겨져야 한다.
* 앞으로 변화가 있더라도 이러한 점에는 영향을 끼치지 않게 한다.
* 모든 상태와 시스템 상태의 모든 새로운 변경 사항에 대해 예상한 결과가 출력되어야 한다.
   
#### 디테일 뷰 테스트
미래의 설문은 목록에 나타나지 않지만 사용자가 URL을 알고 있거나, 추측하면 접근 할 수 있다. 그러므로 디테일 뷰에 제약조건을 추가할 필요가 있다. 

### 테스트에 관하여
* 테스트는 많이 할 수록 좋다.
  * 테스트가 너무 비대하게 느껴질 수도 있다. 하지만 그렇게 작성한 테스트는 한번 작성하고 신경을 쓰지 않아도 어플리케이션을 개발하는 동안 계속 작동할 것이다.
* 테스트도 업데이트 해야한다.
  * 테스트 결과를 최신으로 유지하기 위해 어떤 테스트를 수정해야 하는지 알려주므로 테스트는 테스트를 개선할 수 있도록 도와준다.
* 테스트를 현명하게 관리하라.
  * 각 모델이나 뷰에 대한 별도의 TestClass를 적용하라.
  * 테스트하려는 각 조건 집합에 대해 분리된 테스트 방법을 갖추어라.
  * 기능을 설명하는 테스트 메서드 이름을 사용하라.
* 어플리케이션에서 테스트되지 않은 부분을 탐지하는 좋은 방법은 코드 커버리지를 확인하는 것이다.
  * 테스트 커버리지는 깨지기 쉬운 코드, 죽은 코드를 식별하는데 도움을 준다.
  * 코드를 테스트 할 수 없다는 것은 대개 코드를 리팩토링하거나 제거해야 한다는 뜻이다.