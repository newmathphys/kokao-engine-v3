"""
KOKAO Engine v3.0.4 — Energy Management Module

Energy management and recovery system.
Система управления и восстановления энергии.
"""

import numpy as np
from typing import Dict, Any


class EnergyManager:
    """
    Energy management and recovery system.
    
    Attributes:
        energy (float): Current energy / Текущая энергия
        budget (float): Energy budget / Энергетический бюджет
    """
    
    def __init__(
        self,
        budget: float = 1.0,
        threshold: float = 0.25
    ):
        """
        Initialize energy manager.
        
        Args:
            budget: Initial energy budget / Начальный энергетический бюджет
            threshold: Hibernation threshold / Порог гибернации
        """
        self.energy = budget
        self.budget = budget
        self.threshold = threshold
        self.base_recovery = 0.005
        self.sleep_efficiency = 0.9
    
    def consume(
        self,
        cost: float,
        switches: int = 0
    ) -> None:
        """
        Consume energy.
        
        E(t+1) = E(t) - cost_computation - cost_context_switches
        
        Args:
            cost: Computation cost / Стоимость вычислений
            switches: Number of context switches / Число переключений контекста
        """
        switch_cost = switches * 0.001
        self.energy -= (cost + switch_cost)
        self.energy = max(0.0, self.energy)
    
    def recover(
        self,
        base: float = None,
        efficiency: float = None
    ) -> None:
        """
        Recover energy.
        
        E(t+1) = min(E_init, E(t) + base_recovery · sleep_efficiency)
        
        Args:
            base: Base recovery rate / Базовая скорость восстановления
            efficiency: Sleep efficiency / Эффективность сна
        """
        if base is None:
            base = self.base_recovery
        if efficiency is None:
            efficiency = self.sleep_efficiency
        
        recovery = base * efficiency
        self.energy = min(self.budget, self.energy + recovery)
    
    def is_hibernation_mode(self) -> bool:
        """
        Check if in hibernation mode.
        
        is_hibernation = E < E_threshold
        
        Returns:
            True if hibernation / True если гибернация
        """
        return self.energy < self.threshold
    
    def get_efficiency(self) -> float:
        """
        Get current energy efficiency.
        
        Returns:
            Efficiency ratio / Коэффициент эффективности
        """
        if self.budget <= 0:
            return 0.0
        return self.energy / self.budget
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get energy statistics.
        
        Returns:
            Dictionary with statistics / Словарь со статистикой
        """
        return {
            'energy': self.energy,
            'budget': self.budget,
            'efficiency': self.get_efficiency(),
            'hibernation': self.is_hibernation_mode()
        }
