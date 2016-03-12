# coding=utf-8
from contextlib import contextmanager
from functools import wraps
import json
import pprint
import logging
import sys
import os

import requests
from requests.exceptions import HTTPError


def get_base():
    try:
        return sys.argv[1]
    except IndexError:
        return 'http://127.0.0.1:5000'


BASE_URL = get_base()
JSON_CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache.json')
local_cache = {}
log = logging.getLogger(__name__)


def get_with_headers(requests_get):
    """Decorator, refresh "Session" header if expired."""
    session_header = dict(Session=None)

    @wraps(requests_get)
    def wrapper(url, **kwargs):
        kwargs['headers'] = session_header

        try:
            response = requests_get(url, **kwargs)
            response.raise_for_status()

        except HTTPError as e:
            # noinspection PyUnboundLocalVariable
            if response.json().get('error'):
                session_header['Session'] = requests_get('{}/get-session'.format(BASE_URL)).text
                kwargs['headers'] = session_header
                response = requests_get(url, **kwargs)
            else:
                raise e

        log.info('GET:{}\nResponse:{}'.format(url, response.text))
        return response

    return wrapper


@contextmanager
def ignored(*exception):
    """Standard utility, ignore exception."""
    try:
        yield
    except exception:
        pass


@contextmanager
def saved_cache(file_path):
    """Load and save cache."""
    global local_cache

    try:
        with ignored(IOError):
            local_cache = json.load(open(file_path))
        yield
    finally:
        json.dump(local_cache, open(file_path, 'wb'), sort_keys=True, indent=2, separators=(',', ': '))


def cache_handler(item):
    """Retrieve item from cache, use requests to populate if missing."""
    try:
        if item not in local_cache:
            response = requests.get('{}/{}'.format(BASE_URL, item))
            response.raise_for_status()
            response_json = {k.lower(): v for k, v in response.json().items()}
            local_cache[item] = response_json
        else:
            log.debug('Cache:\n{}:\n{}'.format(item, pprint.pformat(local_cache.get(item))))

        return local_cache.get(item)
    except HTTPError as e:
        raise e


def get_next(next_list):
    """Recursive generator, follow chained URL directives, yield secret keys."""

    # do not iterate through strings
    next_list = [next_list] if isinstance(next_list, basestring) else next_list

    log.debug('\n'
              '{1:=<70}\n'
              'Next List\n'
              '{1:-<70}\n'
              '{0}\n'
              '{1:=<70}'.format('\n'.join(next_list), ''))

    for item in next_list:
        json_response = cache_handler(item)
        try:
            next_item = json_response['next']
        except KeyError, e:  # Found a dead end in the node tree.
            if 'secret' in json_response:
                yield json_response.get('secret')
                continue
            else:
                # Report an actual problem.
                log.warning('{}:{}:{}'.format(e, item, json_response))
                raise e

        # Iterate through each item in ``next_item`` list.
        yield ''.join(list(get_next(next_item)))


# monkeypatch requests get
requests.get = get_with_headers(requests.get)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('requests').setLevel(logging.INFO)

    with saved_cache(JSON_CACHE_FILE):
        start = cache_handler('start')

        list_of_secret_letters = list(get_next(start['next']))
        secret_message = ''.join(list_of_secret_letters)

        print secret_message
