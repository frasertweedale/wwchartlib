"""
Pie chart widget.

Positive angles are counter-clockwise.  Angle of zero is the 3 o'clock
position.
"""

from __future__ import division

import math

from PySide.QtCore import *
from PySide.QtGui import *

from . import chart


def fraction_to_angle(fraction):
    """Convert a fraction to an angle (in Qt terms).

    Qt understands angels in 16ths-of-a-degree (i.e., one revolution is
    5760).
    """
    return fraction * 360 * 16


def theta_to_angle(theta):
    """Convert an angle in radians to an angle in Qt terms."""
    return theta * 360 / (2 * math.pi) * 16


def angle_to_theta(angle):
    """Convert an angle in Qt terms to radians."""
    return angle / 16 / 360 * (2 * math.pi)


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


class AdjustablePieChart(PieChart):
    """A ``PieChart`` with adjustable slices."""

    @property
    def x(self):
        """x component of the origin of the chart."""
        return self.width() / 2

    @property
    def y(self):
        return self.height() / 2
        """y component of the origin of the chart."""

    @property
    def origin(self):
        """The origin of this pie chart, as tuple (x, y)."""
        return self.x, self.y

    @property
    def radius(self):
        """The radius of the chart."""
        return min(self.origin)

    def _polar(self, x, y):
        """Convert cartisian coordinates to polar coordinates.

        Return (radius, angle) (angle in Qt terms).
        """
        rel_x = x - self.x
        rel_y = y - self.y
        theta = math.atan2(rel_y, rel_x)
        theta = theta if theta >= 0 else theta + math.pi * 2
        return self.radius, theta_to_angle(theta)

    def _cartesian(self, angle):
        """Returns cartesian coordinates of point on graph at given angle.

        The point returned is on the circumference of the graph.

        angle
          The angle, in Qt terms.
        """
        theta = angle_to_theta(angle)
        x, y = self.radius * math.cos(theta), self.radius * math.sin(theta)
        return self.x + x, self.y - y

    def paintEvent(self, ev):
        super(AdjustablePieChart, self).paintEvent(ev)

        p = QPainter(self)
        angle = 0
        for item in self._items:
            if item.fraction > 0:
                angle += fraction_to_angle(item.fraction)
                x, y = self._cartesian(angle)
                p.drawEllipse(QPointF(x, y), 5, 5)
