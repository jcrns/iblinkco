# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, session

# Session lib for increase session
from flask_session import Session

# Importing os to encode session variable
import os

# Importing Views
from project.homepage.views import homepage

from project.users.views import users

from project.dashboard.views import dashboard

from project.api.views import api

# Importing ssl
import ssl

# Importing http redirect library
from flask_sslify import SSLify

# Importing Time
from datetime import timedelta

# Adding flask mail for email verification and password reset
from flask_mail import Mail, Message

ssl._create_default_https_context = ssl._create_unverified_context

# String serializer library
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

# Defing app which is nessisary for flask to run
app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(homepage)

app.register_blueprint(users)

app.register_blueprint(dashboard)

app.register_blueprint(api)

sslify = SSLify(app)

# Session config
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=40000)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_THRESHOLD'] = 500  

sess = Session()
sess.init_app(app)

# Config file link
app.config.from_pyfile('appConfig.cfg')


safeTimedUrlSerializer = URLSafeTimedSerializer(app.secret_key)

# Initializing email functions
mail = Mail(app)

# External flask session library
app.config.from_object(__name__)

@app.route('/')
def root():
	return redirect(url_for(homepage.home))


# if __name__ == '__main__':
# 	with Connection(conn):
# 	    worker = Worker(map(Queue, listen))
# 	    worker.work()

