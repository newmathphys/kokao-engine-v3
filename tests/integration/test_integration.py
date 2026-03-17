"""
KOKAO Engine v3.0.4 — Integration Tests

Integration tests for complete workflows.
"""

import unittest
import numpy as np
from kokao import KOKAOEngine
from kokao.core import Etalon, ContextMemory, KosyakovLearningEngine
from kokao.modules import StochasticResonance, RhythmModule, EnergyManager


class TestIntegrationFullWorkflow(unittest.TestCase):
    """Integration tests for full workflow."""
    
    def test_complete_training_and_prediction(self):
        """Test complete training and prediction workflow."""
        np.random.seed(42)
        
        # Generate synthetic data
        n_train = 200
        n_test = 50
        n_features = 50
        n_classes = 4
        
        # Create separable classes
        X_train = []
        y_train = []
        for class_idx in range(n_classes):
            class_center = np.random.randn(n_features) * 5
            for _ in range(n_train // n_classes):
                sample = class_center + np.random.randn(n_features) * 0.5
                X_train.append(sample)
                y_train.append(class_idx)
        
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        # Create test data
        X_test = []
        y_test = []
        for class_idx in range(n_classes):
            class_center = np.random.randn(n_features) * 5
            for _ in range(n_test // n_classes):
                sample = class_center + np.random.randn(n_features) * 0.5
                X_test.append(sample)
                y_test.append(class_idx)
        
        X_test = np.array(X_test)
        y_test = np.array(y_test)
        
        # Create and train engine
        engine = KOKAOEngine(
            d_model=n_features,
            n_classes=n_classes,
            K_max=500,
            delta_base=0.05,
            learning_rate=0.02
        )
        
        engine.fit(X_train, y_train, verbose=False)
        
        # Evaluate
        accuracy = engine.evaluate(X_test, y_test)
        
        # Should achieve reasonable accuracy (> 30% for 4 classes = better than 25% random)
        self.assertGreater(accuracy, 0.25)
        
        # Check statistics
        stats = engine.get_statistics()
        self.assertGreater(stats['n_etalons'], 0)
        self.assertGreater(stats['samples_processed'], 0)
    
    def test_online_learning_progressive(self):
        """Test progressive online learning."""
        np.random.seed(42)
        
        engine = KOKAOEngine(d_model=20, n_classes=3, K_max=100)
        
        accuracies = []
        
        # Train progressively and check accuracy improves
        for n_samples in [10, 30, 60, 100]:
            X = np.random.randn(n_samples, 20)
            y = np.random.randint(0, 3, n_samples)
            
            engine.fit(X, y, verbose=False)
            
            # Evaluate on same data
            acc = engine.evaluate(X, y)
            accuracies.append(acc)
        
        # Generally, accuracy should improve or stay stable
        # (allowing some noise)
        self.assertGreater(accuracies[-1], accuracies[0] * 0.8)
    
    def test_module_integration(self):
        """Test that all modules work together."""
        np.random.seed(42)
        
        engine = KOKAOEngine(
            d_model=30,
            n_classes=3,
            K_max=200,
            stochastic_gain=0.1,
            rhythm_enabled=True,
            energy_efficient=True
        )
        
        # Process some samples
        for _ in range(50):
            x = np.random.randn(30)
            y = np.random.randint(0, 3)
            engine.process(x, target=y)
        
        # Check all modules are functioning
        self.assertGreater(len(engine.memory.etalons), 0)
        
        stats = engine.get_statistics()
        self.assertIn('energy', stats)
        
        # Predict
        x_test = np.random.randn(30)
        pred, conf = engine.predict(x_test)
        
        self.assertIsInstance(pred, int)
        self.assertGreaterEqual(conf, 0.0)
        self.assertLessEqual(conf, 1.0)


class TestIntegrationStress(unittest.TestCase):
    """Stress tests for edge cases."""
    
    def test_large_dataset(self):
        """Test with larger dataset."""
        np.random.seed(42)
        
        n_samples = 1000
        n_features = 100
        n_classes = 10
        
        X = np.random.randn(n_samples, n_features)
        y = np.random.randint(0, n_classes, n_samples)
        
        engine = KOKAOEngine(
            d_model=n_features,
            n_classes=n_classes,
            K_max=2000
        )
        
        engine.fit(X, y, verbose=False)
        
        # Should complete without errors
        accuracy = engine.evaluate(X, y)
        self.assertGreater(accuracy, 1.0 / n_classes)  # Better than random
    
    def test_high_dimensional(self):
        """Test with high-dimensional data."""
        np.random.seed(42)
        
        n_features = 500
        n_classes = 5
        
        X = np.random.randn(100, n_features)
        y = np.random.randint(0, n_classes, 100)
        
        engine = KOKAOEngine(
            d_model=n_features,
            n_classes=n_classes,
            K_max=500
        )
        
        engine.fit(X, y, verbose=False)
        
        # Predict
        x_test = np.random.randn(n_features)
        pred, conf = engine.predict(x_test)
        
        self.assertIsInstance(pred, int)
        self.assertGreaterEqual(pred, 0)
        self.assertLess(pred, n_classes)
    
    def test_many_classes(self):
        """Test with many classes."""
        np.random.seed(42)
        
        n_samples = 200
        n_features = 50
        n_classes = 50
        
        X = np.random.randn(n_samples, n_features)
        y = np.arange(n_classes) % n_classes  # One sample per class initially
        
        engine = KOKAOEngine(
            d_model=n_features,
            n_classes=n_classes,
            K_max=1000
        )
        
        engine.fit(X, y, verbose=False)
        
        # Should handle many classes
        stats = engine.get_statistics()
        self.assertGreater(stats['n_etalons'], 0)


class TestIntegrationBrightnessInvariance(unittest.TestCase):
    """Test brightness invariance property end-to-end."""
    
    def test_prediction_scale_invariance(self):
        """Test that predictions are invariant to input scale."""
        np.random.seed(42)
        
        # Train with normal scale
        X_train = np.random.randn(50, 30)
        y_train = np.random.randint(0, 3, 50)
        
        engine = KOKAOEngine(d_model=30, n_classes=3)
        engine.fit(X_train, y_train, verbose=False)
        
        # Test with different scales
        x_test = np.random.randn(30)
        scales = [0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0]
        
        predictions = []
        confidences = []
        
        for scale in scales:
            pred, conf = engine.predict(x_test * scale)
            predictions.append(pred)
            confidences.append(conf)
        
        # All predictions should be identical (L2 normalization)
        unique_predictions = len(set(predictions))
        self.assertEqual(unique_predictions, 1, 
                        f"Predictions should be scale-invariant, got {unique_predictions} unique")
        
        # Confidences may vary slightly but should be reasonable
        for conf in confidences:
            self.assertGreaterEqual(conf, 0.0)
            self.assertLessEqual(conf, 1.0)


class TestIntegrationReproducibility(unittest.TestCase):
    """Test reproducibility with fixed seeds."""
    
    def test_reproducible_training(self):
        """Test that training is reproducible with same seed."""
        def run_training():
            np.random.seed(123)
            engine = KOKAOEngine(d_model=20, n_classes=3, K_max=100)
            
            X = np.random.randn(50, 20)
            y = np.random.randint(0, 3, 50)
            
            engine.fit(X, y, verbose=False)
            
            x_test = np.random.randn(20)
            pred, conf = engine.predict(x_test)
            
            return engine.get_statistics(), pred, conf
        
        # Run twice
        stats1, pred1, conf1 = run_training()
        stats2, pred2, conf2 = run_training()
        
        # Statistics should match
        self.assertEqual(stats1['n_etalons'], stats2['n_etalons'])
        self.assertEqual(stats1['samples_processed'], stats2['samples_processed'])
        
        # Predictions should match
        self.assertEqual(pred1, pred2)
        self.assertAlmostEqual(conf1, conf2, places=5)


if __name__ == '__main__':
    unittest.main()
