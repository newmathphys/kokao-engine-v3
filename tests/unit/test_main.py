"""
KOKAO Engine v3.0.4 — Unit Tests for Main Module

Tests for kokao.main.KOKAOEngine class.
"""

import unittest
import numpy as np
from kokao.main import KOKAOEngine


class TestKOKAOEngine(unittest.TestCase):
    """Test cases for KOKAOEngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.engine = KOKAOEngine(
            d_model=10,
            n_classes=3,
            K_max=100,
            learning_rate=0.02
        )
    
    def test_init(self):
        """Test engine initialization."""
        self.assertEqual(self.engine.d_model, 10)
        self.assertEqual(self.engine.n_classes, 3)
        self.assertEqual(self.engine.K_max, 100)
        self.assertEqual(self.engine.learning_rate, 0.02)
    
    def test_normalize(self):
        """Test L2 normalization."""
        x = np.array([3.0, 4.0])
        x_norm = self.engine._normalize(x)
        
        norm = np.linalg.norm(x_norm)
        self.assertAlmostEqual(norm, 1.0, places=5)
    
    def test_normalize_zero_vector(self):
        """Test normalization of zero vector."""
        x = np.zeros(10)
        x_norm = self.engine._normalize(x)
        
        # Should handle gracefully
        self.assertEqual(len(x_norm), 10)
    
    def test_process_train(self):
        """Test online training."""
        x = np.random.randn(10)
        pred, conf = self.engine.process(x, target=0)
        
        self.assertIsInstance(pred, int)
        self.assertIsInstance(conf, float)
        self.assertGreaterEqual(len(self.engine.memory.etalons), 1)
    
    def test_process_predict(self):
        """Test prediction without training."""
        # First add some etalons
        for _ in range(5):
            x = np.random.randn(10)
            self.engine.process(x, target=0)
        
        # Now predict
        x = np.random.randn(10)
        pred, conf = self.engine.process(x)
        
        self.assertIsInstance(pred, int)
        self.assertIsInstance(conf, float)
    
    def test_fit(self):
        """Test batch training."""
        X = np.random.randn(50, 10)
        y = np.random.randint(0, 3, 50)
        
        self.engine.fit(X, y, verbose=False)
        
        self.assertGreater(len(self.engine.memory.etalons), 0)
        self.assertEqual(self.engine._samples_processed, 50)
    
    def test_predict(self):
        """Test single prediction."""
        # Train first
        X = np.random.randn(30, 10)
        y = np.random.randint(0, 3, 30)
        self.engine.fit(X, y, verbose=False)
        
        # Predict
        x = np.random.randn(10)
        pred, conf = self.engine.predict(x)
        
        self.assertIsInstance(pred, int)
        self.assertGreaterEqual(pred, 0)
        self.assertLess(pred, 3)
        self.assertGreaterEqual(conf, 0.0)
        self.assertLessEqual(conf, 1.0)
    
    def test_predict_batch(self):
        """Test batch prediction."""
        # Train first
        X = np.random.randn(30, 10)
        y = np.random.randint(0, 3, 30)
        self.engine.fit(X, y, verbose=False)
        
        # Predict batch
        X_test = np.random.randn(10, 10)
        preds, confs = self.engine.predict_batch(X_test)
        
        self.assertEqual(len(preds), 10)
        self.assertEqual(len(confs), 10)
        self.assertIsInstance(preds, np.ndarray)
        self.assertIsInstance(confs, np.ndarray)
    
    def test_evaluate(self):
        """Test accuracy evaluation."""
        # Train
        X_train = np.random.randn(50, 10)
        y_train = np.random.randint(0, 3, 50)
        self.engine.fit(X_train, y_train, verbose=False)
        
        # Evaluate
        X_test = np.random.randn(20, 10)
        y_test = np.random.randint(0, 3, 20)
        accuracy = self.engine.evaluate(X_test, y_test)
        
        self.assertGreaterEqual(accuracy, 0.0)
        self.assertLessEqual(accuracy, 1.0)
    
    def test_get_statistics(self):
        """Test getting engine statistics."""
        stats = self.engine.get_statistics()
        
        self.assertIn('n_etalons', stats)
        self.assertIn('n_etalons_created', stats)
        self.assertIn('samples_processed', stats)
        
        # Train and check stats update
        X = np.random.randn(10, 10)
        y = np.random.randint(0, 3, 10)
        self.engine.fit(X, y, verbose=False)
        
        stats = self.engine.get_statistics()
        self.assertGreater(stats['n_etalons'], 0)
        self.assertGreater(stats['samples_processed'], 0)
    
    def test_energy_management(self):
        """Test energy management functionality."""
        engine = KOKAOEngine(
            d_model=10,
            n_classes=2,
            energy_efficient=True
        )
        
        self.assertIsNotNone(engine.energy)
        
        # Process some samples
        for _ in range(10):
            x = np.random.randn(10)
            engine.process(x, target=0)
        
        stats = engine.get_statistics()
        self.assertIn('energy', stats)
    
    def test_stochastic_resonance(self):
        """Test stochastic resonance module."""
        engine = KOKAOEngine(
            d_model=10,
            n_classes=2,
            stochastic_gain=0.1
        )
        
        self.assertIsNotNone(engine.stochastic)
        
        # Test surprise computation
        surprise = engine.stochastic.compute_surprise(P_return=0.3)
        self.assertGreaterEqual(surprise, 0)
    
    def test_rhythm_module(self):
        """Test rhythm module."""
        engine = KOKAOEngine(
            d_model=10,
            n_classes=2,
            rhythm_enabled=True
        )
        
        self.assertIsNotNone(engine.rhythm)
        
        # Test go signal
        go_signal, info = engine.rhythm.compute_go_signal(volatility=0.1)
        self.assertIsInstance(go_signal, bool)
        self.assertIn('go_probability', info)


class TestKOKAOEngineIntegration(unittest.TestCase):
    """Integration tests for KOKAOEngine."""
    
    def test_full_training_cycle(self):
        """Test complete training and prediction cycle."""
        np.random.seed(42)
        
        # Generate synthetic data
        n_samples = 100
        n_features = 20
        n_classes = 3
        
        X = np.random.randn(n_samples, n_features)
        y = np.random.randint(0, n_classes, n_samples)
        
        # Create and train engine
        engine = KOKAOEngine(
            d_model=n_features,
            n_classes=n_classes,
            K_max=50
        )
        
        engine.fit(X, y, verbose=False)
        
        # Evaluate on same data (should have decent accuracy)
        accuracy = engine.evaluate(X, y)
        
        # With online learning, should achieve better than random
        self.assertGreater(accuracy, 1.0 / n_classes)
    
    def test_brightness_invariance(self):
        """Test that prediction is invariant to input scaling."""
        np.random.seed(42)
        
        # Train
        X = np.random.randn(30, 10)
        y = np.random.randint(0, 2, 30)
        
        engine = KOKAOEngine(d_model=10, n_classes=2)
        engine.fit(X, y, verbose=False)
        
        # Test with different scales
        x_test = np.random.randn(10)
        scales = [0.1, 0.5, 1.0, 2.0, 10.0]
        
        predictions = []
        for scale in scales:
            pred, _ = engine.predict(x_test * scale)
            predictions.append(pred)
        
        # All predictions should be the same (brightness invariance)
        self.assertEqual(len(set(predictions)), 1)


if __name__ == '__main__':
    unittest.main()
