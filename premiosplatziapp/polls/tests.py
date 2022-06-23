import datetime

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_quetions = Question(question_text="¿Quien es el mejor Course Director de Platzi?", pub_date = time)
        self.assertIs(future_quetions.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=2)
        past_quetions = Question(question_text="¿Quien es el mejor Programador de Platzi?", pub_date = time)
        self.assertIs(past_quetions.was_published_recently(), False)

    def test_was_published_recently_with_recently_questions(self):
        """was_published_recently returns True for questions whose pub_date less than a day"""
        time = timezone.now() - datetime.timedelta(days=0.5)
        recently_quetions = Question(question_text="¿Quien es el mejor Programador de Platzi?", pub_date = time)
        self.assertIs(recently_quetions.was_published_recently(), True)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are availables")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])