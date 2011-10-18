#!/usr/bin/env python

import sys
import time

from PySide.QtCore import *
from PySide.QtGui import *

import wwchartlib.piechart

app = QApplication(sys.argv)
items = [wwchartlib.piechart.PieChartItem(fraction=0.2)] * 4
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
