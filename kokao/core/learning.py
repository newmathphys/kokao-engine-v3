"""
KOKAO Engine v3.0.4 — Learning Module

Learning engine based on Kosyakov's Formula (8).
Движок обучения на основе Формулы (8) Косякова.
"""

import numpy as np
from typing import Dict, Any, Optional
from kokao.core.etalon import Etalon


class KosyakovLearningEngine:
    """
    Learning engine based on Kosyakov's Formula (8).
    
    Implements adaptive learning rate and volatility tracking.
    
    Attributes:
        base_lr (float): Base learning rate / Базовая скорость обучения
        adaptive (bool): Adaptive learning flag / Флаг адаптивности
        lambda_T (float): Temperature parameter / Температурный параметр
        volatility (float): Market volatility / Волатильность рынка
    """
    
    def __init__(
        self,
        base_lr: float = 0.02,
        adaptive: bool = True,
        lambda_T: float = 1.0
    ):
        """
        Initialize learning engine.
        
        Args:
            base_lr: Base learning rate / Базовая скорость обучения
            adaptive: Enable adaptive LR / Включить адаптивную скорость
            lambda_T: Temperature parameter / Температурный параметр
        """
        self.base_lr = base_lr
        self.adaptive = adaptive
        self.lambda_T = lambda_T
        self.volatility = 0.0
        self.error_history: list = []
    
    def train_step(
        self,
        etalon: Etalon,
        x: np.ndarray,
        target: int
    ) -> float:
        """
        Perform single learning step.
        
        Args:
            etalon: Target etalon / Целевой эталон
            x: Input vector / Входной вектор
            target: Target class / Целевой класс
        
        Returns:
            Error value / Значение ошибки
        """
        error = self.compute_error(etalon, x, target)
        self.apply_formula_8(etalon, error, x)
        
        self.error_history.append(abs(error))
        if len(self.error_history) > 100:
            self.error_history.pop(0)
        
        self._update_volatility()
        
        return error
    
    def compute_error(
        self,
        etalon: Etalon,
        x: np.ndarray,
        target: int
    ) -> float:
        """
        Compute learning error.
        
        Args:
            etalon: Target etalon / Целевой эталон
            x: Input vector / Входной вектор
            target: Target class / Целевой класс
        
        Returns:
            Error value / Значение ошибки
        """
        y_current = etalon.get_response(x)
        y_target = 1.0 if etalon.class_label == target else -1.0
        return y_target - y_current
    
    def apply_formula_8(
        self,
        etalon: Etalon,
        error: float,
        x: np.ndarray
    ) -> None:
        """
        Apply Formula (8) weight update.
        
        c⁺(t+1) = c⁺(t) + η · ε(t) · x(t)
        c⁻(t+1) = c⁻(t) - η · ε(t) · x(t)
        
        Args:
            etalon: Target etalon / Целевой эталон
            error: Learning error / Ошибка обучения
            x: Input vector / Входной вектор
        """
        lr = self.get_adaptive_lr()
        etalon.update_weights(error, x, lr)
    
    def get_adaptive_lr(self) -> float:
        """
        Get adaptive learning rate.
        
        Returns:
            Learning rate / Скорость обучения
        """
        if not self.adaptive:
            return self.base_lr
        
        if len(self.error_history) < 2:
            return self.base_lr
        
        volatility = np.std(self.error_history)
        surprise = abs(self.error_history[-1] - np.mean(self.error_history))
        
        beta = self._compute_beta(surprise)
        return self.base_lr * beta * (1.0 + volatility)
    
    def _compute_beta(self, surprise: float) -> float:
        """
        Compute beta from surprise.
        
        β ∈ [0.1, 2.0]
        
        Args:
            surprise: Surprise value / Значение сюрприза
        
        Returns:
            Beta value / Значение бета
        """
        alpha = 0.0072973525693
        if alpha < 1e-10:
            return 1.0
        
        surprise_normalized = abs(surprise - alpha) / alpha
        beta = 1.0 / (1.0 + surprise_normalized)
        return np.clip(beta, 0.1, 2.0)
    
    def _update_volatility(self) -> None:
        """Update volatility from error history."""
        if len(self.error_history) >= 2:
            self.volatility = np.std(self.error_history)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get learning statistics.
        
        Returns:
            Dictionary with statistics / Словарь со статистикой
        """
        if not self.error_history:
            return {
                'avg_error': 0.0,
                'volatility': 0.0,
                'current_lr': self.base_lr
            }
        
        return {
            'avg_error': np.mean(self.error_history),
            'volatility': self.volatility,
            'current_lr': self.get_adaptive_lr()
        }
