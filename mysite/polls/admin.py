from django.contrib import admin
from .models import Question

admin.site.register(Question)
"""
관리사이트에 Question 클래스가 있음을 알려준다.
"""