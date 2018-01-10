from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from django.template.loader import render_to_string

from lists.views import home_page


# Create your tests here.
class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'Um novo item na Lista'})
        self.assertIn('Um novo item na Lista', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
