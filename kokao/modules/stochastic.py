"""
KOKAO Engine v3.0.4 — Stochastic Resonance Module

Adaptive stochastic resonance for signal enhancement.
Адаптивный стохастический резонанс для усиления сигнала.
"""

import numpy as np
from typing import Tuple


class StochasticResonance:
    """
    Adaptive stochastic resonance for signal enhancement.
    
    Methods:
        compute_surprise(P_return) -> float
        compute_beta(surprise) -> float  # β ∈ [0.1, 2.0]
        resonance_amplification(volatility) -> float
        add_adaptive_noise(signal, volatility) -> np.ndarray
    """
    
    def __init__(self, gain: float = 0.1):
        """
        Initialize stochastic resonance.
        
        Args:
            gain: Resonance gain / Коэффициент резонанса
        """
        self.gain = gain
        self.alpha = 0.0072973525693  # Fine structure constant
        self.n_magic = 8.52  # Magic number
        self.sigma = 20.0  # Standard deviation
    
    def compute_surprise(self, P_return: float) -> float:
        """
        Compute surprise from return probability.
        
        surprise = |P_return - α| / α
        
        Args:
            P_return: Return probability / Вероятность возврата
        
        Returns:
            Surprise value / Значение сюрприза
        """
        if self.alpha < 1e-10:
            return 0.0
        
        return abs(P_return - self.alpha) / self.alpha
    
    def compute_beta(self, surprise: float) -> float:
        """
        Compute beta from surprise.
        
        β ∈ [0.1, 2.0]
        
        Args:
            surprise: Surprise value / Значение сюрприза
        
        Returns:
            Beta value / Значение бета
        """
        beta = 1.0 / (1.0 + surprise)
        return np.clip(beta, 0.1, 2.0)
    
    def resonance_amplification(self, volatility: float, n_steps: int = 8) -> float:
        """
        Compute resonance amplification.
        
        amplification = 1 / (1 + ((n_steps - n_magic) / σ)²)
        
        Args:
            volatility: Signal volatility / Волатильность сигнала
            n_steps: Number of steps / Число шагов
        
        Returns:
            Amplification factor / Коэффициент усиления
        """
        diff = n_steps - self.n_magic
        amplification = 1.0 / (1.0 + (diff / self.sigma) ** 2)
        return amplification * (1.0 + volatility * self.gain)
    
    def add_adaptive_noise(
        self,
        signal: np.ndarray,
        volatility: float,
        beta: float = 1.0
    ) -> np.ndarray:
        """
        Add adaptive noise for stochastic resonance.
        
        noise = N(0, 1) · β · 0.1 · amplification
        x_enhanced = x + noise
        
        Args:
            signal: Input signal / Входной сигнал
            volatility: Signal volatility / Волатильность сигнала
            beta: Beta parameter / Параметр бета
        
        Returns:
            Enhanced signal / Усиленный сигнал
        """
        amplification = self.resonance_amplification(volatility)
        noise = np.random.normal(0, 1, signal.shape) * beta * 0.1 * amplification
        return signal + noise
