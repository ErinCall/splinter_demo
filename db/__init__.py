from __future__ import unicode_literals

import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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
        SESSION = sessionmaker(bind=ENGINE)()
    return SESSION
