"""
Common classes and routines for ``wwchartlib``.
"""

from PySide.QtGui import *


class ChartItemError(Exception):
    pass


class ChartError(Exception):
    pass


class ChartItem(object):
    def __init__(self, label=None, value=None, data=None, **kwargs):
        """Initialise the chart item.

        label
          An object which will be passed as the parameter to ``unicode``
          to determine a label for the chart item.
        value
          A value that will be displayed as the value of an item (via
          ``unicode(value)`` and *may* be used by subclasses of
          ``Chart`` as the numeric value of the item in determining how
          to draw the chart.
        data
          Arbitrary data attribute; not used by ``wwchartlib``.
        """
        self.label = label
        self.value = value
        self.data = data


class Chart(QWidget):
    _item_class = ChartItem

    def __init__(self, parent=None, items=None):
        super(Chart, self).__init__(parent=parent)
        self._items = None
        if items:
            self.setChartItems(items)

    def setChartItems(self, items):
        """Set the list of ``PieChartItem``s."""
        self._items = list(items)

    def chartItems(self):
        """Return the list of ``ChartItem``s."""
        return self._items

    def addChartItem(self, item, index=-1):
        """Add a ``ChartItem`` to this chart.

        item
          A ``PieChartItem``
        index
          Where to insert the item.  If negative, item is inserted as
          the last item.
        """
        if self._items is None:
            self._items = [item]
        elif index < 0:
            self._items.append(item)
        else:
            self._items.insert(index, item)
        self.update()  # repaint

    def removeChartItem(self, index):
        """Remove a ``ChartItem`` from this ``PieChart``.

        index
          The index of the item to remove.  If negative, the Nth item
          from the end is removed.

        Return the removed item.
        """
        item = self._items.pop(index)
        self.update()
        return item

    def _check_items(self):
        if not self._items:
            raise ChartItemError('No items.')
        if not all(isinstance(x, self._item_class) for x in self._items):
            raise ChartItemError(
                'Not all items are instances of {}'.format(self._item_class)
            )
