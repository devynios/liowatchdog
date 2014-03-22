#!/usr/bin/env python

from flask import Flask, render_template, request, url_for, redirect, session, flash, Response
from datetime import datetime as time
from functools import wraps
import os

# ---------------
# SETTINGS
# login settings
USERNAME = 'user'
PASSWORD = 'password'

# server settings
HOST = '0.0.0.0'
PORT = 8000

#
REFRESH = 20
TIMEOUT = 20

#----------------

# local store for state
store = {}

app = Flask(__name__)

# loading default settings from this file
app.config.from_object(__name__)

# loads settings from file in CHECKSTATUS_SETTINGS envvar
# e.g. export CHECKSTATUS_SETTINGS='/etc/default/checkstatus.cfg' ->
# -> loads from checkstatus.cfg
app.config.from_envvar('CHECKSTATUS_SETTINGS', silent=True)

# as per http://flask.pocoo.org/snippets/8/, I like this solution tbh


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == app.config['USERNAME'] and password == app.config['PASSWORD']


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def is_suspicious(form):
    """
    Returns True if user seems to be suspicious
    Current criteria - more than one uniq user logged in
    """
    return len(set(form['user'].split('\n'))) > 1


def make_data(form):
    """
    Constructs a tuple (primary_key, value) for logging
    primary_key in this case is computer's MAC address
    value is dictionary of given information (ip, mac, uptime, username, submit time)
    """
    return (form['mac'], {
        'ip': form['ip'],
        'mac': form['mac'],
        'uptime': form['uptime'],
        'users': set(form['user'].split('\n')),
        'warning': is_suspicious(form),
        'submitted': int(time.now().strftime('%s'))
    })


@app.route("/submit/", methods=["POST"])
def submit():
    """
    Logs user sent data.
    """
    key, val = make_data(request.form)
    store[key] = val
    return ''


@app.route("/", methods=["GET"])
@requires_auth
def status():
    """
    Status page, if user is logged in - shows status,
    otherwise throws httpauth
    """
    return render_template(
        'status.html',
        clients=store,
        now=int(time.now().strftime('%s')),
        refresh=app.config['REFRESH'],
        delay=app.config['TIMEOUT'])  # delay in seconds till announcing client as 'MIA'


if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'])
