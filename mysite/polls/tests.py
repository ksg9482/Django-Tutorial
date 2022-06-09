import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# TestCase의 하위 클래스
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)
# 이 테스트로 인해 recent_question은 생성부터 23시간59분까지만 '최근'에 생성된 것임을 보장받게 되었다

# 이하는 question을 생성하는 함수와 테스트를 생성하는 클래스이다.
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
    # 테스트 과정중 question을 생성하는 부분에서 반복 사용된다.

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        # 연결, 사용가능한 투표가 없음, question리스트가 비어 있음을 확인한다.

    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )
        # question을 생성하고 그 question이 리스트에 나타나는지 확인한다.

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        # 미래의 pub_date로 질문을 생성한다. pub_date가 now보다 크면 filter로 걸러지기 때문에 인덱스에 질문이 없어야 한다.
        # 데이터베이스는 각 테스트 메서드마다 초기화 되므로 인덱스에 질문이 없어야 한다.

    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        # pub_date가 미래인 question에 접근할 경우 404를 리턴한다

    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)
        # pub_date가 과거인 question에 접근할 경우 해당 페이지를 리턴한다