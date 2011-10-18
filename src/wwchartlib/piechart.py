"""
Pie chart widget.

Positive angles are counter-clockwise.  Angle of zero is the 3 o'clock
position.
"""

from __future__ import division

from PySide.QtCore import *
from PySide.QtGui import *

from . import chart


def fraction_to_angle(fraction):
    """Convert a fraction to an angle (in Qt terms).

    Qt understands angels in 16ths-of-a-degree (i.e., one revolution is
    5760).
    """
    return fraction * 5760


class PieChartItemError(chart.ChartItemError):
    pass


class PieChartError(chart.ChartError):
    pass


class PieChartItem(chart.ChartItem):
    def __init__(self, fraction=None, **kwargs):
        """Initialise the pie chart item.

        fraction:
          The fraction of this pie chart item, in range ``0..1``.
        """
        super(PieChartItem, self).__init__(**kwargs)
        self.fraction = fraction or 0


class PieChart(chart.Chart):
    _item_class = PieChartItem

    def __init__(self, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        # get as much space as possible
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    def _check_items(self):
        super(PieChart, self)._check_items()
        try:
            if any(x.fraction < 0 for x in self._items):
                raise PieChartItemError(
                    'PieChartItem fraction cannot be less than 0.')
            if sum(x.fraction for x in self._items) > 1:
                raise PieChartItemError('Sum of fractions is greater than 1.')
        except TypeError:
            raise PieChartItemError(
                'Items with undefined or non-numeric fraction.'
            )

    def _square(self):
        """Return a centered, square QRect of the maximum size possible."""
        width = self.width()
        height = self.height()
        shortest_side = min(width, height)
        return QRect(
            (width - shortest_side) / 2,
            (height - shortest_side) / 2,
            shortest_side,
            shortest_side
        )

    def paintEvent(self, ev):
        """Paint the pie chart."""
        self._check_items()

        p = QPainter(self)
        rect = self._square()

        angle = 0
        for item in self._items:
            if item.fraction > 0:
                span = fraction_to_angle(item.fraction)
                p.drawPie(rect, angle, span)
                angle += span
