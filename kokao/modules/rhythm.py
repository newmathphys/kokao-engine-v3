"""
KOKAO Engine v3.0.4 — Rhythm Module

Go/No-Go signal generation based on volatility.
Генерация сигналов Go/No-Go на основе волатильности.
"""

import numpy as np
from typing import Tuple, Dict, Any


class RhythmModule:
    """
    Go/No-Go signal generation based on volatility.
    
    Methods:
        compute_go_signal(volatility) -> Tuple[bool, Dict]
    """
    
    def __init__(self, threshold: float = 0.3):
        """
        Initialize rhythm module.
        
        Args:
            threshold: Go signal threshold / Порог Go-сигнала
        """
        self.threshold = threshold
    
    def compute_go_signal(
        self,
        volatility: float,
        amplification: float = 1.0
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Compute Go/No-Go signal.
        
        go_probability = amplification
        go_signal = go_probability > threshold
        
        Args:
            volatility: Signal volatility / Волатильность сигнала
            amplification: Resonance amplification / Резонансное усиление
        
        Returns:
            Tuple of (go_signal, info dict)
        """
        go_probability = amplification
        go_signal = go_probability > self.threshold
        
        info = {
            'go_probability': float(go_probability),
            'volatility': float(volatility),
            'threshold': self.threshold,
            'state': 'GO' if go_signal else 'NO-GO'
        }
        
        return go_signal, info
