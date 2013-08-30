# -*- coding: utf-8 -*-

"""
flstats
~~~~~~~

A tool to collect request execution time
statistics for the flask microframework.

:copyright: (c) 2013 by Yann Lambret.
:license: BSD, see LICENSE for more details.

"""

__title__ = 'flstats'
__version__ = '0.1'
__author__ = 'Yann Lambret'
__license__ = 'BSD'
__copyright__ = 'Copyright 2013 Yann Lambret'

__all__ = ['statistics', 'webstatistics']

from .flstats import statistics, webstatistics
