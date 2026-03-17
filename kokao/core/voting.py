"""
KOKAO Engine v3.0.4 — Voting Module

Weighted voting system for classification.
Взвешенная система голосования для классификации.
"""

import numpy as np
from typing import List, Tuple, Dict, Any
from kokao.core.etalon import Etalon


def weighted_voting_cosine(
    nearest: List[Tuple[int, float, Etalon]],
    x: np.ndarray,
    n_classes: int,
    temperature: float = 1.0,
    top_k: int = 5
) -> Tuple[int, float]:
    """
    Weighted voting with cosine similarity.
    
    votes[c] = Σ(sim(x, e_i) · purity(e_i) · activity(e_i))
    P(c) = exp(votes[c] / T) / Σ(exp(votes[k] / T))
    
    Args:
        nearest: List of (id, sim, etalon) tuples
        x: Input vector / Входной вектор
        n_classes: Number of classes / Число классов
        temperature: Softmax temperature / Температура softmax
        top_k: Use top k etalons / Использовать топ k этапонов
    
    Returns:
        Tuple of (prediction, confidence)
    """
    if not nearest:
        return 0, 0.0
    
    votes = np.zeros(n_classes)
    
    for etalon_id, similarity, etalon in nearest[:top_k]:
        dominant_class = max(etalon.class_counts, key=etalon.class_counts.get)
        purity = etalon.get_purity()
        weight = similarity * purity * etalon.activity
        
        if dominant_class < n_classes:
            votes[dominant_class] += weight
    
    probabilities = softmax(votes / temperature)
    prediction = int(np.argmax(probabilities))
    confidence = float(probabilities[prediction])
    
    return prediction, confidence


def softmax(x: np.ndarray) -> np.ndarray:
    """
    Compute softmax with numerical stability.
    
    P(c) = exp(x[c]) / Σ(exp(x[k]))
    
    Args:
        x: Input array / Входной массив
    
    Returns:
        Softmax probabilities / Вероятности softmax
    """
    x = np.asarray(x, dtype=np.float64)
    
    if len(x) == 0:
        return np.array([])
    
    x_max = np.max(x)
    exp_x = np.exp(x - x_max)
    sum_exp = np.sum(exp_x)
    
    if sum_exp < 1e-10:
        return np.ones(len(x)) / len(x)
    
    return exp_x / sum_exp


def simple_voting(
    nearest: List[Tuple[int, float, Etalon]],
    n_classes: int,
    top_k: int = 5
) -> Tuple[int, float]:
    """
    Simple majority voting (fallback).
    
    Args:
        nearest: List of (id, sim, etalon) tuples
        n_classes: Number of classes / Число классов
        top_k: Use top k etalons / Использовать топ k этапонов
    
    Returns:
        Tuple of (prediction, confidence)
    """
    if not nearest:
        return 0, 0.0
    
    class_votes: Dict[int, float] = {}
    
    for etalon_id, similarity, etalon in nearest[:top_k]:
        dominant_class = max(etalon.class_counts, key=etalon.class_counts.get)
        class_votes[dominant_class] = class_votes.get(dominant_class, 0) + similarity
    
    if not class_votes:
        return 0, 0.0
    
    prediction = max(class_votes, key=class_votes.get)
    total_votes = sum(class_votes.values())
    confidence = class_votes[prediction] / total_votes if total_votes > 0 else 0.0
    
    return prediction, confidence
