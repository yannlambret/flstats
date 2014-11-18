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
from time import sleep


class FlstatsTestCase(unittest.TestCase):

    def setUp(self):
        """Creates a Flask test app and registers two routes
        as well as the flstats blueprint.
        """

        self.app = Flask(__name__)
        self.app.register_blueprint(webstatistics)
        self.client = self.app.test_client()

        @self.app.route('/url1')
        @statistics
        def url1():
            return random.randint(0, 1000)

        @self.app.route('/url2')
        @statistics
        def url2():
            return random.randint(0, 1000)

    def test_url1(self):
        """Test with one URL only"""

        self.client.get('/url1')

        # We make sure data processing is complete
        sleep(0.1)

        response = self.client.get('/flstats/')
        self.assertEqual(response.status, '200 OK')

        # Statistics tests
        data = json.loads(response.data)

        stats = data['stats']
        self.assertEqual(len(stats), 1)

        stat = stats.pop()
        self.assertEqual(stat['url'], 'http://localhost/url1')
        self.assertEqual(stat['throughput'], 1)
        self.assertTrue(stat['min'] == stat['avg'] == stat['max'])

        for i in range(0, 9):
            self.client.get('/url1')

        # We make sure data processing is complete
        sleep(0.1)

        response = self.client.get('/flstats/')
        self.assertEqual(response.status, '200 OK')

        # Statistics tests
        data = json.loads(response.data)

        stats = data['stats']
        self.assertEqual(len(stats), 1)

        stat = stats.pop()
        self.assertEqual(stat['url'], 'http://localhost/url1')
        self.assertEqual(stat['throughput'], 9)
        self.assertTrue(stat['min'] <= stat['avg'] <= stat['max'])

    def test_url2(self):
        """Test with two URLs"""

        for i in range(0, 20):
            self.client.get('/url2')

        # We make sure data processing is complete
        sleep(0.1)

        response = self.client.get('/flstats/')
        self.assertEqual(response.status, '200 OK')

        # Statistics tests
        data = json.loads(response.data)

        stats = data['stats']
        self.assertEqual(len(stats), 2)

        for stat in stats:
            if stat['url'] == 'http://localhost/url1':
                self.assertEqual(stat['throughput'], 0)
                self.assertTrue(stat['min'] <= stat['avg'] <= stat['max'])
            elif stat['url'] == 'http://localhost/url2':
                self.assertEqual(stat['throughput'], 20)
                self.assertTrue(stat['min'] <= stat['avg'] <= stat['max'])
            else:
                self.fail('Invalid URL, WTF?!')


if __name__ == '__main__':
    unittest.main()
