# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, session

# Importing os to encode session variable
import os

# Importing Views
from project.homepage.views import homepage

from project.users.views import users

from project.dashboard.views import dashboard

from project.api.views import api

# Importing Time
from datetime import timedelta

# Redis
import redis

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)


# Defing app which is nessisary for flask to run
app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(homepage)

app.register_blueprint(users)

app.register_blueprint(dashboard)

app.register_blueprint(api)


# Key Config
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.config['DEBUG'] = False


SESSION_TYPE = 'filesystem'

@app.route('/')
def root():
	return redirect(url_for(homepage.home))