"""
KOKAO Engine v3.0.4 — Etalon Module

Implementation of c⁺/c⁻ etalon based on Kosyakov's Theory.
Реализация этапонов c⁺/c⁻ на основе теории Косякова.
"""

import numpy as np
from typing import Dict, Optional


class Etalon:
    """
    c⁺/c⁻ Etalon based on Kosyakov's Theory.
    
    Implements brightness-invariant recognition using S = S⁺/S⁻ ratio.
    
    Attributes:
        c_plus (np.ndarray): Excitatory weights / Возбуждающие веса
        c_minus (np.ndarray): Inhibitory weights / Тормозящие веса
        class_label (int): Dominant class / Доминирующий класс
        class_counts (Dict[int, int]): Class distribution / Распределение классов
        age (int): Age in samples / Возраст в сэмплах
        activity (float): Activity level / Уровень активности
    """
    
    def __init__(
        self,
        c_plus: np.ndarray,
        c_minus: Optional[np.ndarray] = None,
        class_label: int = 0
    ):
        """
        Initialize etalon.
        
        Args:
            c_plus: Excitatory weights / Возбуждающие веса
            c_minus: Inhibitory weights (default: -0.1 * c_plus) / Тормозящие веса
            class_label: Class label / Метка класса
        """
        self.c_plus = np.clip(c_plus.copy(), -2.0, 2.0)
        
        if c_minus is None:
            self.c_minus = -0.1 * self.c_plus
        else:
            self.c_minus = np.clip(c_minus.copy(), -2.0, 2.0)
        
        self.class_label = class_label
        self.class_counts: Dict[int, int] = {class_label: 1}
        self.age = 0
        self.activity = 1.0
    
    def get_response(self, x: np.ndarray) -> float:
        """
        Compute etalon response: R(x) = (x·c⁺) - (x·c⁻).
        
        Args:
            x: Input vector / Входной вектор
        
        Returns:
            Response value / Значение отклика
        """
        return np.dot(x, self.c_plus) - np.dot(x, self.c_minus)
    
    def similarity(self, x: np.ndarray) -> float:
        """
        Compute cosine similarity with input.
        
        Args:
            x: Input vector / Входной вектор
        
        Returns:
            Cosine similarity ∈ [0, 1] / Косинусное сходство
        """
        norm_x = np.linalg.norm(x)
        norm_c = np.linalg.norm(self.c_plus)
        
        if norm_x < 1e-10 or norm_c < 1e-10:
            return 0.0
        
        sim = np.dot(x, self.c_plus) / (norm_x * norm_c)
        return (sim + 1) / 2  # Normalize to [0, 1]
    
    def update_weights(
        self,
        error: float,
        x: np.ndarray,
        lr: float = 0.02
    ) -> None:
        """
        Update weights using Formula (8).
        
        c⁺(t+1) = c⁺(t) + η · ε(t) · x(t)
        c⁻(t+1) = c⁻(t) - η · ε(t) · x(t)
        
        Args:
            error: Learning error / Ошибка обучения
            x: Input vector / Входной вектор
            lr: Learning rate / Скорость обучения
        """
        self.c_plus = np.clip(
            self.c_plus + lr * error * x,
            -2.0, 2.0
        )
        self.c_minus = np.clip(
            self.c_minus - lr * error * x,
            -2.0, 2.0
        )
    
    def get_purity(self) -> float:
        """
        Compute class purity (dominant class ratio).
        
        Returns:
            Purity score ∈ [0, 1] / Оценка чистоты
        """
        if not self.class_counts:
            return 0.0
        
        total = sum(self.class_counts.values())
        if total == 0:
            return 0.0
        
        max_count = max(self.class_counts.values())
        return max_count / total
    
    def add_sample(self, class_label: int) -> None:
        """
        Add sample to class counts.
        
        Args:
            class_label: Class label / Метка класса
        """
        self.class_counts[class_label] = self.class_counts.get(class_label, 0) + 1
        self.age += 1
    
    def decay(self, tau: float = 50.0) -> None:
        """
        Apply activity decay.
        
        activity(t+1) = activity(t) · exp(-1/τ)
        
        Args:
            tau: Time constant / Время затухания
        """
        self.activity *= np.exp(-1.0 / tau)
        self.activity = np.clip(self.activity, 0.0, 1.0)
