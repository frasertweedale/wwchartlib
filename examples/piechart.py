#!/usr/bin/env python

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

import sys
import time

from PySide.QtCore import *
from PySide.QtGui import *

import wwchartlib.piechart

app = QApplication(sys.argv)
items = [wwchartlib.piechart.PieChartItem(fraction=0.2) for x in range(4)]
chart = wwchartlib.piechart.PieChart(items=items)
chart.show()


def _remove():
    chart.removeChartItem(0)


timer1 = QTimer()
timer1.setSingleShot(True)
timer1.timeout.connect(_remove)


def _add():
    chart.addChartItem(wwchartlib.piechart.PieChartItem(fraction=0.1))
    timer1.start(1000)


timer = QTimer()
timer.setSingleShot(True)
timer.timeout.connect(_add)
timer.start(1000)

app.exec_()
