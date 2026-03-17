"""
KOKAO Engine v3.0.4 — Memory Module

STM/LTM Context Memory for etalon storage.
Контекстная память STM/LTM для хранения этапонов.
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from kokao.core.etalon import Etalon


class ContextMemory:
    """
    STM/LTM Context Memory for etalon storage.
    
    Implements forgetting mechanism and class-specific thresholds.
    
    Attributes:
        etalons (List[Etalon]): Etalon list / Список этапонов
        K_max (int): Maximum capacity / Макс. вместимость
        delta_base (float): Base threshold / Базовый порог
        forgetting_factor (float): Forgetting rate / Коэф. забывания
    """
    
    def __init__(
        self,
        K_max: int = 1500,
        delta_base: float = 0.05,
        forgetting_factor: float = 0.999
    ):
        """
        Initialize context memory.
        
        Args:
            K_max: Maximum etalons / Макс. этапонов
            delta_base: Base threshold / Базовый порог
            forgetting_factor: Forgetting rate / Коэф. забывания
        """
        self.etalons: List[Etalon] = []
        self.K_max = K_max
        self.delta_base = delta_base
        self.forgetting_factor = forgetting_factor
        self.class_deltas: Dict[int, float] = {}
    
    def add_etalon(self, x: np.ndarray, y: int) -> Etalon:
        """
        Add new etalon to memory.
        
        Args:
            x: Input vector / Входной вектор
            y: Class label / Метка класса
        
        Returns:
            Created etalon / Созданный эталон
        """
        etalon = Etalon(c_plus=x, c_minus=-0.1*x, class_label=y)
        
        if len(self.etalons) >= self.K_max:
            self._remove_oldest()
        
        self.etalons.append(etalon)
        return etalon
    
    def _remove_oldest(self) -> None:
        """Remove oldest etalon with lowest activity."""
        if not self.etalons:
            return
        
        min_idx = 0
        min_activity = self.etalons[0].activity
        
        for i, etalon in enumerate(self.etalons):
            if etalon.activity < min_activity:
                min_activity = etalon.activity
                min_idx = i
        
        self.etalons.pop(min_idx)
    
    def find_nearest(
        self,
        x: np.ndarray,
        k: int = 5
    ) -> List[Tuple[int, float, Etalon]]:
        """
        Find k nearest etalons.
        
        Args:
            x: Query vector / Запрашиваемый вектор
            k: Number of neighbors / Число соседей
        
        Returns:
            List of (id, similarity, etalon) tuples
        """
        if not self.etalons:
            return []
        
        similarities = []
        for i, etalon in enumerate(self.etalons):
            sim = etalon.similarity(x)
            similarities.append((i, sim, etalon))
        
        similarities.sort(key=lambda t: t[1], reverse=True)
        return similarities[:k]
    
    def should_create(self, x: np.ndarray, y: int) -> bool:
        """
        Check if new etalon should be created.
        
        Condition: similarity < 1 - delta_class
        
        Args:
            x: Input vector / Входной вектор
            y: Class label / Метка класса
        
        Returns:
            True if creation needed / True если нужно создание
        """
        if not self.etalons:
            return True
        
        nearest = self.find_nearest(x, k=1)
        if not nearest:
            return True
        
        delta = self.get_delta(y)
        similarity = nearest[0][1]
        
        return similarity < (1 - delta)
    
    def get_delta(self, class_label: int) -> float:
        """
        Get class-specific threshold.
        
        δ(c) = δ_base · (1 + n_etalons(c) / K_max)
        
        Args:
            class_label: Class ID / ID класса
        
        Returns:
            Delta value / Значение дельты
        """
        n_etalons = sum(
            1 for e in self.etalons if e.class_label == class_label
        )
        
        delta = self.delta_base * (1 + n_etalons / self.K_max)
        return min(delta, 0.5)
    
    def predict(self, x: np.ndarray, k: int = 5) -> Tuple[int, float]:
        """
        Predict class for input.
        
        Args:
            x: Input vector / Входной вектор
            k: Number of neighbors / Число соседей
        
        Returns:
            Tuple of (prediction, confidence)
        """
        from kokao.core.voting import weighted_voting_cosine
        
        nearest = self.find_nearest(x, k)
        if not nearest:
            return 0, 0.0
        
        n_classes = max(
            (max(e.class_counts.keys()) for e in self.etalons),
            default=0
        ) + 1
        
        return weighted_voting_cosine(nearest, x, n_classes)
    
    def cleanup(self, min_activity: float = 0.1) -> int:
        """
        Remove etalons with low activity.
        
        Args:
            min_activity: Minimum activity threshold / Мин. порог активности
        
        Returns:
            Number of removed etalons / Число удалённых этапонов
        """
        initial_count = len(self.etalons)
        self.etalons = [e for e in self.etalons if e.activity >= min_activity]
        return initial_count - len(self.etalons)
    
    def get_statistics(self) -> Dict:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with statistics / Словарь со статистикой
        """
        if not self.etalons:
            return {
                'n_etalons': 0,
                'n_classes': 0,
                'avg_activity': 0.0,
                'avg_age': 0.0
            }
        
        classes = set(e.class_label for e in self.etalons)
        activities = [e.activity for e in self.etalons]
        ages = [e.age for e in self.etalons]
        
        return {
            'n_etalons': len(self.etalons),
            'n_classes': len(classes),
            'avg_activity': np.mean(activities),
            'avg_age': np.mean(ages)
        }
