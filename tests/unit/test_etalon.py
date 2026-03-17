"""
KOKAO Engine v3.0.4 — Unit Tests for Etalon Module

Tests for kokao.core.etalon.Etalon class.
"""

import unittest
import numpy as np
from kokao.core.etalon import Etalon


class TestEtalon(unittest.TestCase):
    """Test cases for Etalon class."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.x = np.random.randn(10)
        self.etalon = Etalon(c_plus=self.x.copy(), class_label=0)
    
    def test_init(self):
        """Test etalon initialization."""
        self.assertEqual(self.etalon.class_label, 0)
        self.assertEqual(self.etalon.age, 0)
        self.assertEqual(self.etalon.activity, 1.0)
        np.testing.assert_array_equal(self.etalon.c_plus, self.x)
        np.testing.assert_array_almost_equal(
            self.etalon.c_minus, -0.1 * self.x
        )
    
    def test_init_with_c_minus(self):
        """Test etalon initialization with custom c_minus."""
        c_minus = np.random.randn(10)
        etalon = Etalon(c_plus=self.x, c_minus=c_minus, class_label=1)
        np.testing.assert_array_equal(etalon.c_minus, c_minus)
        self.assertEqual(etalon.class_label, 1)
    
    def test_get_response(self):
        """Test etalon response computation."""
        response = self.etalon.get_response(self.x)
        expected = np.dot(self.x, self.etalon.c_plus) - np.dot(self.x, self.etalon.c_minus)
        self.assertAlmostEqual(response, expected)
    
    def test_similarity(self):
        """Test cosine similarity computation."""
        sim = self.etalon.similarity(self.x)
        self.assertGreaterEqual(sim, 0.0)
        self.assertLessEqual(sim, 1.0)
        
        # Same vector should have high similarity
        sim_same = self.etalon.similarity(self.etalon.c_plus)
        self.assertGreater(sim_same, 0.9)
    
    def test_similarity_zero_vector(self):
        """Test similarity with zero vector."""
        zero_vec = np.zeros(10)
        sim = self.etalon.similarity(zero_vec)
        self.assertEqual(sim, 0.0)
    
    def test_update_weights(self):
        """Test weight update using Formula (8)."""
        initial_c_plus = self.etalon.c_plus.copy()
        initial_c_minus = self.etalon.c_minus.copy()
        
        error = 0.5
        lr = 0.02
        
        self.etalon.update_weights(error, self.x, lr)
        
        expected_c_plus = initial_c_plus + lr * error * self.x
        expected_c_minus = initial_c_minus - lr * error * self.x
        
        np.testing.assert_array_almost_equal(
            self.etalon.c_plus, np.clip(expected_c_plus, -2.0, 2.0)
        )
        np.testing.assert_array_almost_equal(
            self.etalon.c_minus, np.clip(expected_c_minus, -2.0, 2.0)
        )
    
    def test_update_weights_clipping(self):
        """Test weight clipping during update."""
        large_error = 100.0
        large_lr = 1.0
        
        self.etalon.update_weights(large_error, self.x, large_lr)
        
        self.assertTrue(np.all(self.etalon.c_plus >= -2.0))
        self.assertTrue(np.all(self.etalon.c_plus <= 2.0))
        self.assertTrue(np.all(self.etalon.c_minus >= -2.0))
        self.assertTrue(np.all(self.etalon.c_minus <= 2.0))
    
    def test_get_purity(self):
        """Test purity computation."""
        # Initial purity should be 1.0 (only one class)
        purity = self.etalon.get_purity()
        self.assertEqual(purity, 1.0)
        
        # Add samples of different class
        self.etalon.add_sample(1)
        self.etalon.add_sample(1)
        
        # Now class 1 has 2 samples, class 0 has 1
        purity = self.etalon.get_purity()
        self.assertAlmostEqual(purity, 2/3)
    
    def test_add_sample(self):
        """Test adding samples to etalon."""
        self.etalon.add_sample(0)
        self.etalon.add_sample(1)
        
        self.assertEqual(self.etalon.age, 2)
        self.assertEqual(self.etalon.class_counts[0], 2)  # 1 from init + 1 added
        self.assertEqual(self.etalon.class_counts[1], 1)
    
    def test_decay(self):
        """Test activity decay."""
        initial_activity = self.etalon.activity
        self.etalon.decay(tau=50.0)
        self.assertLess(self.etalon.activity, initial_activity)
        self.assertGreaterEqual(self.etalon.activity, 0.0)
        self.assertLessEqual(self.etalon.activity, 1.0)
    
    def test_decay_multiple_steps(self):
        """Test activity decay over multiple steps."""
        activity = self.etalon.activity
        for _ in range(10):
            self.etalon.decay(tau=10.0)
        
        expected = activity * (np.exp(-1/10.0) ** 10)
        self.assertAlmostEqual(self.etalon.activity, expected, places=5)


class TestEtalonBrightnessInvariance(unittest.TestCase):
    """Test brightness invariance property."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.x = np.random.randn(10)
        self.etalon = Etalon(c_plus=self.x.copy(), class_label=0)
    
    def test_brightness_invariance(self):
        """Test that recognition is invariant to brightness scaling."""
        # Scale input by different factors
        scales = [0.1, 0.5, 1.0, 2.0, 10.0]
        similarities = []
        
        for scale in scales:
            x_scaled = self.x * scale
            sim = self.etalon.similarity(x_scaled)
            similarities.append(sim)
        
        # All similarities should be approximately equal (cosine similarity)
        for i in range(len(similarities) - 1):
            self.assertAlmostEqual(
                similarities[i], similarities[i+1], 
                places=5,
                msg=f"Similarity should be invariant to scale {scales[i]} vs {scales[i+1]}"
            )


if __name__ == '__main__':
    unittest.main()
