# -*- coding: utf-8 -*-

"""
flstats test script
~~~~~~~~~~~~~~~~~~~

This script is intended to test the flstats module.
"""

import json
import random
import unittest

from flstats import statistics, webstatistics
from flask import Flask

class FlstatsTestCase(unittest.TestCase):

    def setUp(self):
        """Creates a Flask test app and registers two routes
        together with the flstats blueprint.
        """ 

        self.app = Flask(__name__)
        self.app.register_blueprint(webstatistics)
        self.client = self.app.test_client()
        self.urls = ['http://localhost/url1', 'http://localhost/url2']

        @self.app.route('/url1')
        @statistics
        def url1():
            return random.choice(range(0, 1000))
        
        @self.app.route('/url2')
        @statistics
        def url2():
            return random.choice(range(0, 1000))

    def test_url1(self):
        """Sends a unique request to one URL and tests the
        returned statistics.
        """

        self.client.get('/url1')

        response = self.client.get('/flstats/')
        data = json.loads(response.data)
        stats = data['stats']

        # /flstats access tests
        self.assertEqual(response.status, '200 OK')

        # Statistics tests
        self.assertEqual(len(stats), 1)
        stat = stats.pop()
        self.assertEqual(stat['url'], 'http://localhost/url1')
        self.assertEqual(stat['count'], 1)
        self.assertTrue(stat['min'] == stat['avg'] == stat['max'])

    def test_url2(self):
        """Sends requests to both URLs and tests the
        returned statistics.
        """

        for i in range(1, 10):
            self.client.get('/url1')
        for i in range(0, 10):
            self.client.get('/url2')

        response = self.client.get('/flstats/')
        data = json.loads(response.data)
        stats = data['stats']

        # /flstats access tests
        self.assertEqual(response.status, '200 OK')

        # Statistics tests
        self.assertEqual(len(stats), 2)
        for stat in stats:
            self.assertTrue(stat['url'] in self.urls)
            self.assertEqual(stat['count'], 10)
            self.assertTrue(stat['min'] <= stat['avg'] <= stat['max'])

if __name__ == '__main__':
    unittest.main()
