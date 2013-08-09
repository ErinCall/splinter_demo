"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from signups.models import User
from splinter_demo.test_runner import BROWSER


class TestSignup(TestCase):
    def visit(self, path):
        BROWSER.visit('http://localhost:65432' + path)

    def test_sign_up(self):
        Client().post('/', {'email': 'andrew@lorente.name'})
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, 'andrew@lorente.name')

        self.visit('/')
        BROWSER.fill('email', 'joe@lewis.name')
        BROWSER.find_by_name('go').click()
        assert BROWSER.is_text_present('Thanks'), 'rude!'

        users = User.objects.all()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[1].email, 'joe@lewis.name')

    def test_valid_emails_get_validated(self):
        self.visit('/')
        BROWSER.fill('email', 'eric@holscher.name')
        assert BROWSER.is_text_present('valid'), "didn't get validated"

    def test_invalid_emails_get_yelled_about(self):
        self.visit('/')
        BROWSER.fill('email', 'aghlaghlaghl')
        assert BROWSER.is_text_present('invalid'), "didn't get yelled at"
