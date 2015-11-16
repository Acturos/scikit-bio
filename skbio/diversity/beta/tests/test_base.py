# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

from unittest import TestCase, main

import numpy.testing as npt

from skbio.io._fileobject import StringIO
from skbio import DistanceMatrix, TreeNode
from skbio.diversity import beta_diversity
from skbio.diversity.beta import unweighted_unifrac, weighted_unifrac


class BaseTests(TestCase):
    def setUp(self):
        self.t1 = [[1, 5],
                   [2, 3],
                   [0, 1]]
        self.ids1 = list('ABC')
        self.tree1 = TreeNode.read(StringIO(
            '((O1:0.25, O2:0.50):0.25, O3:0.75)root;'))
        self.otu_ids1 = ['O1', 'O2']

        self.t2 = [[23, 64, 14, 0, 0, 3, 1],
                   [0, 3, 35, 42, 0, 12, 1],
                   [0, 5, 5, 0, 40, 40, 0],
                   [44, 35, 9, 0, 1, 0, 0],
                   [0, 2, 8, 0, 35, 45, 1],
                   [0, 0, 25, 35, 0, 19, 0]]
        self.ids2 = list('ABCDEF')

    def test_beta_diversity_invalid_input(self):
        # number of ids doesn't match the number of samples
        self.assertRaises(ValueError, beta_diversity, self.t1, list('AB'),
                          'euclidean')

    def test_beta_diversity_euclidean(self):
        actual_dm = beta_diversity('euclidean', self.t1, self.ids1)
        self.assertEqual(actual_dm.shape, (3, 3))
        npt.assert_almost_equal(actual_dm['A', 'A'], 0.0)
        npt.assert_almost_equal(actual_dm['B', 'B'], 0.0)
        npt.assert_almost_equal(actual_dm['C', 'C'], 0.0)
        npt.assert_almost_equal(actual_dm['A', 'B'], 2.23606798)
        npt.assert_almost_equal(actual_dm['B', 'A'], 2.23606798)
        npt.assert_almost_equal(actual_dm['A', 'C'], 4.12310563)
        npt.assert_almost_equal(actual_dm['C', 'A'], 4.12310563)
        npt.assert_almost_equal(actual_dm['B', 'C'], 2.82842712)
        npt.assert_almost_equal(actual_dm['C', 'B'], 2.82842712)

        actual_dm = beta_diversity('euclidean', self.t2, self.ids2)
        expected_data = [
            [0., 80.8455317, 84.0297566, 36.3042697, 86.0116271, 78.9176786],
            [80.8455317, 0., 71.0844568, 74.4714710, 69.3397433, 14.422205],
            [84.0297566, 71.0844568, 0., 77.2851861, 8.3066238, 60.7536007],
            [36.3042697, 74.4714710, 77.2851861, 0., 78.7908624, 70.7389567],
            [86.0116271, 69.3397433, 8.3066238, 78.7908624, 0., 58.4807660],
            [78.9176786, 14.422205, 60.7536007, 70.7389567, 58.4807660, 0.]]
        expected_dm = DistanceMatrix(expected_data, self.ids2)
        for id1 in self.ids2:
            for id2 in self.ids2:
                npt.assert_almost_equal(actual_dm[id1, id2],
                                        expected_dm[id1, id2], 6)

    def test_beta_diversity_braycurtis(self):
        actual_dm = beta_diversity('braycurtis', self.t1, self.ids1)
        self.assertEqual(actual_dm.shape, (3, 3))
        npt.assert_almost_equal(actual_dm['A', 'A'], 0.0)
        npt.assert_almost_equal(actual_dm['B', 'B'], 0.0)
        npt.assert_almost_equal(actual_dm['C', 'C'], 0.0)
        npt.assert_almost_equal(actual_dm['A', 'B'], 0.27272727)
        npt.assert_almost_equal(actual_dm['B', 'A'], 0.27272727)
        npt.assert_almost_equal(actual_dm['A', 'C'], 0.71428571)
        npt.assert_almost_equal(actual_dm['C', 'A'], 0.71428571)
        npt.assert_almost_equal(actual_dm['B', 'C'], 0.66666667)
        npt.assert_almost_equal(actual_dm['C', 'B'], 0.66666667)

        actual_dm = beta_diversity('braycurtis', self.t2, self.ids2)
        expected_data = [
            [0., 0.78787879, 0.86666667, 0.30927835, 0.85714286, 0.81521739],
            [0.78787879, 0., 0.78142077, 0.86813187, 0.75, 0.1627907],
            [0.86666667, 0.78142077, 0., 0.87709497, 0.09392265, 0.71597633],
            [0.30927835, 0.86813187, 0.87709497, 0., 0.87777778, 0.89285714],
            [0.85714286, 0.75, 0.09392265, 0.87777778, 0., 0.68235294],
            [0.81521739, 0.1627907, 0.71597633, 0.89285714, 0.68235294, 0.]]
        expected_dm = DistanceMatrix(expected_data, self.ids2)
        for id1 in self.ids2:
            for id2 in self.ids2:
                npt.assert_almost_equal(actual_dm[id1, id2],
                                        expected_dm[id1, id2], 6)

    def test_beta_diversity_unweighted_unifrac(self):
        # expected values calculated by hand
        dm1 = beta_diversity('unweighted_unifrac', self.t1, self.ids1,
                             otu_ids=self.otu_ids1, tree=self.tree1)
        dm2 = beta_diversity(unweighted_unifrac, self.t1, self.ids1,
                             otu_ids=self.otu_ids1, tree=self.tree1)
        self.assertEqual(dm1.shape, (3, 3))
        self.assertEqual(dm1, dm2)
        expected_data = [
            [0.0, 0.0, 0.25/1.0],
            [0.0, 0.0, 0.25/1.0],
            [0.25/1.0, 0.25/1.0, 0.0]]
        expected_dm = DistanceMatrix(expected_data, ids=self.ids1)
        for id1 in self.ids1:
            for id2 in self.ids1:
                npt.assert_almost_equal(dm1[id1, id2],
                                        expected_dm[id1, id2], 6)

    def test_beta_diversity_weighted_unifrac(self):
        # expected values calculated by hand
        dm1 = beta_diversity('weighted_unifrac', self.t1, self.ids1,
                             otu_ids=self.otu_ids1, tree=self.tree1)
        dm2 = beta_diversity(weighted_unifrac, self.t1, self.ids1,
                             otu_ids=self.otu_ids1, tree=self.tree1)
        self.assertEqual(dm1.shape, (3, 3))
        self.assertEqual(dm1, dm2)
        expected_data = [
            [0.0, 0.1750000, 0.12499999],
            [0.1750000, 0.0, 0.3000000],
            [0.12499999, 0.3000000, 0.0]]
        expected_dm = DistanceMatrix(expected_data, ids=self.ids1)
        for id1 in self.ids1:
            for id2 in self.ids1:
                npt.assert_almost_equal(dm1[id1, id2],
                                        expected_dm[id1, id2], 6)

    def test_beta_diversity_weighted_unifrac_normalized(self):
        # expected values calculated by hand
        dm1 = beta_diversity('weighted_unifrac', self.t1, self.ids1,
                             otu_ids=self.otu_ids1, tree=self.tree1,
                             normalized=True)
        dm2 = beta_diversity(weighted_unifrac, self.t1, self.ids1,
                             otu_ids=self.otu_ids1, tree=self.tree1,
                             normalized=True)
        self.assertEqual(dm1.shape, (3, 3))
        self.assertEqual(dm1, dm2)
        expected_data = [
            [0.0, 0.128834, 0.085714],
            [0.128834, 0.0, 0.2142857],
            [0.085714, 0.2142857, 0.0]]
        expected_dm = DistanceMatrix(expected_data, ids=self.ids1)
        for id1 in self.ids1:
            for id2 in self.ids1:
                npt.assert_almost_equal(dm1[id1, id2],
                                        expected_dm[id1, id2], 6)

if __name__ == "__main__":
    main()
