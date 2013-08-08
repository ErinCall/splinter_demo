from __future__ import unicode_literals

from test import TestCase
from web import app
from db import session, User
from nose.tools import eq_


class TestSignup(TestCase):
    def test_sign_up(self):
        app.test_client().post('/', data={'email': 'andrew@lorente.name'})

        users = session().query(User.email).all()
        eq_(users, [('andrew@lorente.name',)])

        self.visit('/')
        self.browser.fill('email', 'joe@lewis.name')
        self.browser.find_by_name('go').click()
        assert self.browser.is_text_present('Thanks'), 'rude!'

        users = session().query(User.email).all()
        eq_(users, [('andrew@lorente.name',), ('joe@lewis.name',)])
