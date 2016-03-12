# coding=utf-8
import logging
import sys
from functools import partial
from textwrap import dedent
from urlparse import urljoin

import requests
from requests.exceptions import HTTPError

#
# GLOBALS
# ============================================================================

log = logging.getLogger(__name__)
try:
    url = partial(urljoin, sys.argv[1])
except IndexError:
    url = partial(urljoin, 'http://127.0.0.1:5000')

headers = {}


#
# CORE
# ============================================================================

def get_next_secret(path):
    """Recursively follow a path to yield secrets."""

    # Setup, get next resource
    response = request_next(url(path))
    # clean response data
    response_data = normalize_keys(response.json())

    # Guard, response is a leaf
    if 'secret' in response_data:
        secret = response_data['secret']
        log_secret_found(secret, url(path))
        yield secret

    else:
        next_list = response_data['next']
        log_next_list(next_list)

        # traverse each child branch
        for next_path in next_list:
            # yield from results
            for next_secret in get_next_secret(next_path):
                yield next_secret


def request_next(path, is_retry=False):
    """Handle requests with custom headers."""

    # Setup, get resource
    response = requests.get(url(path), headers=headers)

    # handle 404 response
    try:
        response.raise_for_status()
    except HTTPError as e:

        # Guard, infinite loop
        if is_retry:
            log_response_error('Unable to refresh "Session" token.', headers['Session'], url(path), response.json())
            raise e

        # Guard, unexpected error
        if not response.json().get('error'):
            log_response_error('"error" key missing from response.', headers['Session'], url(path), response.json())
            raise e

        # request new Session header
        headers['Session'] = requests.get(url('get-session')).text
        log.info('New "Session" token: %s', headers['Session'])

        # retry request with updated headers
        return request_next(path, is_retry=True)

    log.info('GET %s', url(path))
    log.debug('Response: %s', response.text)
    return response


#
# UTILS
# ============================================================================

def normalize_keys(data):
    """Convert keys to lowercase"""
    return {k.lower(): v for k, v in data.items()}


#
# LOG UTILS
# ============================================================================

def log_next_list(next_list):
    template = dedent("""

        {log_header_1}
        Next list
        {log_header_2}
        {next_list}
        {log_header_1}
    """[1:])
    template_vars = {
        'log_header_1': '=' * 70, 'log_header_2': '-' * 70, 'next_list': '\n'.join(next_list)
    }

    log.debug(template.format(**template_vars))


def log_secret_found(secret, url):
    template = dedent("""

        {log_header_1}
        Secret Found
        {log_header_2}
        Url: {url}
        Secret: {secret}
        {log_header_1}
    """[1:])
    template_vars = {
        'log_header_1': '-' * 70, 'log_header_2': '~' * 70, 'url': url, 'secret': secret
    }

    log.debug(template.format(**template_vars))


def log_response_error(message, session, full_url, response):
    log.error(message)
    log.error('  - SESSION: %s', session)
    log.error('  - URL: %s', full_url)
    log.error('  - RESPONSE: %s', response)


#
# MAIN
# ============================================================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('requests').setLevel(logging.INFO)

    print ''.join(get_next_secret('start'))
