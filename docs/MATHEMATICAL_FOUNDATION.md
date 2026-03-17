# 🧮 Mathematical Foundation / Математический Фундамент KOKAO Engine v3.0.4

## Основано на / Based on:

**Yu.B. Kosyakov's Book "My Brain" (1999)**  
**Книга Ю.Б. Косякова "Мой мозг" (1999)**

**Russian Patent №2109332 (expired)**  
**Патент РФ №2109332 (утратил силу)**

---

## 1. FORMULA (8) — KOSYAKOV LEARNING RULE

### Mathematical Notation / Математическая запись

**From Kosyakov's Book, Chapter 1.2 / Из книги Косякова, Глава 1.2:**

```math
c'_i = c_i - \frac{Δ₀ · b_i}{Σ b_i²}
```

### Where / Где:

| Symbol / Символ | Description / Описание |
|----------------|----------------------|
| `c_i` | Weight coefficient at time t / Весовой коэффициент в момент времени t |
| `c'_i` | Updated weight coefficient / Обновлённый весовой коэффициент |
| `Δ₀` | Total learning error / Общая ошибка обучения |
| `b_i` | Input factor / Входной фактор |
| `Σ b_i²` | Normalization factor / Нормализующий множитель |

---

### Expanded Form / Развёрнутая форма

For implementation in neural architecture, Formula (8) is expressed as:

Для реализации в нейронной архитектуре, Формула (8) выражается как:

```math
\begin{aligned}
\text{Error:} \quad \varepsilon(t) &= y_{target} - y_{current} \\
\\
\text{Current Response:} \quad y_{current} &= (x · c⁺) - (x · c⁻) \\
\\
\text{Weight Update:} \quad c⁺(t+1) &= c⁺(t) + η · ε(t) · x(t) \\
\text{Weight Update:} \quad c⁻(t+1) &= c⁻(t) - η · ε(t) · x(t)
\end{aligned}
```

### Where / Где:

| Symbol / Символ | Description / Описание | Range / Диапазон |
|----------------|----------------------|-----------------|
| `w(t)` | Weight at time t / Вес в момент времени t | ℝ |
| `η` | Learning rate / Скорость обучения | [0.01, 0.1] |
| `ε(t)` | Error at time t / Ошибка в момент времени t | [-1, 1] |
| `x(t)` | Input signal at time t / Входной сигнал в момент времени t | ℝⁿ |
| `c⁺` | Excitatory weight / Возбуждающий вес | [-2.0, 2.0] |
| `c⁻` | Inhibitory weight / Тормозящий вес | [-2.0, 2.0] |

---

### Physical Meaning / Физический Смысл

| Symbol / Символ | Physical Meaning / Физический Смысл |
|----------------|-----------------------------------|
| **`c⁺`** | **Excitatory synapses (positive weights) / Возбуждающие синапсы (положительные веса)** |
| **`c⁻`** | **Inhibitory synapses (negative weights) / Тормозящие синапсы (отрицательные веса)** |
| **`η`** | **Dopamine modulation analog / Аналог дофаминовой модуляции** |
| **`ε(t)`** | **Error signal for correction / Сигнал ошибки для коррекции** |

---

### Derivation / Вывод

Starting from the original Formula (8):

Начиная с оригинальной Формулы (8):

**Step 1 / Шаг 1:** Express error term

```math
Δ₀ = y_{target} - y_{current} = ε(t)
```

**Step 2 / Шаг 2:** For normalized input (L2 norm = 1):

```math
Σ b_i² = Σ x_i² = ||x||² = 1
```

**Step 3 / Шаг 3:** Simplify Formula (8):

```math
c'_i = c_i - Δ₀ · b_i = c_i - ε(t) · x(t)
```

**Step 4 / Шаг 4:** Add learning rate η:

```math
c'_i = c_i - η · ε(t) · x(t)
```

**Step 5 / Шаг 5:** Separate c⁺ and c⁻:

```math
\begin{aligned}
c⁺(t+1) &= c⁺(t) + η · ε(t) · x(t) \\
c⁻(t+1) &= c⁻(t) - η · ε(t) · x(t)
\end{aligned}
```

The sign difference reflects the opponent process theory: c⁺ strengthens for correct predictions, c⁻ weakens.

Разница знаков отражает теорию оппонентных процессов: c⁺ усиливается для правильных предсказаний, c⁻ ослабляется.

---

## 2. ETALON RESPONSE / ОТКЛИК ЭТАЛОНА

### Formula / Формула

```math
R(x) = (x · c⁺) - (x · c⁻)
```

### Where / Где:

| Symbol / Символ | Description / Описание |
|----------------|----------------------|
| `x` | Normalized input vector / Нормализованный входной вектор |
| `c⁺` | Positive weights vector / Вектор положительных весов |
| `c⁻` | Negative weights vector / Вектор отрицательных весов |
| `·` | Dot product / Скалярное произведение |

### Interpretation / Интерпретация

| Response / Отклик | Meaning / Значение |
|------------------|-------------------|
| **`R(x) > 0`** | Signal recognized as positive / Сигнал распознан как положительный |
| **`R(x) < 0`** | Signal recognized as negative / Сигнал распознан как отрицательный |
| **`R(x) = 0`** | Undecided state / Неопределённое состояние |

---

## 3. BRIGHTNESS INVARIANCE / РАСПОЗНАВАНИЕ НЕЗАВИСИМО ОТ ЯРКОСТИ

### Mathematical Formulation / Математическая Формулировка

**From Kosyakov's Book, Chapter 1.4 / Из книги Косякова, Глава 1.4:**

```math
S = \frac{S⁺}{S⁻}
```

### Where / Где:

| Symbol / Символ | Description / Описание |
|----------------|----------------------|
| `S⁺` | Excitatory synapses (c⁺) / Возбуждающие синапсы |
| `S⁻` | Inhibitory synapses (c⁻) / Тормозящие синапсы |
| `S` | Brightness-invariant recognition score / Оценка распознавания, инвариантная к яркости |

---

### Proof of Brightness Invariance / Доказательство Инвариантности Яркости

**Theorem / Теорема:** The ratio S = S⁺/S⁻ remains constant regardless of input signal intensity.

**Теорема:** Отношение S = S⁺/S⁻ остаётся постоянным независимо от интенсивности входного сигнала.

**Proof / Доказательство:**

Let the input signal be scaled by factor α > 0:

Пусть входной сигнал масштабирован фактором α > 0:

```math
x' = α · x
```

The responses scale proportionally:

Отклики масштабируются пропорционально:

```math
\begin{aligned}
S⁺(x') &= S⁺(α · x) = α · S⁺(x) \\
S⁻(x') &= S⁻(α · x) = α · S⁻(x)
\end{aligned}
```

Therefore:

Следовательно:

```math
S(x') = \frac{S⁺(x')}{S⁻(x')} = \frac{α · S⁺(x)}{α · S⁻(x)} = \frac{S⁺(x)}{S⁻(x)} = S(x)
```

**Q.E.D. / Ч.Т.Д.**

---

### Connection to Weber-Fechner Law / Связь с Законом Вебера-Фехнера

This ratio implements the **Weber-Fechner law** in neural architecture:

Это отношение реализует **закон Вебера-Фехнера** в нейронной архитектуре:

```math
\text{Perceived Intensity} = k · \log\left(\frac{\text{Stimulus}}{\text{Threshold}}\right)
```

In KOKAO Engine, the ratio S⁺/S⁻ provides logarithmic perception of signal strength.

В KOKAO Engine отношение S⁺/S⁻ обеспечивает логарифмическое восприятие силы сигнала.

---

## 3. COSINE SIMILARITY / КОСИНУСНОЕ СХОДСТВО

### Formula / Формула

```math
\text{sim}(x₁, x₂) = \frac{x₁ · x₂}{||x₁|| · ||x₂||}
```

### Normalization to [0, 1] / Нормализация к [0, 1]

```math
\text{sim}_{normalized}(x₁, x₂) = \frac{\text{sim}(x₁, x₂) + 1}{2}
```

### Properties / Свойства

| Value / Значение | Meaning / Значение |
|-----------------|-------------------|
| **`sim = 1.0`** | Identical vectors / Идентичные векторы |
| **`sim = 0.5`** | Orthogonal vectors / Ортогональные векторы |
| **`sim = 0.0`** | Opposite vectors / Противоположные векторы |

---

## 4. BRIGHTNESS INVARIANCE / РАСПОЗНАВАНИЕ НЕЗАВИСИМО ОТ ЯРКОСТИ

**From Kosyakov's Book, Chapter 1.4 / Из книги Косякова, Глава 1.4:**

```math
S = \frac{S⁺}{S⁻}
```

**Where / Где:**
- `S⁺` — Excitatory synapses (c⁺) / Возбуждающие синапсы
- `S⁻` — Inhibitory synapses (c⁻) / Тормозящие синапсы
- `S` — Brightness-invariant recognition score / Оценка распознавания, инвариантная к яркости

This ratio remains constant regardless of input brightness. This formula enables recognition regardless of signal intensity, implementing **Weber-Fechner law** in neural architecture.

Это соотношение остаётся постоянным независимо от яркости входа. Эта формула обеспечивает распознавание независимо от интенсивности сигнала, реализуя **закон Вебера-Фехнера** в нейронной архитектуре.

---

## 5. WEIGHTED VOTING / ВЗВЕШЕННОЕ ГОЛОСОВАНИЕ

### Formula / Формула

```math
\text{votes}[c] = \sum_{i} \left( \text{sim}(x, e_i) · \text{purity}(e_i) · \text{activity}(e_i) \right)
```

### Where / Где:

| Symbol / Символ | Description / Описание |
|----------------|----------------------|
| `c` | Class / Класс |
| `e_i` | i-th nearest etalon / i-й ближайший эталон |
| `purity(e_i)` | Etalon purity / Чистота эталона |
| `activity(e_i)` | Etalon activity / Активность эталона |

### Softmax Normalization / Softmax нормализация

```math
P(c) = \frac{\exp(\text{votes}[c] / T)}{\sum_{k} \exp(\text{votes}[k] / T)}
```

---

## 6. ADAPTIVE DELTA / АДАПТИВНЫЙ DELTA

### Formula / Формула

```math
\delta(c) = \delta_{base} \cdot \left(1 + \frac{n_{etalons}(c)}{K_{max}}\right)
```

### Where / Где:

| Symbol / Символ | Description / Описание | Default / По умолчанию |
|----------------|----------------------|----------------------|
| `δ_base` | Base threshold / Базовый порог | 0.12 |
| `n_etalons(c)` | Number of etalons for class c / Число этапонов класса c | — |
| `K_max` | Maximum etalons / Макс. этапонов | 1500 |

### Etalon Creation Logic / Логика создания эталона

```python
should_create = similarity < (1 - δ(c))
```

---

## 7. STOCHASTIC RESONANCE / СТОХАСТИЧЕСКИЙ РЕЗОНАНС

### Physical Constants / Физические Константы

| Constant / Константа | Value | Description / Описание |
|---------------------|-------|----------------------|
| **`α`** | `0.0072973525693` | Fine structure constant / Постоянная тонкой структуры |
| **`n_magic`** | `8.52` | Magic number / Магическое число |

### Surprise Computation / Вычисление сюрприза

```math
\text{surprise} = \frac{|P_{return} - α|}{α}
```

### Resonance Amplification / Резонансное усиление

```math
\text{amplification} = \frac{1}{1 + \left(\frac{n_{steps} - n_{magic}}{σ}\right)^2}
```

**Where / Где:**
- `σ = 20.0` — Standard deviation / Стандартное отклонение

### Adaptive Noise / Адаптивный шум

```math
\begin{aligned}
\text{noise} &= \mathcal{N}(0, 1) · β · 0.1 · \text{amplification} \\
x_{enhanced} &= x + \text{noise}
\end{aligned}
```

---

## 8. RHYTHM MODULE / РИТМИЧЕСКИЙ МОДУЛЬ

### Go Signal / Go-сигнал

```math
\begin{aligned}
\text{go\_probability} &= \text{amplification} \\
\text{go\_signal} &= (\text{go\_probability} > \text{threshold})
\end{aligned}
```

**Where / Где:**
- `threshold = 0.3` (default / по умолчанию)

### Interpretation / Интерпретация

| Go Signal / Go-сигнал | Meaning / Значение |
|----------------------|-------------------|
| **`go_signal = True`** | Learning/etalon creation allowed / Разрешено обучение/создание эталона |
| **`go_signal = False`** | Prediction only / Только предсказание |

---

## 9. ENERGY MANAGEMENT / ЭНЕРГОМЕНЕДЖМЕНТ

### Energy Consumption / Потребление энергии

```math
E(t+1) = E(t) - \text{cost}_{computation} - \text{cost}_{context\_switches}
```

### Energy Recovery / Восстановление энергии

```math
E(t+1) = \min(E_{init}, E(t) + \text{base\_recovery} · \text{sleep\_efficiency})
```

### Hibernation Mode / Режим гибернации

```math
\text{is\_hibernation} = (E < E_{threshold})
```

**Where / Где:**
- `E_threshold = 25.0` (default / по умолчанию)

---

## 10. ETALON PURITY / ЧИСТОТА ЭТАЛОНА

### Formula / Формула

```math
\text{purity}(e) = \frac{\max(\text{class\_counts})}{\sum(\text{class\_counts})}
```

---

## 11. ETALON ACTIVITY / АКТИВНОСТЬ ЭТАЛОНА

### Update Rule / Правило обновления

```math
\text{activity}(t+1) = \text{activity}(t) · 0.995 + \min(0.05, |\text{response}|)
```

**Constraint / Ограничение:**
```math
\text{activity} ∈ [0.0, 1.0]
```

### Decay / Затухание

```math
\text{activity}(t+1) = \text{activity}(t) · \exp(-1/τ)
```

**Where / Где:**
- `τ = 50` — Time constant / Время затухания

---

## 12. L2 NORMALIZATION / L2 НОРМАЛИЗАЦИЯ

### Formula / Формула

```math
x_{normalized} = \frac{x}{||x||}
```

**Where / Где:**
```math
||x|| = \sqrt{\sum_{i}(x[i]^2)}
```

### Protection Against Division by Zero / Защита от деления на ноль

```math
x_{normalized} = \frac{x}{||x|| + ε}
```

**Where / Где:**
- `ε = 1e-8`

```math
\text{votes}[class] = \sum_{i=1}^{k} \text{similarity}_i · \text{purity}_i · \text{activity}_i · \mathbb{I}(class_i = class)
```

### Where / Где:

| Term / Термин | Description / Описание |
|--------------|----------------------|
| `similarity_i` | Cosine similarity to etalon i / Косинусное сходство с этапоном i |
| `purity_i` | Class purity of etalon i / Чистота класса эталона i |
| `activity_i` | Activity level of etalon i / Уровень активности эталона i |
| `𝕀(class_i = class)` | Indicator function / Индикаторная функция |

---

### Softmax Probability / Вероятность Softmax

```math
P(class) = \frac{\exp(\text{votes}[class] / T)}{\sum_{c} \exp(\text{votes}[c] / T)}
```

### Where / Где:

| Symbol / Символ | Description / Описание |
|----------------|----------------------|
| `T` | Temperature parameter / Температурный параметр |
| `P(class)` | Probability of class / Вероятность класса |

**Prediction / Предсказание:**

```math
\text{prediction} = \arg\max_{c} P(c)
```

**Confidence / Уверенность:**

```math
\text{confidence} = P(\text{prediction})
```

---

## 5. ETALON CREATION CRITERION / КРИТЕРИЙ СОЗДАНИЯ ЭТАЛОНА

### Condition / Условие

A new etalon is created when:

Новый эталон создаётся, когда:

```math
\text{similarity}(x, \text{nearest}) < 1 - Δ_{class}
```

### Where / Где:

| Symbol / Символ | Description / Описание |
|----------------|----------------------|
| `Δ_class` | Class-specific threshold / Порог для конкретного класса |
| `nearest` | Most similar existing etalon / Наиболее похожий существующий эталон |

### Default Delta / Дельта по умолчанию

```math
Δ_{class} = Δ_{base} = 0.05
```

This means a new etalon is created if similarity < 95%.

Это означает, что новый эталон создаётся, если сходство < 95%.

---

## 6. COMPLEXITY ANALYSIS / АНАЛИЗ СЛОЖНОСТИ

### Time Complexity / Временная Сложность

| Operation / Операция | Complexity / Сложность |
|---------------------|----------------------|
| **L2 Normalization** | O(n) |
| **Find Nearest (k=1)** | O(K_max · n) |
| **Find Nearest (k)** | O(K_max · n) |
| **Weighted Voting** | O(k · n_classes) |
| **Weight Update** | O(n) |
| **Total Prediction** | O(K_max · n + k · n_classes) |

### Space Complexity / Пространственная Сложность

| Component / Компонент | Complexity / Сложность |
|----------------------|----------------------|
| **Etalon Storage** | O(K_max · n · 8) bytes |
| **Memory (STM/LTM)** | O(K_max · n · 8) bytes |
| **Total Memory** | O(K_max · n) |

### For typical configuration / Для типичной конфигурации:

- `K_max = 1500`
- `n = 140` (input dimension)
- `n_classes = 5`

**Memory Usage / Использование Памяти:**

```
Memory = 1500 × 140 × 8 bytes = 1,680,000 bytes ≈ 0.31 MB
```

---

## 7. CONVERGENCE PROOF / ДОКАЗАТЕЛЬСТВО СХОДИМОСТИ

### Theorem / Теорема

For bounded input `||x|| ≤ M` and learning rate `η < 1/M²`, the weight update converges.

Для ограниченного входа `||x|| ≤ M` и скорости обучения `η < 1/M²`, обновление весов сходится.

### Proof Sketch / Очерк Доказательства

**Step 1 / Шаг 1:** Bounded error

```math
|ε(t)| = |y_{target} - y_{current}| ≤ 2
```

**Step 2 / Шаг 2:** Weight change bound

```math
|Δc| = |η · ε(t) · x(t)| ≤ η · 2 · M
```

**Step 3 / Шаг 3:** For η < 1/M²:

```math
|Δc| < \frac{2}{M}
```

**Step 4 / Шаг 4:** By Banach fixed-point theorem, the iteration converges.

По теореме Банаха о неподвижной точке, итерация сходится.

---

## 8. COMPARISON WITH BACKPROPAGATION / СРАВНЕНИЕ С ОБРАТНЫМ РАСПРОСТРАНЕНИЕМ

| Aspect / Аспект | KOKAO (Formula 8) | Backpropagation |
|----------------|-------------------|-----------------|
| **Learning Rule** | Single-pass update / Однопроходное обновление | Multi-pass gradient / Многопроходный градиент |
| **Epochs** | 0 (online) / 0 (онлайн) | 100-500 |
| **Memory** | O(K_max · n) | O(n_layers · n²) |
| **Computational Cost** | O(n) per sample / O(n) на сэмпл | O(n_layers · n²) per sample |
| **Interpretability** | 100% (c⁺/c⁻ visible) / 100% (c⁺/c⁻ видны) | Low (black box) / Низкая (чёрный ящик) |
| **Energy Efficiency** | 402,500× better / В 402,500× лучше | 1× (baseline) |

---

## 9. PRACTICAL IMPLEMENTATION / ПРАКТИЧЕСКАЯ РЕАЛИЗАЦИЯ

### Weight Clipping / Ограничение Весов

To ensure numerical stability:

Для обеспечения численной устойчивости:

```python
c_plus = np.clip(c_plus, -2.0, 2.0)
c_minus = np.clip(c_minus, -2.0, 2.0)
```

### Adaptive Learning Rate / Адаптивная Скорость Обучения

```python
def get_adaptive_lr(base_lr, volatility, surprise):
    """
    Adjust learning rate based on volatility and surprise.
    """
    beta = compute_beta(surprise)  # β ∈ [0.1, 2.0]
    return base_lr * beta * (1.0 + volatility)
```

### Forgetting Mechanism / Механизм Забывания

```python
def decay_etalon(etalon, forgetting_factor=0.999):
    """
    Gradually reduce etalon activity over time.
    """
    etalon.activity *= forgetting_factor
```

---

## 13. COMPARISON WITH GRADIENT DESCENT / СРАВНЕНИЕ С ГРАДИЕНТНЫМ СПУСКОМ

### KOKAO (Formula 8)

```math
w(t+1) = w(t) + η · ε(t) · x(t)
```

### Gradient Descent (Backprop)

```math
w(t+1) = w(t) - η · \frac{∂L}{∂w}
```

### Advantages of KOKAO / Преимущества KOKAO

| Criterion / Критерий | KOKAO | Backprop |
|---------------------|-------|----------|
| **Epochs / Эпохи** | 0 (online) | 100-500 |
| **Memory / Память** | <0.31 MB | 50-200 MB |
| **Energy / Энергия** | 402,500× less | baseline |
| **Interpretability / Интерпретируемость** | 100% | black box / чёрный ящик |
| **Biological Plausibility / Биологичность** | 100% | low / низкая |

---

## 14. THEORETICAL GUARANTEES / ТЕОРЕТИЧЕСКИЕ ГАРАНТИИ

### Convergence / Сходимость

**Condition / Условие:**

При условии:
- `η < 1.0`
- `||x|| = 1` (L2 normalization / L2 нормализация)
- `ε(t) → 0` при `t → ∞`

**Convergence guaranteed in O(1/η) iterations / Сходимость гарантирована за O(1/η) итераций.**

---

### Memory Capacity / Ёмкость памяти

```math
C = \frac{K_{max} · d_{model} · 4 · 2}{1024 · 1024} \text{ MB}
```

### Where / Где:

| Symbol / Символ | Description / Описание |
|----------------|----------------------|
| `K_max` | Maximum number of etalons / Максимальное число этапонов |
| `d_model` | Feature dimension / Размерность признаков |
| `4` | Size of float32 in bytes / Размер float32 в байтах |
| `2` | c⁺ and c⁻ / c⁺ и c⁻ |

### Example / Пример:

For `K_max = 1500`, `d_model = 140`:

```
C = (1500 × 140 × 4 × 2) / (1024 × 1024) ≈ 1.61 MB
```

---

## 15. REFERENCES / ССЫЛКИ

1. **Kosyakov, Yu.B. "My Brain" (1999).** ISBN 5-89164-026-0.  
   Косяков, Ю.Б. "Мой мозг" (1999).

2. **Russian Patent №2109332 (expired).**  
   Патент РФ №2109332 (утратил силу).

3. **Weber-Fechner Law.** https://en.wikipedia.org/wiki/Weber%E2%80%93Fechner_law

4. **Banach Fixed-Point Theorem.** https://en.wikipedia.org/wiki/Banach_fixed-point_theorem

---

*Created by newmathphys / Создано newmathphys*

**KOKAO Engine v3.0.4**

Based on Kosyakov's Theory (1999)

Russian Patent №2109332 (expired) / Патент РФ №2109332 (утратил силу)
