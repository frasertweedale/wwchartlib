"""
Pie chart widget.

Positive angles are counter-clockwise.  Angle of zero is the 3 o'clock
position.
"""

from __future__ import division

import math
import numbers

from PySide.QtCore import *
from PySide.QtGui import *

from . import chart


def fraction_to_angle(fraction):
    """Convert a fraction to an angle (in Qt terms).

    Qt understands angels in 16ths-of-a-degree (i.e., one revolution is
    5760).
    """
    return fraction * 360 * 16


def angle_to_fraction(angle):
    """Convert an angle (in Qt terms) to a fraction."""
    return angle / 16 / 360


def theta_to_angle(theta):
    """Convert an angle in radians to an angle in Qt terms."""
    return theta * 360 / (2 * math.pi) * 16


def angle_to_theta(angle):
    """Convert an angle in Qt terms to radians."""
    return angle / 16 / 360 * (2 * math.pi)


def opposite_angle(angle):
    """Determine the opposite angle to the angle given, in Qt terms."""
    angle += 180 * 16
    if angle >= 360 * 16:
        angle -= 360 * 16
    return angle


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

    @classmethod
    def _check_item(cls, item):
        if not isinstance(item.fraction, numbers.Number):
            raise TypeError('PieChartItem fraction must be a Number.')
        if item.fraction < 0:
            raise ValueError('PieChartItem fraction cannot be less than 0.')
        if item.fraction > 1:
            raise ValueError('PieChartItem fraction cannot be greater than 1.')
        return super(PieChart, cls)._check_item(item)

    @classmethod
    def _check_items(cls, items):
        if sum(item.fraction for item in items) > 1:
            raise ValueError(
                'Sum of PieChartItem fractions cannot be greater than 1.'
            )
        return super(PieChart, cls)._check_items(items)

    def __init__(self, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        # get as much space as possible
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    def addChartItem(self, item, **kwargs):
        self._check_item(item)
        if sum((x.fraction for x in self._items), item.fraction) > 1:
            raise ValueError('PieChartItem fraction is too large.')
        super(PieChart, self).addChartItem(item, **kwargs)

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
    _grip_radius = 5

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

    def __init__(self, **kwargs):
        """Initialise the adjustable pie chart."""
        super(AdjustablePieChart, self).__init__(**kwargs)
        self._gripped_item = None  # the item currently being adjusted

    def _polar(self, x, y):
        """Convert cartisian coordinates to polar coordinates.

        Return (radius, angle) (angle in Qt terms).
        """
        rel_x = x - self.x
        rel_y = self.y - y
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

    def _grips(self):
        """A generator for the cartesian coordinates of all grips.

        Return x, y, item where item is the items whose grip should be
        found at the given coordinates.
        """
        angle = 0
        for item in self._items:
            angle += fraction_to_angle(item.fraction)
            yield self._cartesian(angle) + (item,)

    def paintEvent(self, ev):
        super(AdjustablePieChart, self).paintEvent(ev)

        p = QPainter(self)
        angle = 0
        for x, y, item in self._grips():
            p.drawEllipse(QPointF(x, y), self._grip_radius, self._grip_radius)

    def mousePressEvent(self, ev):
        """Check if an item is being gripped.

        If multiple grips are in the same place, the *last* matching
        grip is recorded as the gripped item.
        """
        gripped_item = None
        for x, y, item in self._grips():
            # see if press event is on this grip
            radius = math.sqrt((x - ev.x()) ** 2 + (y - ev.y()) ** 2)
            if radius < self._grip_radius:
                gripped_item = item
        self._gripped_item = gripped_item

    def mouseMoveEvent(self, ev):
        if self._gripped_item:
            gripped_item = self._gripped_item
            index = self._items.index(gripped_item)
            previous_items = self._items[:index]
            next_items = self._items[index + 1:]

            # calculate some interesting angles for this item
            #
            # A slice cannot become smaller than its base_angle and
            # cannot become larger than its max_angle
            base_angle = fraction_to_angle(
                sum(item.fraction for item in previous_items)
            )
            cur_angle = base_angle + fraction_to_angle(gripped_item.fraction)
            max_angle = cur_angle + fraction_to_angle(
                next_items[0].fraction if next_items else 1
            )

            # calculate current angle of pointer
            radius, angle = self._polar(ev.x(), ev.y())

            # determine whether we have grown to max or shrunk to base
            # if the angle is not between base and max
            if not base_angle <= angle <= max_angle:
                midline = opposite_angle((max_angle + base_angle) / 2)
                if midline < 180 * 16 and 0 <= angle < midline:
                    angle = max_angle
                elif midline >= 180 * 16 and midline <= angle <= 360 * 16:
                    angle = base_angle
                elif angle < base_angle:
                    angle = base_angle
                else:
                    angle = max_angle

            if angle != cur_angle:  # angle has changed
                # set the fraction of the gripped_item
                gripped_item.fraction = \
                    max(angle_to_fraction(angle - base_angle), 0)

                # subtract new angle from next item (if there is one)
                if next_items:
                    fraction_delta = angle_to_fraction(angle - cur_angle)
                    next_items[0].fraction = \
                        max(next_items[0].fraction - fraction_delta, 0)

            self.update()

    def mouseReleaseEvent(self, ev):
        self._gripped_item = None
