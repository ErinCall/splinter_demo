from __future__ import unicode_literals

import os
import subprocess
import time
import unittest
from sqlalchemy import create_engine
import sqlalchemy.exc
import db
from db import session


class TestCase(unittest.TestCase):
    def setUp(self):
        session().commit = session().flush

    def tearDown(self):
        session().rollback()

db_info = {}


def setUpPackage():
    create_temp_database()
    temp_db_url = 'postgresql://localhost/{0}'.format(db_info['temp_db_name'])
    db_info['engine'] = create_engine(temp_db_url)
    db.ENGINE = db_info['engine']

    apply_migrations(temp_db_url)


def tearDownPackage():
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


def apply_migrations(temp_db_url):
    migrations_dir = os.path.join(os.path.dirname(__file__),
                                  '..',
                                  'migrations')
    subprocess.check_output(
        ['yoyo-migrate', '-b', 'apply', migrations_dir, temp_db_url])


def drop_temp_database():
    conn = db_info['master_engine'].connect()
    conn.execute('commit')
    conn.execute('drop database {0}'.format(db_info['temp_db_name']))
