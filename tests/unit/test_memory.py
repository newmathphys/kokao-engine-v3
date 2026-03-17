"""
KOKAO Engine v3.0.4 — Unit Tests for Memory Module

Tests for kokao.core.memory.ContextMemory class.
"""

import unittest
import numpy as np
from kokao.core.memory import ContextMemory
from kokao.core.etalon import Etalon


class TestContextMemory(unittest.TestCase):
    """Test cases for ContextMemory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.memory = ContextMemory(K_max=100, delta_base=0.05)
        self.x = np.random.randn(10)
    
    def test_init(self):
        """Test memory initialization."""
        self.assertEqual(len(self.memory.etalons), 0)
        self.assertEqual(self.memory.K_max, 100)
        self.assertEqual(self.memory.delta_base, 0.05)
    
    def test_add_etalon(self):
        """Test adding etalon to memory."""
        etalon = self.memory.add_etalon(self.x, y=0)
        
        self.assertEqual(len(self.memory.etalons), 1)
        self.assertIsInstance(etalon, Etalon)
        self.assertEqual(etalon.class_label, 0)
    
    def test_add_etalon_exceeds_max(self):
        """Test adding etalon when memory is full."""
        for i in range(100):
            x = np.random.randn(10)
            self.memory.add_etalon(x, y=i % 3)
        
        self.assertEqual(len(self.memory.etalons), 100)
        
        # Add one more
        self.memory.add_etalon(self.x, y=0)
        
        # Should still be at K_max
        self.assertEqual(len(self.memory.etalons), 100)
    
    def test_find_nearest(self):
        """Test finding nearest etalons."""
        x1 = np.array([1.0, 0.0, 0.0])
        x2 = np.array([0.0, 1.0, 0.0])
        x3 = np.array([0.0, 0.0, 1.0])
        
        self.memory.add_etalon(x1, y=0)
        self.memory.add_etalon(x2, y=1)
        self.memory.add_etalon(x3, y=2)
        
        query = np.array([0.9, 0.1, 0.0])
        nearest = self.memory.find_nearest(query, k=2)
        
        self.assertEqual(len(nearest), 2)
        self.assertEqual(nearest[0][0], 0)  # First etalon should be closest
    
    def test_find_nearest_empty(self):
        """Test finding nearest in empty memory."""
        nearest = self.memory.find_nearest(self.x, k=5)
        self.assertEqual(len(nearest), 0)
    
    def test_should_create(self):
        """Test etalon creation decision."""
        # Empty memory should create
        self.assertTrue(self.memory.should_create(self.x, y=0))
        
        # Add similar etalon
        self.memory.add_etalon(self.x.copy(), y=0)
        
        # Same vector should not create new etalon
        self.assertFalse(self.memory.should_create(self.x, y=0))
        
        # Very different vector should create
        x_diff = np.random.randn(10) * 10
        self.assertTrue(self.memory.should_create(x_diff, y=0))
    
    def test_get_delta(self):
        """Test class-specific delta computation."""
        # Add etalons for class 0
        for _ in range(10):
            x = np.random.randn(10)
            self.memory.add_etalon(x, y=0)
        
        delta_0 = self.memory.get_delta(0)
        delta_1 = self.memory.get_delta(1)
        
        # Class 0 should have higher delta (more etalons)
        self.assertGreater(delta_0, self.memory.delta_base)
        self.assertEqual(delta_1, self.memory.delta_base)
    
    def test_predict(self):
        """Test prediction."""
        x1 = np.array([1.0, 0.0, 0.0])
        x2 = np.array([0.0, 1.0, 0.0])
        
        self.memory.add_etalon(x1, y=0)
        self.memory.add_etalon(x2, y=1)
        
        pred, conf = self.memory.predict(x1, k=1)
        self.assertEqual(pred, 0)
        self.assertGreater(conf, 0.5)
    
    def test_predict_empty(self):
        """Test prediction with empty memory."""
        pred, conf = self.memory.predict(self.x, k=5)
        self.assertEqual(pred, 0)
        self.assertEqual(conf, 0.0)
    
    def test_cleanup(self):
        """Test cleaning up low-activity etalons."""
        for i in range(10):
            x = np.random.randn(10)
            etalon = self.memory.add_etalon(x, y=0)
            etalon.activity = 0.01 if i < 5 else 0.5
        
        removed = self.memory.cleanup(min_activity=0.1)
        
        self.assertEqual(removed, 5)
        self.assertEqual(len(self.memory.etalons), 5)
    
    def test_get_statistics(self):
        """Test getting memory statistics."""
        stats = self.memory.get_statistics()
        
        self.assertEqual(stats['n_etalons'], 0)
        self.assertEqual(stats['n_classes'], 0)
        
        # Add some etalons
        for i in range(10):
            x = np.random.randn(10)
            self.memory.add_etalon(x, y=i % 3)
        
        stats = self.memory.get_statistics()
        
        self.assertEqual(stats['n_etalons'], 10)
        self.assertEqual(stats['n_classes'], 3)
        self.assertGreater(stats['avg_activity'], 0.0)
        self.assertEqual(stats['avg_age'], 0.0)


class TestContextMemoryAdaptive(unittest.TestCase):
    """Test adaptive delta functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.memory = ContextMemory(K_max=1000, delta_base=0.12)
    
    def test_adaptive_delta_formula(self):
        """Test δ(c) = δ_base · (1 + n_etalons(c) / K_max)."""
        # Add 100 etalons for class 0
        for _ in range(100):
            x = np.random.randn(10)
            self.memory.add_etalon(x, y=0)
        
        delta = self.memory.get_delta(0)
        expected = 0.12 * (1 + 100 / 1000)
        
        self.assertAlmostEqual(delta, expected, places=5)
    
    def test_adaptive_delta_max(self):
        """Test that delta is capped at 0.5."""
        # Add many etalons
        for _ in range(5000):
            x = np.random.randn(10)
            self.memory.add_etalon(x, y=0)
        
        delta = self.memory.get_delta(0)
        self.assertLessEqual(delta, 0.5)


if __name__ == '__main__':
    unittest.main()
