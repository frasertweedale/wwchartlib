#!/usr/bin/env python

import sys

from PySide.QtCore import *
from PySide.QtGui import *

import wwchartlib.piechart

app = QApplication(sys.argv)
items = [wwchartlib.piechart.PieChartItem(fraction=0.2) for x in range(4)]
chart = wwchartlib.piechart.AdjustablePieChart(items=items)
chart.show()

app.exec_()
