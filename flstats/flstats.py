# -*- coding: utf-8 -*-

"""
flstats
~~~~~~~

This module allows you to monitor Flask requests execution time.
Statistics can be accessed by using the '/flstats/' route.
"""

from flask import Blueprint, Flask, jsonify, request
from functools import wraps
from Queue import Queue, Full
from threading import Thread
from time import time as now


class Stat(object):
    """The Stat class, which stores statistics for a specific URL."""

    def __init__(self):
        # Number of requests for the URL
        self.count = 0

        # Execution time for all requests
        self.total_time = 0.

        # Shortest request execution time
        self.min_time = 3600.

        # Longest request execution time
        self.max_time = 0.

    def update(self, time):
        self.count += 1
        self.total_time += time
        if time < self.min_time:
            self.min_time = time
        if time > self.max_time:
            self.max_time = time


class StatsManager(object):
    """The StatsManager class, which handles the statistics for all URLs."""

    # Application statistics
    stats = {}

    # Requests throughput
    throughput = {}

    @classmethod
    def process(cls):
        data = []
        for url, stat in cls.stats.iteritems():
            data.append({
                'url': url,
                'throughput': stat.count - cls.throughput.setdefault(url, 0),
                'avg': round((stat.total_time / stat.count) * 1000, 2),
                'min': round(stat.min_time * 1000, 2),
                'max': round(stat.max_time * 1000, 2)
            })
            cls.throughput[url] = stat.count
        return data


class Worker(Thread):
    """The Worker class, which processes statistics updates."""

    # We're using a queue to take care of concurrency
    queue = Queue(maxsize=0)

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while 1:
            url, time = self.__class__.queue.get()
            StatsManager.stats.setdefault(url, Stat()).update(time)
            self.__class__.queue.task_done()


#
# statistics decorator
#

def statistics(f):
    """The decorator used in the application to collect statistics."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        t1 = now()
        result = f(*args, **kwargs)
        t2 = now()
        # The queue should never be full, but we can't
        # take the risk to block the request anyway
        try:
            Worker.queue.put_nowait((request.url, t2 - t1))
        except Full:
            pass
        return result
    return wrapper


#
# Web statistics blueprint
#

webstatistics = Blueprint('webstatistics', __name__)


@webstatistics.route('/flstats/', methods=['GET'])
def flstats():
    """Returns statistics in the JSON format."""

    return jsonify({'stats': StatsManager.process()})


#
# Runs the worker
#

worker = Worker()
worker.daemon = True
worker.start()
