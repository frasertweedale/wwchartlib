"""
Provides ``TestCase``s for testing code that requires a QApplication.
"""
import unittest

from PySide.QtGui import *


class QtTestCase(unittest.TestCase):
    """``TestCase`` that sets up and tears down a ``QApplication``."""
    @classmethod
    def setUpClass(cls):
        app = QApplication.instance()
        cls._app = QApplication([]) if app is None else app
