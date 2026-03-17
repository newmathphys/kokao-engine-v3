"""
KOKAO Engine v3.0.4 — Unit Tests for Modules

Tests for kokao.modules (StochasticResonance, RhythmModule, EnergyManager).
"""

import unittest
import numpy as np
from kokao.modules.stochastic import StochasticResonance
from kokao.modules.rhythm import RhythmModule
from kokao.modules.energy import EnergyManager


class TestStochasticResonance(unittest.TestCase):
    """Test cases for StochasticResonance class."""
    
    def setUp(self):
        """Set up test fixtures."""
        np.random.seed(42)
        self.sr = StochasticResonance(gain=0.1)
    
    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.sr.gain, 0.1)
        self.assertAlmostEqual(self.sr.alpha, 0.0072973525693)
        self.assertEqual(self.sr.n_magic, 8.52)
        self.assertEqual(self.sr.sigma, 20.0)
    
    def test_compute_surprise(self):
        """Test surprise computation."""
        surprise = self.sr.compute_surprise(P_return=0.3)
        self.assertGreater(surprise, 0)
        
        # When P_return equals alpha, surprise should be 0
        surprise_zero = self.sr.compute_surprise(P_return=self.sr.alpha)
        self.assertAlmostEqual(surprise_zero, 0.0, places=5)
    
    def test_compute_beta(self):
        """Test beta computation."""
        beta = self.sr.compute_beta(surprise=0.0)
        self.assertAlmostEqual(beta, 1.0)
        
        # High surprise should give low beta
        beta_low = self.sr.compute_beta(surprise=100.0)
        self.assertAlmostEqual(beta_low, 0.1, places=2)
        
        # Beta should be in [0.1, 2.0]
        for surprise in [0.0, 0.5, 1.0, 10.0, 100.0]:
            beta = self.sr.compute_beta(surprise)
            self.assertGreaterEqual(beta, 0.1)
            self.assertLessEqual(beta, 2.0)
    
    def test_resonance_amplification(self):
        """Test resonance amplification."""
        amp = self.sr.resonance_amplification(volatility=0.1, n_steps=8)
        self.assertGreater(amp, 0)
        
        # Maximum amplification at n_magic
        amp_max = self.sr.resonance_amplification(volatility=0.0, n_steps=8.52)
        amp_off = self.sr.resonance_amplification(volatility=0.0, n_steps=0)
        
        self.assertGreater(amp_max, amp_off)
    
    def test_add_adaptive_noise(self):
        """Test adding adaptive noise."""
        signal = np.ones(100)
        enhanced = self.sr.add_adaptive_noise(signal, volatility=0.1)
        
        self.assertEqual(enhanced.shape, signal.shape)
        # Enhanced signal should be different from original
        self.assertFalse(np.array_equal(enhanced, signal))
    
    def test_add_adaptive_noise_reproducibility(self):
        """Test noise addition reproducibility with seed."""
        signal = np.ones(100)
        
        np.random.seed(42)
        enhanced1 = self.sr.add_adaptive_noise(signal, volatility=0.1)
        
        np.random.seed(42)
        enhanced2 = self.sr.add_adaptive_noise(signal, volatility=0.1)
        
        np.testing.assert_array_equal(enhanced1, enhanced2)


class TestRhythmModule(unittest.TestCase):
    """Test cases for RhythmModule class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rhythm = RhythmModule(threshold=0.3)
    
    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.rhythm.threshold, 0.3)
    
    def test_compute_go_signal(self):
        """Test Go/No-Go signal computation."""
        # High amplification should give GO
        go_signal, info = self.rhythm.compute_go_signal(
            volatility=0.1,
            amplification=0.8
        )
        self.assertTrue(go_signal)
        self.assertEqual(info['state'], 'GO')
        
        # Low amplification should give NO-GO
        go_signal, info = self.rhythm.compute_go_signal(
            volatility=0.1,
            amplification=0.1
        )
        self.assertFalse(go_signal)
        self.assertEqual(info['state'], 'NO-GO')
    
    def test_compute_go_signal_threshold(self):
        """Test threshold behavior."""
        # At threshold
        go_signal, info = self.rhythm.compute_go_signal(
            volatility=0.1,
            amplification=0.3
        )
        self.assertFalse(go_signal)  # > threshold, not >=
        
        # Just above threshold
        go_signal, info = self.rhythm.compute_go_signal(
            volatility=0.1,
            amplification=0.31
        )
        self.assertTrue(go_signal)
    
    def test_compute_go_signal_info(self):
        """Test info dictionary contents."""
        go_signal, info = self.rhythm.compute_go_signal(
            volatility=0.5,
            amplification=0.6
        )
        
        self.assertIn('go_probability', info)
        self.assertIn('volatility', info)
        self.assertIn('threshold', info)
        self.assertIn('state', info)
        
        self.assertAlmostEqual(info['go_probability'], 0.6)
        self.assertAlmostEqual(info['volatility'], 0.5)


class TestEnergyManager(unittest.TestCase):
    """Test cases for EnergyManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.energy = EnergyManager(budget=1.0, threshold=0.25)
    
    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.energy.energy, 1.0)
        self.assertEqual(self.energy.budget, 1.0)
        self.assertEqual(self.energy.threshold, 0.25)
    
    def test_consume(self):
        """Test energy consumption."""
        initial = self.energy.energy
        self.energy.consume(cost=0.1)
        
        self.assertAlmostEqual(self.energy.energy, initial - 0.1)
    
    def test_consume_with_switches(self):
        """Test energy consumption with context switches."""
        initial = self.energy.energy
        self.energy.consume(cost=0.1, switches=5)
        
        expected = initial - 0.1 - (5 * 0.001)
        self.assertAlmostEqual(self.energy.energy, expected, places=5)
    
    def test_consume_minimum(self):
        """Test that energy doesn't go below 0."""
        self.energy.consume(cost=10.0)
        self.assertGreaterEqual(self.energy.energy, 0.0)
    
    def test_recover(self):
        """Test energy recovery."""
        self.energy.energy = 0.5
        self.energy.recover(base=0.1, efficiency=0.9)
        
        self.assertAlmostEqual(self.energy.energy, 0.5 + 0.1 * 0.9)
    
    def test_recover_maximum(self):
        """Test that energy doesn't exceed budget."""
        self.energy.energy = 0.95
        self.energy.recover(base=0.1, efficiency=1.0)
        
        self.assertLessEqual(self.energy.energy, self.energy.budget)
    
    def test_is_hibernation_mode(self):
        """Test hibernation mode detection."""
        self.energy.energy = 0.3
        self.assertFalse(self.energy.is_hibernation_mode())
        
        self.energy.energy = 0.2
        self.assertTrue(self.energy.is_hibernation_mode())
    
    def test_get_efficiency(self):
        """Test efficiency computation."""
        self.energy.energy = 1.0
        self.assertAlmostEqual(self.energy.get_efficiency(), 1.0)
        
        self.energy.energy = 0.5
        self.assertAlmostEqual(self.energy.get_efficiency(), 0.5)
        
        self.energy.energy = 0.0
        self.assertAlmostEqual(self.energy.get_efficiency(), 0.0)
    
    def test_get_statistics(self):
        """Test getting statistics."""
        stats = self.energy.get_statistics()
        
        self.assertIn('energy', stats)
        self.assertIn('budget', stats)
        self.assertIn('efficiency', stats)
        self.assertIn('hibernation', stats)
        
        self.assertEqual(stats['energy'], self.energy.energy)
        self.assertEqual(stats['budget'], self.energy.budget)


class TestEnergyManagerScenarios(unittest.TestCase):
    """Test energy manager in various scenarios."""
    
    def test_consume_recover_cycle(self):
        """Test consume-recover cycle."""
        energy = EnergyManager(budget=1.0)
        
        for _ in range(10):
            energy.consume(cost=0.05)
            energy.recover(base=0.02)
        
        # Energy should still be positive
        self.assertGreater(energy.energy, 0)
    
    def test_hibernation_recovery(self):
        """Test recovery from hibernation."""
        energy = EnergyManager(budget=1.0, threshold=0.25)
        
        # Deplete energy
        energy.consume(cost=1.0)
        self.assertTrue(energy.is_hibernation_mode())
        
        # Recover
        for _ in range(100):
            energy.recover(base=0.01)
        
        # Should eventually exit hibernation
        if energy.energy >= energy.threshold:
            self.assertFalse(energy.is_hibernation_mode())


if __name__ == '__main__':
    unittest.main()
