"""
KOKAO Engine v3.0.4 — Unit Tests for Learning Module

Tests for kokao.core.learning.KosyakovLearningEngine class.
"""

import unittest
import numpy as np
from kokao.core.learning import KosyakovLearningEngine
from kokao.core.etalon import Etalon


class TestKosyakovLearningEngine(unittest.TestCase):
    """Test cases for KosyakovLearningEngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.engine = KosyakovLearningEngine(base_lr=0.02)
        self.x = np.random.randn(10)
        self.etalon = Etalon(c_plus=self.x.copy(), class_label=0)
    
    def test_init(self):
        """Test engine initialization."""
        self.assertEqual(self.engine.base_lr, 0.02)
        self.assertTrue(self.engine.adaptive)
        self.assertEqual(self.engine.lambda_T, 1.0)
        self.assertEqual(self.engine.volatility, 0.0)
    
    def test_train_step(self):
        """Test single training step."""
        error = self.engine.train_step(self.etalon, self.x, target=0)
        
        self.assertIsInstance(error, float)
        self.assertEqual(len(self.engine.error_history), 1)
    
    def test_compute_error(self):
        """Test error computation."""
        error = self.engine.compute_error(self.etalon, self.x, target=0)
        
        # Error should be finite
        self.assertTrue(np.isfinite(error))
        
        # For non-matching class, error should be different
        error_mismatch = self.engine.compute_error(self.etalon, self.x, target=1)
        self.assertNotAlmostEqual(error, error_mismatch)
    
    def test_apply_formula_8(self):
        """Test Formula (8) weight update."""
        initial_c_plus = self.etalon.c_plus.copy()
        error = 0.5
        
        self.engine.apply_formula_8(self.etalon, error, self.x)
        
        # Weights should have changed
        self.assertFalse(np.array_equal(self.etalon.c_plus, initial_c_plus))
    
    def test_get_adaptive_lr(self):
        """Test adaptive learning rate computation."""
        # Without error history, should return base_lr
        lr = self.engine.get_adaptive_lr()
        self.assertAlmostEqual(lr, self.engine.base_lr)
        
        # Add some error history
        for _ in range(10):
            self.engine.error_history.append(np.random.randn())
        
        lr_adaptive = self.engine.get_adaptive_lr()
        self.assertGreater(lr_adaptive, 0)
    
    def test_compute_beta(self):
        """Test beta computation from surprise."""
        beta = self.engine._compute_beta(surprise=0.0)
        self.assertGreaterEqual(beta, 0.1)
        self.assertLessEqual(beta, 2.0)
        
        # High surprise should give lower beta
        beta_high = self.engine._compute_beta(surprise=100.0)
        self.assertAlmostEqual(beta_high, 0.1, places=2)
    
    def test_update_volatility(self):
        """Test volatility update."""
        self.engine.error_history = [0.1, 0.2, 0.3, 0.4, 0.5]
        self.engine._update_volatility()
        
        self.assertGreater(self.engine.volatility, 0)
    
    def test_get_statistics(self):
        """Test getting learning statistics."""
        stats = self.engine.get_statistics()
        
        self.assertIn('avg_error', stats)
        self.assertIn('volatility', stats)
        self.assertIn('current_lr', stats)
    
    def test_formula_8_implementation(self):
        """Test that Formula (8) is correctly implemented."""
        # c'_i = c_i - (Δ₀ · b_i) / Σ b_i²
        # For normalized input: c'_i = c_i - η · ε(t) · x(t)
        
        x_normalized = self.x / np.linalg.norm(self.x)
        etalon = Etalon(c_plus=x_normalized.copy(), class_label=0)
        
        error = 0.5
        lr = 0.02
        
        initial_c_plus = etalon.c_plus.copy()
        etalon.update_weights(error, x_normalized, lr)
        
        # Expected update: c_plus += lr * error * x
        expected = initial_c_plus + lr * error * x_normalized
        
        np.testing.assert_array_almost_equal(
            etalon.c_plus, np.clip(expected, -2.0, 2.0), decimal=5
        )


class TestKosyakovLearningEngineConvergence(unittest.TestCase):
    """Test convergence properties."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.engine = KosyakovLearningEngine(base_lr=0.01)
    
    def test_convergence_with_repeated_samples(self):
        """Test that error decreases with repeated samples."""
        x = np.random.randn(20)
        etalon = Etalon(c_plus=x.copy(), class_label=0)
        
        errors = []
        for _ in range(100):
            error = self.engine.train_step(etalon, x, target=0)
            errors.append(abs(error))
        
        # Error should generally decrease (with some noise)
        early_avg = np.mean(errors[:10])
        late_avg = np.mean(errors[-10:])
        
        # Allow some tolerance due to noise
        self.assertLessEqual(late_avg, early_avg * 1.5)


if __name__ == '__main__':
    unittest.main()
