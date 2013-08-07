from __future__ import unicode_literals

import os
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table import User

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html.jinja')


@app.route('/', methods=["POST"])
def signup():
    engine = create_engine(os.environ['DATABASE_URL'])
    session = sessionmaker(bind=engine)()
    user = User(email=request.form['email'])
    session.add(user)
    session.commit()
    return render_template("signed_up.html.jinja")
