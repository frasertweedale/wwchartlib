import unittest

from PySide.QtGui import *

import wwchartlib.chart
import wwchartlib.piechart

from .. import qt


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

    def test_add_item_with_non_number_fraction(self):
        # fraction of 0.5 should work
        item = wwchartlib.piechart.PieChartItem(fraction=0.5)
        self.chart.addChartItem(item)

        item_nn = wwchartlib.piechart.PieChartItem(fraction='foo')
        with self.assertRaisesRegexp(
            TypeError,
            '[Ff]raction must be a [Nn]umber'
        ):
            self.chart.addChartItem(item_nn)

        with self.assertRaisesRegexp(
            TypeError,
            '[Ff]raction must be a [Nn]umber'
        ):
            self.chart.setChartItems([
                wwchartlib.piechart.PieChartItem(fraction=0.5),
                wwchartlib.piechart.PieChartItem(fraction='foo'),
            ])

        # check that the (failed) operation had no effect
        # (the list should be just the original item added)
        self.assertListEqual(self.chart.chartItems(), [item])

    def test_add_item_fraction_lt_0(self):
        # zero should work
        item = wwchartlib.piechart.PieChartItem(fraction=0)
        self.chart.addChartItem(item)

        # less than zero should fail
        item_ltz = wwchartlib.piechart.PieChartItem(fraction=-0.5)
        with self.assertRaisesRegexp(
            ValueError,
            '[Ff]raction cannot be less than 0'
        ):
            self.chart.addChartItem(item_ltz)

        # check that the (failed) operation had no effect
        # (the list should be just the original item added)
        self.assertListEqual(self.chart.chartItems(), [item])

        with self.assertRaisesRegexp(
            ValueError,
            '[Ff]raction cannot be less than 0'
        ):
            self.chart.setChartItems([
                wwchartlib.piechart.PieChartItem(fraction=0.5),
                wwchartlib.piechart.PieChartItem(fraction=-0.5),
            ])

        # check that the (failed) operation had no effect
        # (the list should be just the original item added)
        self.assertListEqual(self.chart.chartItems(), [item])

    def test_add_item_fraction_gt_1(self):
        # add an item = 1 (should work)
        item = wwchartlib.piechart.PieChartItem(fraction=1)
        self.chart.addChartItem(item)

        # clear chart
        self.chart.setChartItems([])

        # add single item > 1
        item_gt1 = wwchartlib.piechart.PieChartItem(fraction=1.5)
        with self.assertRaisesRegexp(
            ValueError,
            '[Ff]raction cannot be greater than 1'
        ):
            self.chart.addChartItem(item_gt1)

        # check that the (failed) operation had no effect
        # (list should be empty)
        self.assertListEqual(self.chart.chartItems(), [])

        with self.assertRaisesRegexp(
            ValueError,
            '[Ff]raction cannot be greater than 1'
        ):
            self.chart.setChartItems([
                wwchartlib.piechart.PieChartItem(fraction=0),
                wwchartlib.piechart.PieChartItem(fraction=1.5),
            ])

        # check that the (failed) operation had no effect
        # (list should be empty)
        self.assertListEqual(self.chart.chartItems(), [])

    def test_sum_fractions_gt_1(self):
        item = wwchartlib.piechart.PieChartItem(fraction=0.5)
        self.chart.addChartItem(item)

        # add an item to take it over 1
        item_toobig = wwchartlib.piechart.PieChartItem(fraction=1)
        with self.assertRaisesRegexp(ValueError, '[Ff]raction is too large'):
            self.chart.addChartItem(item_toobig)

        # check that the (failed) operation had no effect
        # (the list should be just the original item added)
        self.assertListEqual(self.chart.chartItems(), [item])

        # test with a list that sums to exactly 1; should succeed
        itemA = wwchartlib.piechart.PieChartItem(fraction=0.5)
        itemB = wwchartlib.piechart.PieChartItem(fraction=0.5)
        self.chart.setChartItems([itemA, itemB])

        # test a list that sums to > 1
        with self.assertRaisesRegexp(
            ValueError,
            '[Ss]um of.*fractions cannot be greater than 1'
        ):
            self.chart.setChartItems([
                wwchartlib.piechart.PieChartItem(fraction=0.5),
                wwchartlib.piechart.PieChartItem(fraction=1),
            ])

        # check that the (failed) operation had no effect
        # (the list should be that from the earlier setChartItems
        self.assertListEqual(self.chart.chartItems(), [itemA, itemB])
