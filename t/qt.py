# This file is part of wwchartlib
# Copyright (C) 2011 Benon Technologies Pty Ltd
#
# wwchartlib is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
