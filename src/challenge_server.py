#!/usr/bin/env python
# coding=utf-8
import json
import logging.handlers
import os
from functools import wraps
from hashlib import md5
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_caching.backends import FileSystemCache


app = Flask(__name__)
log_file = os.path.join(os.path.dirname(__file__), "challenge_server.log")
file_handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=1024 * 1024, backupCount=5
)
logging.getLogger("werkzeug").setLevel(logging.INFO)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)


cache = FileSystemCache("./tmp/.cache", default_timeout=300)


try:
    with open("message.json") as f:
        secret_message = json.load(f)
except IOError:
    raise RuntimeError(
        "Use %r to create the database first. %r not found. \n"
        "Shutting down..." % ("make migrate", "message.json")
    )


def response_error(message, status_code):
    response = jsonify(error=message)
    response.status_code = status_code
    return response


def validate_session(function):
    session_missing_message = (
        '"Session" header is missing. "/get-session" to get a session id.'
    )
    session_expired_message = "Invalid session id, a token is valid for 10 requests."

    @wraps(function)
    def wrapper(*args, **kwargs):
        session = request.headers.get("Session")
        app.logger.debug("Session: %s" % session)
        if not session:
            return response_error(session_missing_message, 401)

        if not cache.has(session):
            return response_error(session_expired_message, 403)

        if cache.get(session) <= 0:
            return response_error(session_expired_message, 403)

        cache.dec(session)
        app.logger.info("Key: %s, Value: %s" % (session, cache.get(session)))
        return function(*args, **kwargs)

    return wrapper


@app.route("/")
def index():
    return 'On the right track. You can start here: "/start" '


@app.route("/start", defaults={"page_id": "start"})
@app.route("/<uuid:page_id>")
@validate_session
def start(page_id):
    try:
        return jsonify(secret_message[str(page_id)])
    except KeyError:
        return response_error("Page not found", 404)


@app.route("/get-session")
def get_session():
    key = str(uuid4())
    cache.set(key, 10, timeout=60)

    app.logger.info("New Key: %s" % key)

    return key


app.logger.info("Server routes registered.")


def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()
