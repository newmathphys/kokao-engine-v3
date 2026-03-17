# 📖 Code Documentation / Документация Кода KOKAO Engine v3.0.4

## API Reference / Справочник API

---

## 1. KOKAOEngine Class / Класс KOKAOEngine

**File:** `kokao/main.py`

### Class Definition / Определение Класса

```python
class KOKAOEngine:
    """
    Biologically Plausible Cognitive Architecture based on 
    Kosyakov's Theory of Functionally-Independent Structures.
    
    Achieves 92.92% average accuracy on 9 real UCR datasets.
    
    Attributes:
        d_model (int): Input dimension / Размерность входа
        n_classes (int): Number of classes / Число классов
        K_max (int): Maximum number of etalons / Макс. количество этапонов
        delta_base (float): Learning threshold / Порог обучения
        learning_rate (float): Learning rate / Скорость обучения
    
    Example:
        >>> engine = KOKAOEngine(d_model=140, n_classes=5)
        >>> engine.fit(X_train, y_train)
        >>> predictions = engine.predict(X_test)
    """
```

---

### Constructor / Конструктор

```python
def __init__(
    self,
    d_model: int = 140,
    n_classes: int = 5,
    K_max: int = 1500,
    delta_base: float = 0.05,
    learning_rate: float = 0.02,
    adaptive_learning: bool = True,
    stochastic_gain: float = 0.1,
    rhythm_enabled: bool = True,
    energy_efficient: bool = True
):
    """
    Initialize KOKAO Engine.
    
    Args:
        d_model: Input dimension / Размерность входа
        n_classes: Number of classes / Число классов
        K_max: Maximum etalons / Макс. этапонов
        delta_base: Learning threshold / Порог обучения
        learning_rate: Learning rate / Скорость обучения
        adaptive_learning: Enable adaptive LR / Включить адаптивную скорость
        stochastic_gain: Stochastic resonance gain / Коэф. стох. резонанса
        rhythm_enabled: Enable rhythm module / Включить ритмический модуль
        energy_efficient: Enable energy saving / Включить энергосбережение
    """
```

---

### Public Methods / Публичные Методы

#### `process(x, target=None)`

```python
def process(
    self,
    x: np.ndarray,
    target: Optional[int] = None
) -> Tuple[int, float]:
    """
    Process single sample (online training/prediction).
    
    Args:
        x: Input sample of shape (d_model,) / Входной сэмпл
        target: Optional target class / Опциональная целевая метка
    
    Returns:
        Tuple of (prediction, confidence) / Кортеж (предсказание, уверенность)
    
    Example:
        >>> pred, conf = engine.process(x_sample, target=y_sample)  # Train
        >>> pred, conf = engine.process(x_sample)  # Predict
    """
```

---

#### `fit(X, y)`

```python
def fit(
    self,
    X: np.ndarray,
    y: np.ndarray,
    verbose: bool = True
) -> 'KOKAOEngine':
    """
    Fit engine to training data (batch training).
    
    Args:
        X: Training data of shape (n_samples, d_model) / Обучающие данные
        y: Training labels of shape (n_samples,) / Обучающие метки
        verbose: Show progress / Показать прогресс
    
    Returns:
        self: Fitted engine / Обученный движок
    
    Example:
        >>> engine.fit(X_train, y_train)
    """
```

---

#### `predict(x, k=5)`

```python
def predict(
    self,
    x: np.ndarray,
    k: int = 5
) -> Tuple[int, float]:
    """
    Predict class for single sample.
    
    Args:
        x: Input sample of shape (d_model,) / Входной сэмпл
        k: Number of nearest etalons / Число ближайших этапонов
    
    Returns:
        Tuple of (prediction, confidence) / Кортеж (предсказание, уверенность)
    
    Example:
        >>> pred, conf = engine.predict(x_test)
    """
```

---

#### `predict_batch(X, k=5)`

```python
def predict_batch(
    self,
    X: np.ndarray,
    k: int = 5
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Predict classes for multiple samples.
    
    Args:
        X: Input data of shape (n_samples, d_model) / Входные данные
        k: Number of nearest etalons / Число ближайших этапонов
    
    Returns:
        Tuple of (predictions, confidences) / Кортеж (предсказания, уверенности)
    
    Example:
        >>> preds, confs = engine.predict_batch(X_test)
    """
```

---

#### `evaluate(X, y)`

```python
def evaluate(
    self,
    X: np.ndarray,
    y: np.ndarray
) -> float:
    """
    Evaluate accuracy on test data.
    
    Args:
        X: Test data of shape (n_samples, d_model) / Тестовые данные
        y: Test labels of shape (n_samples,) / Тестовые метки
    
    Returns:
        Accuracy score / Точность
    
    Example:
        >>> accuracy = engine.evaluate(X_test, y_test)
        >>> print(f"Accuracy: {accuracy:.4f}")
    """
```

---

#### `get_statistics()`

```python
def get_statistics(self) -> Dict[str, Any]:
    """
    Get engine statistics.
    
    Returns:
        Dictionary with statistics / Словарь со статистикой
    
    Example:
        >>> stats = engine.get_statistics()
        >>> print(f"Etalons: {stats['n_etalons']}")
        >>> print(f"Energy: {stats['energy']:.4f}")
    """
```

---

## 2. Etalon Class / Класс Эталона

**File:** `kokao/core/etalon.py`

### Class Definition / Определение Класса

```python
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
    
    Example:
        >>> etalon = Etalon(c_plus=x, c_minus=-0.1*x, class_label=y)
        >>> response = etalon.get_response(x_query)
    """
```

---

### Methods / Методы

#### `get_response(x)`

```python
def get_response(self, x: np.ndarray) -> float:
    """
    Compute etalon response: (c⁺·x) - (c⁻·x).
    
    Args:
        x: Input vector / Входной вектор
    
    Returns:
        Response value / Значение отклика
    """
```

---

#### `similarity(x)`

```python
def similarity(self, x: np.ndarray) -> float:
    """
    Compute cosine similarity with input.
    
    Args:
        x: Input vector / Входной вектор
    
    Returns:
        Cosine similarity / Косинусное сходство
    """
```

---

#### `update_weights(error, x, lr)`

```python
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
```

---

#### `get_purity()`

```python
def get_purity(self) -> float:
    """
    Compute class purity (dominant class ratio).
    
    Returns:
        Purity score ∈ [0, 1] / Оценка чистоты
    """
```

---

## 3. ContextMemory Class / Класс Контекстной Памяти

**File:** `kokao/core/memory.py`

### Class Definition / Определение Класса

```python
class ContextMemory:
    """
    STM/LTM Context Memory for etalon storage.
    
    Implements forgetting mechanism and class-specific thresholds.
    
    Attributes:
        etalons (List[Etalon]): Etalon list / Список этапонов
        K_max (int): Maximum capacity / Макс. вместимость
        delta_base (float): Base threshold / Базовый порог
        forgetting_factor (float): Forgetting rate / Коэф. забывания
    
    Example:
        >>> memory = ContextMemory(K_max=1500, delta_base=0.05)
        >>> memory.add_etalon(x, y)
        >>> nearest = memory.find_nearest(x_query, k=5)
    """
```

---

### Methods / Методы

#### `add_etalon(x, y)`

```python
def add_etalon(self, x: np.ndarray, y: int) -> Etalon:
    """
    Add new etalon to memory.
    
    Args:
        x: Input vector / Входной вектор
        y: Class label / Метка класса
    
    Returns:
        Created etalon / Созданный эталон
    """
```

---

#### `find_nearest(x, k=5)`

```python
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
```

---

#### `should_create(x, y)`

```python
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
```

---

#### `get_delta(class_label)`

```python
def get_delta(self, class_label: int) -> float:
    """
    Get class-specific threshold.
    
    Args:
        class_label: Class ID / ID класса
    
    Returns:
        Delta value / Значение дельты
    """
```

---

## 4. KosyakovLearningEngine Class / Класс Обучения Косякова

**File:** `kokao/core/learning.py`

### Class Definition / Определение Класса

```python
class KosyakovLearningEngine:
    """
    Learning engine based on Kosyakov's Formula (8).
    
    Implements adaptive learning rate and volatility tracking.
    
    Attributes:
        base_lr (float): Base learning rate / Базовая скорость обучения
        adaptive (bool): Adaptive learning flag / Флаг адаптивности
        lambda_T (float): Temperature parameter / Температурный параметр
        volatility (float): Market volatility / Волатильность рынка
    
    Example:
        >>> learner = KosyakovLearningEngine(base_lr=0.02, adaptive=True)
        >>> learner.train_step(etalon, x, target)
    """
```

---

### Methods / Методы

#### `train_step(etalon, x, target)`

```python
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
```

---

#### `compute_error(etalon, x, target)`

```python
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
```

---

#### `apply_formula_8(etalon, error, x)`

```python
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
```

---

## 5. Voting Functions / Функции Голосования

**File:** `kokao/core/voting.py`

### `weighted_voting_cosine(nearest, x, n_classes)`

```python
def weighted_voting_cosine(
    nearest: List[Tuple[int, float, Etalon]],
    x: np.ndarray,
    n_classes: int,
    temperature: float = 1.0,
    top_k: int = 5
) -> Tuple[int, float]:
    """
    Weighted voting with cosine similarity.
    
    Args:
        nearest: List of (id, sim, etalon) tuples
        x: Input vector / Входной вектор
        n_classes: Number of classes / Число классов
        temperature: Softmax temperature / Температура softmax
        top_k: Use top k etalons / Использовать топ k этапонов
    
    Returns:
        Tuple of (prediction, confidence)
    """
```

---

## 6. Module Classes / Классы Модулей

### StochasticResonance

**File:** `kokao/modules/stochastic.py`

```python
class StochasticResonance:
    """
    Adaptive stochastic resonance for signal enhancement.
    
    Methods:
        compute_surprise(P_return) -> float
        compute_beta(surprise) -> float  # β ∈ [0.1, 2.0]
        resonance_amplification(volatility) -> float
        add_adaptive_noise(signal, volatility) -> np.ndarray
    """
```

---

### RhythmModule

**File:** `kokao/modules/rhythm.py`

```python
class RhythmModule:
    """
    Go/No-Go signal generation based on volatility.
    
    Methods:
        compute_go_signal(volatility) -> Tuple[bool, Dict]
    """
```

---

### EnergyManager

**File:** `kokao/modules/energy.py`

```python
class EnergyManager:
    """
    Energy management and recovery system.
    
    Attributes:
        energy (float): Current energy / Текущая энергия
        budget (float): Energy budget / Энергетический бюджет
    
    Methods:
        consume(cost, switches) -> None
        recover(base, efficiency) -> None
        is_hibernation_mode() -> bool
    """
```

---

## 7. Type Definitions / Определения Типов

```python
from typing import (
    Dict,
    List,
    Tuple,
    Optional,
    Any,
    Union,
    Callable
)

import numpy as np
import numpy.typing as npt

# Type aliases / Псевдонимы типов
Vector = npt.NDArray[np.float64]
Matrix = npt.NDArray[np.float64]
EtalonTuple = Tuple[int, float, Etalon]
Prediction = Tuple[int, float]
```

---

## 8. Exceptions / Исключения

```python
class KOKAOError(Exception):
    """Base exception for KOKAO Engine."""
    pass


class EtalonError(KOKAOError):
    """Etalon-related errors."""
    pass


class MemoryError(KOKAOError):
    """Memory-related errors."""
    pass


class LearningError(KOKAOError):
    """Learning-related errors."""
    pass
```

---

## 9. Constants / Константы

```python
# Version / Версия
__version__ = "3.0.4"

# Default values / Значения по умолчанию
DEFAULT_D_MODEL = 140
DEFAULT_N_CLASSES = 5
DEFAULT_K_MAX = 1500
DEFAULT_DELTA_BASE = 0.05
DEFAULT_LEARNING_RATE = 0.02

# Weight clipping limits / Пределы ограничения весов
WEIGHT_CLIP_MIN = -2.0
WEIGHT_CLIP_MAX = 2.0

# Beta range for adaptive learning / Диапазон бета для адаптивного обучения
BETA_MIN = 0.1
BETA_MAX = 2.0
```

---

## 10. Testing / Тестирование

### Test Coverage / Покрытие тестами

| Module / Модуль | Coverage / Покрытие | Status / Статус |
|----------------|-------------------|----------------|
| **voting.py** | 96% | 🏆 Excellent |
| **learning.py** | 89% | ✅ Good |
| **memory.py** | 80% | ✅ Sufficient |
| **etalon.py** | 80% | ✅ Sufficient |
| **main.py** | 72% | ✅ Acceptable |
| **Core Average / Среднее по ядру** | **83.4%** | ✅ Publication Ready |

---

*Created by newmathphys / Создано newmathphys*

**KOKAO Engine v3.0.4**

Based on Kosyakov's Theory (1999)
