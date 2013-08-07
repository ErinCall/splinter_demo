from __future__ import unicode_literals

from test import TestCase
from web import app
from db import session, User
from nose.tools import eq_


class TestSignup(TestCase):
    def test_sign_up(self):
        app.test_client().post('/', data={'email': 'andrew@lorente.name'})

        users = session().query(User).all()
        eq_(len(users), 1)
        eq_(users[0].email, 'andrew@lorente.name')

        self.visit('/')
        self.browser.fill('email', 'andrew@lorente.name')
