#!/usr/bin/env python
# coding=utf-8
from functools import wraps
import json
import os
from hashlib import md5

from flask import Flask, jsonify, request


app = Flask(__name__)

try:
    # noinspection PyUnresolvedReferences
    from redislite import StrictRedis
    # noinspection PyUnresolvedReferences
    from werkzeug.contrib.cache import RedisCache

    cache_file = os.path.join(os.path.dirname(__file__), 'server_cache.rdb')

    cache = RedisCache(StrictRedis(cache_file))
except ImportError:
    from werkzeug.contrib.cache import SimpleCache

    cache = SimpleCache()
    app.logger.warning("redislite could not be imported. "
                       "Falling back to non-thread-safe caching")

try:
    with open('message.json') as f:
        secret_message = json.load(f)
except IOError:
    raise RuntimeError("Use %r to create the database first. %r not found. \n"
                       "Shutting down..." % (
                           'make migrate', 'message.json'))


def response_error(message):
    response = jsonify(error=message)
    response.status_code = 404
    return response


def validate_session(function):
    session_missing_message = ('"Session" header is missing. '
                               '"/get-session" to get a session id.')
    session_expired_message = ('Invalid session id, '
                               'a token is valid for 10 requests.')

    @wraps(function)
    def wrapper(*args, **kwargs):
        session = request.headers.get('Session')
        app.logger.debug("Session: %s" % session)
        if not session:
            return response_error(session_missing_message)

        elif cache.get(session) <= 0:
            return response_error(session_expired_message)
        else:
            cache.dec(session)
            app.logger.info("Key: %s, Value: %s" % (session, cache.get(session)))
            return function(*args, **kwargs)

    return wrapper


@app.route('/')
def index():
    return 'On the right track. You can start here: "/start" '


@app.route('/<page_id>')
@validate_session
def start(page_id):
    try:
        return jsonify(secret_message[page_id])
    except KeyError:
        return response_error('Page not found')


@app.route('/get-session')
def get_session():
    key = md5(os.urandom(32)).hexdigest()
    cache.set(key, 10, timeout=60)
    return key


@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    print 'Server shutting down...'
    return ""


if __name__ == '__main__':
    app.run(debug=True)
