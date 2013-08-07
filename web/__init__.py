from __future__ import unicode_literals

from flask import Flask, render_template, request
from db import User, session

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html.jinja')


@app.route('/', methods=["POST"])
def signup():
    user = User(email=request.form['email'])
    session().add(user)
    session().commit()
    return render_template("signed_up.html.jinja")
