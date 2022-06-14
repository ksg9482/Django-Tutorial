# 첫번째 장고 앱 작성하기 part 7

## 관리자 사이트 커스터마이징
Question 모델을 admin.site.register에 등록하는 것으로 Django는 디폴트 폼을 구현 할 수 있다.
```python
# polls/admin.py
admin.site.register(Question)
# register에 QuestionAdmin을 등록한다.
admin.site.register(Question, QuestionAdmin)
```
모델의 관리자 옵션을 변경해야 할경우 위 패턴을 적용하면 된다.
* 모델 관리자(어드민)클래스 생성 후, admin.site.register에 두번째 인수로 전달.

### filedsets 분리
많은 수의 필드가 있는 관리 폼의 경우 폼을 fieldsets으로 분할 하는 것이 좋다.   
fieldsets의 각 튜플 첫번째 요소는 필드셋의 제목이다.   

#### 관련된 객체 추가
* 방법 1. Choice를 관리자에 등록한다.
  * admin.site.register(Choice)
  * 방법은 Question을 추가하는 것과 같다.
register에 Choice를 등록하면 관리자 페이지에서 Add choice로 사용 할 수 있다. Add choice 페이지의 Question필드는 데이터베이스의 모든 질문을 포함하는 선택창이다. Django는 ForeignKey가 admin에서 <select>로 표현되어야 한다는 것을 안다. Question 옆에는 Add Another가 있는데 ForeignKey 관계를 가진 모든 객체는 이 링크가 존재한다. 해당 페이지지를 통해 조작하고 저장하면 Django는 데이터베이스에 자료를 저장하고 동적으로 이를 폼에 추가한다.   
   
그러나 이는 비효율적인 방법이다.   
   
* Inline 선언을 사용한다.
```python
class ChoiceInline(admin.stackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Data information', {'fields': ['pub_date'], 'classes':['collapse']})
    ]
    inlines = [ChoiceInline]
```
위 코드는 Choice 객체는 Question 관리자 페이지에서 편집되고, 기본적으로 3가지 선택 항목을 제공한다. 
* 모든 필드를 표시하는데 많은 화면 공간이 필요할 경우 admin.TabularInline을 이용한다
  * class ChoiceInline(admin.TabularInline)
  * TabularInline은 stackedInline 보다 좀 더 조밀하고 테이블 기반 형식으로 표현된다.
기본적으로 Django는 각 객체의 str()을 표시한다. 그러나 개별 필드를 표시하기 원하는 경우에는 list_display 옵션을 사용한다. 이 옵션은 객체의 변경 목록 페이지에서 열로 표시할 필드 이름들의 튜플이다.
```python
listPdisplay = ('question_text', 'pub_date', 'was_published_recently')
```
was_published_recently를 제외하고 머리글을 클릭하여 그 값으로 정렬 할 수 있다. 임의의 메서드의 출력에 의한 정렬은 지원하지 않기 때문이다. 하지만 display() 데코레이터를 메서드에 사용하면 개선 할 수 있다.
#### display() 데코레이터
```python
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
```
* 머리글을 Published recently?로 설정하고 pub_date로 정렬한다.
그리고 pub_date 필드에 의해 변경 목록을 필터링 할 수 있도록  QuestionAdmin에 list_filter = ['pub_date']을 추가한다.   
   
pub_date는 DateTimeField이므로 여러 적절한 필터 옵션을 기본적으로 제공해준다.

#### 검색창 추가
```python
search_fields = ['question_text']
```
변경 목록 맨 위에 검색 창이 추가 된다. 검색어를 입력하면 Django는 question_text를 검색한다. 그러나 내부적으로 LIKE 쿼리를 이용하기 때문에 검색 필드의 수를 적당하게 제한해야 데이터베이스 검색을 더 쉽게 할 수 있다.

### 프로젝트 템플릿 커스터마이징
프로젝트 디렉토리(manage.py가 있는)에 template 디렉토리를 만들고 mysite/settings.py을 수정한다.
*  TEMPLATES 설정에 DIR 옵션을 추가한다. 
  * 'DIRS': [BASE_DIR / 'templates']
DIRS는 Django가 템플릿을 로드할 때 파일을 검사하는 경로이다. DIR이 기본 설정대로 비어 있어도 APP_DIRS = True이기에 Django는 각 어플리케이션 페이지 내에서 templates/ 서브 디렉토리를 자동으로 찾아서 대체한다.
templates 디렉토리에 admin 디렉토리를 만들고 admin/base_site.html(django/contrib/admin/templates)을 해당 디렉토리에 복사한다.
* Django 소스파일을 찾기 힘든 경우
  * python -c "import django; print(django.\_\_path\_\_)"
파일을 편집하여 적합한 사이트 이름으로 변경한다.
* {{ site_header|default:_('Django administration') }}을 수정한다.
* 실제 프로젝트에서는 django.contrib.admin.AdminSite.site_header 속성을 사용하여 커스터마이징을 더욱 쉽게 할 수 있다.
* {%와 {{태그느 Django의 템플릿 언어이다. 이 템플릿 언어는 최종 HTML 페이지를 생성하기 위해 평가 된다.
