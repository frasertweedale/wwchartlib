import unittest

from PySide.QtGui import *

import wwchartlib.chart
import wwchartlib.piechart

from .. import qt


class TestPieChartItemError(unittest.TestCase):
    def test_base(self):
        self.assertTrue(issubclass(
            wwchartlib.piechart.PieChartItemError,
            wwchartlib.chart.ChartItemError))


class TestChartError(unittest.TestCase):
    def test_base(self):
        self.assertTrue(issubclass(
            wwchartlib.piechart.PieChartError, wwchartlib.chart.ChartError))


class TestPieChartItem(unittest.TestCase):
    def test_base(self):
        self.assertTrue(issubclass(
            wwchartlib.piechart.PieChartItem, wwchartlib.chart.ChartItem))

    def test_init(self):
        item = wwchartlib.piechart.PieChartItem()
        self.assertIs(item.fraction, 0)
        self.assertIsNone(item.label)
        self.assertIsNone(item.value)
        self.assertIsNone(item.data)
        item = wwchartlib.piechart.PieChartItem(
            fraction=0.5, label='a', value=2, data=True)
        self.assertIs(item.fraction, 0.5)
        self.assertIs(item.label, 'a')
        self.assertIs(item.value, 2)
        self.assertTrue(item.data)
        item = wwchartlib.piechart.PieChartItem(fraction=1)
        self.assertIs(item.fraction, 1)
        item = wwchartlib.piechart.PieChartItem(fraction=2)
        self.assertIs(item.fraction, 2)


class TestPieChart(qt.QtTestCase):
    def setUp(self):
        self.chart = wwchartlib.piechart.PieChart()

    def test_base(self):
        self.assertIsInstance(self.chart, wwchartlib.chart.Chart)

    def test_init(self):
        # check size policy
        self.assertEqual(
            self.chart.sizePolicy(),
            QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        )

    def test_check_items(self):
        item_ltz = wwchartlib.piechart.PieChartItem(fraction=-0.5)
        item_nn = wwchartlib.piechart.PieChartItem(fraction='foo')

        # add bogus item (fraction < 0)
        self.chart.addChartItem(item_ltz)
        with self.assertRaisesRegexp(
            wwchartlib.piechart.PieChartItemError,
            'fraction cannot be less than 0'
        ):
            self.chart._check_items()

        # remove bogus item
        self.chart.removeChartItem(0)

        # add bogus item (non-numeric fraction)
        self.chart.addChartItem(item_nn)
        with self.assertRaisesRegexp(
            wwchartlib.piechart.PieChartItemError,
            'non-numeric fraction'
        ):
            self.chart._check_items()

        # remove bogus item
        self.chart.removeChartItem(0)

        # add bogus item list (sum of fractions > 1)
        item_1 = wwchartlib.piechart.PieChartItem(fraction=0.5)
        item_2 = wwchartlib.piechart.PieChartItem(fraction=0.5)
        item_3 = wwchartlib.piechart.PieChartItem(fraction=0.5)
        self.chart.setChartItems([item_1, item_2, item_3])
        with self.assertRaisesRegexp(
            wwchartlib.piechart.PieChartItemError,
            'Sum of fractions is greater than 1'
        ):
            self.chart._check_items()

        # remove one item (sum should then equal 1)
        self.chart.removeChartItem(2)
        self.chart._check_items()
