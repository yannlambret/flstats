# -*- coding: utf-8 -*-

"""
flstats
~~~~~~~

This module allows you to monitor Flask requests execution time.
Statistics can be accessed by using the '/flstats/' route.
"""

from flask import Blueprint, Flask, jsonify, make_response, request, Response
from functools import wraps
from Queue import Queue
from threading import Thread
from time import time as now

class _Stat(object):
    """The _Stat class, which stores statistics for a specific URL."""

    def __init__(self):
        # Number of requests for the URL
        self.count = 0

        # Execution time for all requests
        self.total_time = 0.

        # Shortest request execution time
        self.min_time = 3600.

        # Longest request execution time 
        self.max_time = 0.

        # Computed data
        self.data = {}

    def update(self, time):
        self.count += 1
        self.total_time += time
        if time < self.min_time: self.min_time = time
        if time > self.max_time: self.max_time = time

class _StatsManager(object):
    """The _StatsManager class, which handles the statistics for all URLs."""

    # Application statistics
    stats = {}

    @classmethod
    def process(cls):
        data = []
        for url in cls.stats:
            d = {}
            stat = cls.stats[url]
            d['url'] = url
            d['count'] = stat.count
            # Converts time values to milliseconds
            d['avg'] = round((stat.total_time / stat.count) * 1000, 2)
            d['min'] = round(stat.min_time * 1000, 2)
            d['max'] = round(stat.max_time * 1000, 2)
            data.append(d)
        return data

class _Worker(Thread):
    """The _Worker class, which processes statistics updates."""

    # We're using a queue to take care of concurrency
    queue = Queue(maxsize=0)

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while 1:
            url, time = self.__class__.queue.get(block=True)
            _StatsManager.stats.setdefault(url, _Stat()).update(time)
            self.__class__.queue.task_done()

#
# statistics decorator
#

def statistics(f):
    """The decorator used in the application to collect statistics."""

    @wraps(f)
    def decorated(*args, **kwargs):
        t1 = now()
        result = f(*args, **kwargs)
        t2 = now()
        _Worker.queue.put((request.url, t2 - t1), block=True)
        return result
    return decorated

#
# Web statistics blueprint
#

webstatistics = Blueprint('webstatistics', __name__)

@webstatistics.route('/flstats/', methods=['GET'])
def flstats():
    """Returns statistics in the JSON format."""

    return jsonify({'stats' : _StatsManager.process()})

#
# Runs the worker
#

_worker = _Worker()
_worker.daemon = True
_worker.start()
