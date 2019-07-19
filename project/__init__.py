# Importing all needed Flask classes
from flask import Flask, render_template, session, flash, redirect, url_for, session

# Importing session
from flask_sessionstore import Session


# Importing os to encode session variable
import os

# Importing redis for larger session
import  urllib.parse


# from redis import Redis
import redis
from rq import Worker, Queue, Connection

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

ssl._create_default_https_context = ssl._create_unverified_context

# Defing app which is nessisary for flask to run
app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(homepage)

app.register_blueprint(users)

app.register_blueprint(dashboard)

app.register_blueprint(api)

sslify = SSLify(app)
SESSION_TYPE = 'redis'

# redis_url = os.getenv('REDISTOGO_URL')

# urllib.parse.uses_netloc.append('redis')
# url = urllib.parse.quote_plus(redis_url)
# conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)

redis_url = os.getenv('REDISTOGO_URL', 'redis://h:p9cd965813270ce4f4585a9a45fe132dce4eab7d54896910bf8ec61c9dcdea3af@ec2-3-221-178-194.compute-1.amazonaws.com:17279')
redis = redis.from_url(redis_url)

# Config
app.config.from_pyfile('appConfig.cfg')

# External flask session library
app.config.from_object(__name__)
Session(app)

@app.route('/')
def root():
	return redirect(url_for(homepage.home))


if __name__ == '__main__':
	with Connection(conn):
	    worker = Worker(map(Queue, listen))
	    worker.work()

