import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

#Question 모델
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

# Choice 모델
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # question_id로 외부키가 설정된다.
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

"""
모델이란 부가적인 메타데이터를 가진 데이터베이스의 구조(layout)를 말한다.
모델은 데이터에 대한 단 하나의 확실한 정보 출처이며 저장중인 데이터의 필수 필드 및 동작이 포함된다. 

모델의 목표는 데이터 모델을 한 곳에서 정의하고 데이터 모델을 자동으로 파생하는 것이다.
여기에는 migration이 포함된다. migration은 모두 모델 파일에서 파생되며, 기본적으로 Django가
데이터베이스 스키마를 현재의 모델에 도달 할 수 있게 해주는 기록이다.

각 모델은 django.db.models.Model의 하위 클래스로 표현된다. 여러 클래스 변수가 있으며 각 클래스 변수는 모델에서 데이터베이스 필드를 나타낸다.
Field 클래스의 생성자에 인수를 전달하여 이름을 지정 할 수 있다. 이 방법은 Django의 내부를 설명하는 용도로 종종 사용되며 
이 예제에선 Question.pub_date에 한해서 이름을 정의 했다.

몇몇 Field 클래스들은 필수 인수가 필요하며 다양한 선택적인 인수를 가질 수 있다.
예를 들어 CharField는 max_length가 필수이다.
"""

"""
__str__() 메서드를 추가한 이유: 
객체의 표현을 대화식 트롬프트에서 편하게 보려는 이유,
Django가 자동으로 생성하는 관리 사이트에서도 객체의 표현이 사용되기 때문이다.
"""