# 첫번째 장고 앱 작성하기 part 6

## 정적 파일
서버에서 생성된 HTML을 제외하고, 웹 어플리케이션은 일반적으로 전체 웹 페이지를 렌더링하는데 필요한 추가 파일을 제공해야 한다. 
* 이미지
* JavaScript 또는 CSS 등
이러한 파일을 Django에서는 정적파일(Static Files)이라 부른다. 소규모 프로젝트일 경우 정적파일을 간단히 보관할 수 있으므로 큰 문제가 되지 않는다. 그러나 대규모 프로젝트일 경우 각 어플리케이션에 제공하는 여러 정적파일 세트를 처리하는 것이 까다로워 진다.   
   
이를 처리하는 것이 django.contrib.staticfiles의 목적이다. 이는 각 어플리케이션의 정적 파일들을 프로덕션 환경에서 쉽게 제공 할 수 있는 단일 위치로 수집한다.

### 어플리케이션의 모양을 바꾸기
polls 디렉토리에 static 디렉토리를 생성한다. Django는 템플릿을 찾는 것과 비슷하게 polls/static에서 정적 파일을 찾는다.   
   
Django의 STATICFILES_FINDERS 설정은 다양한 소스에서 정적 파일을 찾는 방법을 알고 있는 파인더 목록을 가지고 있다. 기본값 중 하나는 AppDirectoriesFinder인데, INSTALLED_APPS에서 'static' 하위 디렉토리를 찾는다.   
   
polls 어플리케이션의 경우 polls/static/polls 내부에 정적 파일이 있어야 한다. style.css를 생성해야 한다면 그 위치는 polls/static/polls/style.css이다. 이 위치는 단순히 polls/style.css 라고 부를 수 있다.
* 다른 polls 디렉토리를 생성하지 않고 polls/static에 직접 정적 파일을 저장하는 것은 좋은 생각이 아니다. 
  * Django는 이름이 일치하는 첫 번째 정적 파일을 선택한다.
  * 다른 어플리케이션에 같은 이름의 정적 파일이 있으면 Django는 이를 구분할 수 없다.

#### style.css의 적용
polls/static/polls/style.css를 생성하고 적용하려면 템플릿에 css를 추가해야 한다.
```python
#  polls/templates/polls/index.html
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}">
```
* {% load static %} static 템플릿 태그는 정적 파일의 절대 URL을 생성한다.

#### 배경 이미지 적용
이미지 용 하위 디렉토리 즉, polls/static/polls/images/를 생성한다. 이 디렉토리 안에 background.gif를 넣고 style.css에 이하를 추가 한다.
```python
#  polls/static/polls/style.css
body {
    background: white url("images/background.gif") no-repeat;
}
```
* 스타일시트와 같은 Django가 생성하지 않은 정적 파일에는 {% static %} 템플릿 태그를 사용할 수 없다. 정적 파일을 서로 연결 할 때에는 항상 상대경로를 이용해야 한다. 그러면 정적 파일의 여러 경로를 수정할 필요 없이 STATIC_URL을 변경할 수 있다.
  * STATIC_URL: static 템플릿 태그에서 URL을 생성하는데 사용된다.