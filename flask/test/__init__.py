from __future__ import unicode_literals

import os
import subprocess
import time
import unittest
import threading
import sqlalchemy.exc
from sqlalchemy import create_engine
from werkzeug.serving import make_server
from splinter.driver.webdriver.firefox import WebDriver

import db
from db import session
from web import app


db_info = {}
web_actors = {}


class TestCase(unittest.TestCase):
    def setUp(self):
        session().commit = session().flush
        self.browser = web_actors['browser']

    def tearDown(self):
        session().rollback()

    def visit(self, path):
        self.browser.visit('http://localhost:65432' + path)


def setUpPackage():
    create_temp_database()
    apply_migrations()

    server = make_server('0.0.0.0', 65432, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    web_actors['server'] = server

    web_actors['browser'] = SingleVisitFirefoxDriver()


def tearDownPackage():
    web_actors['browser'].quit()
    terminate_query = """
        select pg_terminate_backend({0})
        from pg_stat_activity
        where datname = '{1}'
    """
    try:
        db_info['master_engine'].execute(
            terminate_query.format('procpid', db_info['temp_db_name']))
    except sqlalchemy.exc.ProgrammingError as e:
        if '"procpid" does not exist' in str(e):
            #postgres 9.2 changed pg_stat_activity.procpid to just .pid
            db_info['master_engine'].execute(
                terminate_query.format('pid', db_info['temp_db_name']))
        else:
            raise
    drop_temp_database()


def create_temp_database():
    db_info['master_engine'] = create_engine('postgresql://localhost/postgres')
    db_info['temp_db_name'] = 'splinter_demo_test_{0}'.format(int(time.time()))
    conn = db_info['master_engine'].connect()
    conn.execute('commit')  # work around sqlalchemy's auto-transactions
    conn.execute('create database {0}'.format(db_info['temp_db_name']))
    db_info['temp_db_url'] = 'postgresql://localhost/{0}'.format(
        db_info['temp_db_name'])
    db_info['engine'] = create_engine(db_info['temp_db_url'])
    db.ENGINE = db_info['engine']


def apply_migrations():
    migrations_dir = os.path.join(os.path.dirname(__file__),
                                  '..',
                                  'migrations')
    subprocess.check_output(['yoyo-migrate',
                             '-b',
                             'apply',
                             migrations_dir,
                             db_info['temp_db_url']])


def drop_temp_database():
    conn = db_info['master_engine'].connect()
    conn.execute('commit')
    conn.execute('drop database {0}'.format(db_info['temp_db_name']))


class SingleVisitFirefoxDriver(WebDriver):
    def visit(self, url):
        self.driver.get(url)
