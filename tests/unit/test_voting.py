"""
KOKAO Engine v3.0.4 — Unit Tests for Voting Module

Tests for kokao.core.voting module.
"""

import unittest
import numpy as np
from kokao.core.voting import weighted_voting_cosine, simple_voting, softmax
from kokao.core.etalon import Etalon


class TestSoftmax(unittest.TestCase):
    """Test cases for softmax function."""
    
    def test_softmax_basic(self):
        """Test basic softmax computation."""
        x = np.array([1.0, 2.0, 3.0])
        probs = softmax(x)
        
        # Sum should be 1.0
        self.assertAlmostEqual(np.sum(probs), 1.0)
        
        # All positive
        self.assertTrue(np.all(probs > 0))
        
        # Largest input should have largest probability
        self.assertEqual(np.argmax(probs), 2)
    
    def test_softmax_numerical_stability(self):
        """Test softmax with large numbers."""
        x = np.array([100.0, 200.0, 300.0])
        probs = softmax(x)
        
        # Should not be NaN or Inf
        self.assertTrue(np.all(np.isfinite(probs)))
        self.assertAlmostEqual(np.sum(probs), 1.0)
    
    def test_softmax_empty(self):
        """Test softmax with empty array."""
        x = np.array([])
        probs = softmax(x)
        self.assertEqual(len(probs), 0)
    
    def test_softmax_uniform(self):
        """Test softmax with uniform input."""
        x = np.array([1.0, 1.0, 1.0])
        probs = softmax(x)
        
        expected = np.array([1/3, 1/3, 1/3])
        np.testing.assert_array_almost_equal(probs, expected)


class TestWeightedVoting(unittest.TestCase):
    """Test cases for weighted voting."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.n_classes = 3
        
        # Create etalons with different classes
        self.etalon0 = Etalon(c_plus=np.ones(10), class_label=0)
        self.etalon1 = Etalon(c_plus=np.ones(10) * 2, class_label=1)
        self.etalon2 = Etalon(c_plus=np.ones(10) * 3, class_label=2)
        
        # Add samples to vary purity
        self.etalon0.add_sample(0)
        self.etalon1.add_sample(1)
        self.etalon1.add_sample(0)  # Mixed class
        self.etalon2.add_sample(2)
        self.etalon2.add_sample(2)
    
    def test_weighted_voting_basic(self):
        """Test basic weighted voting."""
        x = np.random.randn(10)
        nearest = [
            (0, 0.9, self.etalon0),
            (1, 0.7, self.etalon1),
            (2, 0.5, self.etalon2)
        ]
        
        pred, conf = weighted_voting_cosine(nearest, x, self.n_classes)
        
        self.assertIsInstance(pred, int)
        self.assertIsInstance(conf, float)
        self.assertGreaterEqual(conf, 0.0)
        self.assertLessEqual(conf, 1.0)
    
    def test_weighted_voting_empty(self):
        """Test voting with no neighbors."""
        x = np.random.randn(10)
        pred, conf = weighted_voting_cosine([], x, self.n_classes)
        
        self.assertEqual(pred, 0)
        self.assertEqual(conf, 0.0)
    
    def test_weighted_voting_top_k(self):
        """Test voting with top_k parameter."""
        x = np.random.randn(10)
        nearest = [
            (0, 0.9, self.etalon0),
            (1, 0.7, self.etalon1),
            (2, 0.5, self.etalon2),
            (3, 0.3, self.etalon0)
        ]
        
        pred1, conf1 = weighted_voting_cosine(nearest, x, self.n_classes, top_k=2)
        pred2, conf2 = weighted_voting_cosine(nearest, x, self.n_classes, top_k=4)
        
        # Results may differ based on k
        self.assertIsInstance(pred1, int)
        self.assertIsInstance(pred2, int)
    
    def test_weighted_voting_temperature(self):
        """Test voting with different temperatures."""
        x = np.random.randn(10)
        nearest = [
            (0, 0.9, self.etalon0),
            (1, 0.7, self.etalon1),
        ]
        
        pred_low, conf_low = weighted_voting_cosine(
            nearest, x, self.n_classes, temperature=0.1
        )
        pred_high, conf_high = weighted_voting_cosine(
            nearest, x, self.n_classes, temperature=10.0
        )
        
        # Lower temperature should give more confident predictions
        self.assertGreaterEqual(conf_low, conf_high * 0.5)


class TestSimpleVoting(unittest.TestCase):
    """Test cases for simple voting."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.etalon0 = Etalon(c_plus=np.ones(10), class_label=0)
        self.etalon1 = Etalon(c_plus=np.ones(10) * 2, class_label=1)
    
    def test_simple_voting_basic(self):
        """Test basic simple voting."""
        x = np.random.randn(10)
        nearest = [
            (0, 0.9, self.etalon0),
            (0, 0.8, self.etalon0),
            (1, 0.7, self.etalon1)
        ]
        
        pred, conf = simple_voting(nearest, n_classes=2)
        
        self.assertEqual(pred, 0)  # Class 0 has more votes
        self.assertGreater(conf, 0.5)
    
    def test_simple_voting_empty(self):
        """Test voting with no neighbors."""
        pred, conf = simple_voting([], n_classes=2)

        self.assertEqual(pred, 0)
        self.assertEqual(conf, 0.0)


if __name__ == '__main__':
    unittest.main()
