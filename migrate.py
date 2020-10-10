#!/usr/bin/env python
# coding=utf-8
"""
This script generates the "database" for the server api.  In this case, it's only using
a json file.  It takes a secret message and expands it into a node tree of a determined
depth.  The characters of the message are revealed on the `MAX_DEPTH`.

The tree is dynamically generated, you're free to customize the message.
"""
import json
import logging
import re
from collections import deque
from hashlib import md5
from os import urandom
from random import randint, random, choice
from textwrap import wrap
from time import clock, time

END_MESSAGE = "Congratulations!  Send your solution to bionikspoon@gmail.com to receive your prize."
"""The message to be expanded by the node tree"""

START_MESSAGE = ("There is something I want to show you, "
                 "let's see if you can figure this out"
                 " by finding all of my secrets.")
"""This message is displayed on the start page
after the challenger gets past some early hurdles"""

MAX_DEPTH = 4
"""Depth of the message.  Used to test understanding of recursion and traversing nodes.
 The message expansion algorithm isn't too smart, if this is set too high, the first
 several layers will only share one directive to go to the next link."""

JSON_FILE = 'message.json'
"""Don't change this.  You can, but this is hardcoded into the makefile and the server."""

REDACTED_OUT = True
"""Redact `END_MESSAGE` from the build output.
Hopefully you tried to solve this before looking."""

logger = logging.getLogger(__name__)


def make_document(depth, **kwargs):
    """
    Impersonate mongodb document storage.

    The original puzzle was likely served from a mongodb, this is simulating that
    document structure.
    """
    random_and_unique_things = "{:f}{:f}{}".format(clock(), time(), urandom(32))
    kwargs['depth'] = depth
    kwargs['id'] = md5(random_and_unique_things).hexdigest()
    return kwargs


def get_next_key():
    """
    Introduce random typos into the key.

    A mild test in problem solving and normalizing data.
    """
    if random() < .9:
        return "next"
    else:
        typo = choice(("Next", "nExt", "neXt", "nexT", "NExt", "nEXt", "neXT", "NEXt", "nEXT", "NEXT"))
        logger.info("Purposely added a typo! %s", typo)
        return typo


def group_nodes(child_doc_list, group_depth):
    """
    Group layer into random sized chunks.

    The layer tree is built from the MAX_DEPTH up.  Each parent reveals up to 3
    children.
    **Note that depth 0 will wrangle together all children, even if it's
    more than 3.
    """
    child_doc_list = deque(child_doc_list)
    group = []
    while child_doc_list:
        try:
            parent_next = []
            for _ in xrange(randint(1, 4)):  # chunk size
                child_doc = child_doc_list.popleft()
                parent_next.append(child_doc['id'])

        except IndexError:
            break
        finally:
            next_dict = {get_next_key(): parent_next}
            group.append(make_document(group_depth, **next_dict))
    return group


def flatten_tree(groups):
    """
    Flatten layer groups into ONE key-value dict.

    While building, order and grouping matters.  For the server and the puzzle a flat
    structure makes more sense.
    """
    return {item['id']: item for data in groups for item in data}


def expand_message():
    """Build all of the documents in order from MAX_DEPTH up to depth 0."""
    groups = [[make_document(MAX_DEPTH, secret=letter) for letter in END_MESSAGE]]

    for i in reversed(xrange(1, MAX_DEPTH)):
        groups.append(group_nodes(groups[-1], i))

    start_page = dict(depth=0, id="start", message=START_MESSAGE, next=[item['id'] for item in groups[-1]])
    groups.append([start_page])
    return groups


def redacted_end_message(redacted=True):
    """Hide `END_MESSAGE` in the build output"""
    re_letters = re.compile('[a-z]', flags=re.I)
    if redacted:
        return re_letters.sub("*", END_MESSAGE)
    else:
        return END_MESSAGE


if __name__ == '__main__':
    log_format = "%(levelname)s:%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    # Set it up ...
    node_groups = expand_message()

    # ... and knock it down. boom.
    flat_data = flatten_tree(node_groups)

    with open(JSON_FILE, 'wb') as f:
        json.dump(flat_data, f, sort_keys=True, indent=2, separators=(',', ': '))

    # Pretty print a success message with a summary.
    print "*" * 70
    print "Start Message:"
    print "\n\t".join(wrap("\t%s" % START_MESSAGE))
    print "End Message: %s" % "(redacted)" if REDACTED_OUT else ""
    print "\n\t".join(wrap("\t%s" % redacted_end_message(redacted=REDACTED_OUT)))
    print
    print "The database has been successfully migrated."
    print "\n".join(wrap("**(Optional) Customize these messages in %r and rerun %r" % (__file__, "make migrate")))
