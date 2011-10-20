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

from PySide.QtCore import *
from PySide.QtGui import *

import wwchartlib.piechart

app = QApplication(sys.argv)
items = [wwchartlib.piechart.PieChartItem(fraction=0.2) for x in range(4)]
chart = wwchartlib.piechart.AdjustablePieChart(items=items)
chart.show()

app.exec_()
