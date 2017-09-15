# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question

# Create your tests here.


def create_question(question_text, days):
    """
    Creates question with given text and days offset to now
    Negative days indicates in the past, positive in the future.
    """
    
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text = question_text, pub_date = time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions are available, a suitable message should be displayed
        """

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")

        self.assertQuerysetEqual(response.context['lastest_question_list'], [])
 

    def test_index_with_a_past_question(self):
        """
        Questions with pub_dates in the past should be displayed on the index pg
        """
  
        create_question(question_text="This is a past question.", days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: This is a past question.>']) 


    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """ 
        recently_published() should return 0 for future questions
        """    

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)

        self.assertIs(future_question.recently_published(), False)


    def test_was_published_recently_with_old_question(self):
        """
        recently_published() should return 0 for q with pub_date > 1 day 
        """

        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date = time)
 
        self.assertIs(old_question.recently_published(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        recently_published() should return 1 for q with pub_date <= 1 day
        """

        time = timezone.now() - timezone.timedelta(hours = 1)
        recent_question = Question(pub_date = time)

        self.assertIs(recent_question.recently_published(), True)

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
