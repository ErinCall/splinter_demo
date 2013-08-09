from __future__ import unicode_literals

import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from threading import Lock
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String)


SESSION = None
ENGINE = None


def session():
    global SESSION
    global ENGINE
    if ENGINE is None:
        ENGINE = create_engine(os.environ['DATABASE_URL'])
    if SESSION is None:
        SESSION = MutexSession(ENGINE)
    return SESSION

mutex = Lock()


class MutexSession(object):
    def __init__(self, engine):
        self._session = sessionmaker(bind=engine)()

        def define_function(name):
            def function(*args, **kwargs):
                mutex.acquire()
                try:
                    return getattr(self._session, name)(*args, **kwargs)
                finally:
                    mutex.release()
            return function
        for function_name in [
                'add',
                'flush',
                'commit',
                'rollback',
                'query',
                'execute',
                'delete']:
            function = define_function(function_name)
            setattr(self, function_name, function)
