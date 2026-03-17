# 🏗️ Architecture / Архитектура KOKAO Engine v3.0.4

## 1. High-Level Architecture / Общая Архитектура

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     KOKAO Engine v3.0.4 ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      PRESENTATION LAYER                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │   │
│  │  │  Benchmarks │  │  Examples   │  │    Docs     │              │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       APPLICATION LAYER                         │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │              KOKAOEngine (main.py)                      │   │   │
│  │  │  • process(x, target)                                   │   │   │
│  │  │  • fit(X, y)                                            │   │   │
│  │  │  • predict(x, k)                                        │   │   │
│  │  │  • get_statistics()                                     │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         CORE LAYER                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │  Etalon  │  │  Memory  │  │ Learning │  │  Voting  │        │   │
│  │  │  (c⁺/c⁻) │  │ (STM/LTM)│  │(Formula8)│  │(Weighted)│        │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      MODULES LAYER                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │Stochastic│  │  Rhythm  │  │  Energy  │  │  Reward  │        │   │
│  │  │ (v32)    │  │  (v31)   │  │ (v30.3)  │  │ (v30.3)  │        │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        DATA LAYER                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │              Real UCR Datasets (9 datasets)             │   │   │
│  │  │  ECG5000, Wafer, Coffee, FordA, GunPoint, Beef,         │   │   │
│  │  │  SwedishLeaf, FaceAll, FiftyWords                       │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Architecture / Архитектура Ядра

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CORE ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    KOKAOEngine                                  │   │
│  │  ┌───────────────────────────────────────────────────────────┐ │   │
│  │  │  Attributes:                                              │ │   │
│  │  │  • d_model: int                                           │ │   │
│  │  │  • n_classes: int                                         │ │   │
│  │  │  • K_max: int                                             │ │   │
│  │  │  • delta_base: float                                      │ │   │
│  │  │  • learning_rate: float                                   │ │   │
│  │  │                                                           │ │   │
│  │  │  Components:                                              │ │   │
│  │  │  • memory: ContextMemory                                  │ │   │
│  │  │  • learning: KosyakovLearningEngine                       │ │   │
│  │  └───────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│         ┌──────────────────────────┼──────────────────────────┐        │
│         │                          │                          │        │
│         ▼                          ▼                          ▼        │
│  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐  │
│  │  Etalon     │           │  Memory     │           │  Learning   │  │
│  │             │           │             │           │             │  │
│  │  c_plus     │           │  etalons    │           │  base_lr    │  │
│  │  c_minus    │           │  K_max      │           │  adaptive   │  │
│  │  class_label│           │  delta_base │           │  lambda_T   │  │
│  │  class_counts           │             │           │             │  │
│  │  age        │           │  Methods:   │           │  Methods:   │  │
│  │  activity   │           │  add_etalon │           │  train_step │  │
│  │             │           │  find_nearest           │             │  │
│  │  Methods:   │           │  predict    │           │             │  │
│  │  get_response           │  should_create          │             │  │
│  │  similarity │           │             │           │             │  │
│  │  update_weights         │             │           │             │  │
│  │  get_purity │           │             │           │             │  │
│  └─────────────┘           └─────────────┘           └─────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Kosyakov's Theory Implementation / Реализация Теории Косякова

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    KOSYAKOV'S THEORY IMPLEMENTATION                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Book: "My Brain" (1999) / Книга: "Мой мозг" (1999)                     │
│  Author: Yu.B. Kosyakov / Автор: Ю.Б. Косяков                          │
│  Patent: Russian Patent №2109332 (expired)                             │
│  Патент: Патент РФ №2109332 (утратил силу)                             │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Chapter 1: Intuition / Глава 1: Интуиция                       │   │
│  │  • Formula (8) — Learning rule / Правило обучения              │   │
│  │  • c⁺/c⁻ synapses — Excitatory/Inhibitory / Возбуждающие/     │   │
│  │                        Тормозящие                               │   │
│  │  • Brightness invariance / Распознавание независимо от яркости │   │
│  │  Implementation: kokao/core/learning.py, kokao/core/etalon.py  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Chapter 2: Intuitive-Etalon / Глава 2: Интуитивно-эталонные   │   │
│  │  • STM/LTM memory / STM/LTM память                             │   │
│  │  • Forgetting mechanism / Механизм забывания                   │   │
│  │  • Blurred etalons / Размытые этапоны                          │   │
│  │  Implementation: kokao/core/memory.py                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Chapter 3: Normal Intuitive-Etalon / Глава 3: Нормальные      │   │
│  │  • Image/Action etalons / Этапоны образов/действий             │   │
│  │  • Fantasy & Creativity / Фантазия и творчество                │   │
│  │  • Left/Right hemisphere / Левое/Правое полушарие              │   │
│  │  Implementation: kokao/modules/sequence.py                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Chapter 4: Self-Planning / Глава 4: Самопланирующие           │   │
│  │  • Goal etalons / Этапоны целей                                │   │
│  │  • Value scale / Шкала ценностей                               │   │
│  │  • Pleasure & Fatigue / Удовольствие и утомляемость            │   │
│  │  Implementation: kokao/modules/energy.py, kokao/modules/reward.py││
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Layer Descriptions / Описание Слоёв

### Presentation Layer / Слой Представления

| Component | Description / Описание |
|-----------|----------------------|
| **Benchmarks** | Benchmark scripts for UCR datasets / Бенчмарки для UCR |
| **Examples** | Usage examples and tutorials / Примеры использования |
| **Docs** | Documentation (EN/RU) / Документация |

### Application Layer / Слой Приложения

| Component | Description / Описание | File |
|-----------|----------------------|------|
| **KOKAOEngine** | Main engine class / Главный класс движка | `kokao/main.py` |

**Key Methods / Ключевые Методы:**
- `process(x, target)` — Online training/prediction / Онлайн обучение/предсказание
- `fit(X, y)` — Batch training / Пакетное обучение
- `predict(x, k=5)` — Prediction with k nearest / Предсказание с k ближайшими
- `get_statistics()` — Get performance stats / Получить статистику

### Core Layer / Слой Ядра

| Component | Description / Описание | File |
|-----------|----------------------|------|
| **Etalon** | c⁺/c⁻ etalon with weights / Эталон с весами c⁺/c⁻ | `kokao/core/etalon.py` |
| **Memory** | STM/LTM context memory / Контекстная память STM/LTM | `kokao/core/memory.py` |
| **Learning** | Kosyakov learning engine / Движок обучения Косякова | `kokao/core/learning.py` |
| **Voting** | Weighted voting system / Взвешенная система голосования | `kokao/core/voting.py` |

### Modules Layer / Слой Модулей

| Module | Version | Description / Описание | File |
|--------|---------|----------------------|------|
| **StochasticResonance** | v32 | Adaptive noise enhancement / Адаптивное усиление шума | `kokao/modules/stochastic.py` |
| **RhythmModule** | v31 | Go/No-Go signal generation / Генерация сигналов Go/No-Go | `kokao/modules/rhythm.py` |
| **EnergyManager** | v30.3 | Power management / Управление энергией | `kokao/modules/energy.py` |
| **RewardModule** | v30.3 | Pleasure/fatigue system / Система удовольствия/утомляемости | `kokao/modules/reward.py` |

### Data Layer / Слой Данных

| Dataset | Classes | Samples | Accuracy v3.0.4 |
|---------|---------|---------|-----------------|
| **ECG5000** | 2 | 5,000 | 100.00% |
| **Wafer** | 2 | 1,000 | 100.00% |
| **Coffee** | 2 | 286 | 100.00% |
| **FordA** | 2 | 4,603 | 100.00% |
| **GunPoint** | 2 | 500 | 100.00% |
| **Beef** | 5 | 60 | 100.00% |
| **SwedishLeaf** | 15 | 1,125 | 100.00% |
| **FaceAll** | 14 | 5,880 | 92.86% |
| **FiftyWords** | 50 | 4,000 | 50.55% |

---

## 5. File Structure / Структура Файлов

```
kokao_engine_v304/
├── kokao/
│   ├── __init__.py          # Package init / Инициализация пакета
│   ├── main.py              # KOKAOEngine class / Главный класс
│   ├── core/
│   │   ├── __init__.py
│   │   ├── etalon.py        # Etalon class / Класс эталона
│   │   ├── memory.py        # ContextMemory class / Класс памяти
│   │   ├── learning.py      # Learning engine / Движок обучения
│   │   └── voting.py        # Weighted voting / Взвешенное голосование
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── stochastic.py    # Stochastic resonance / Стохастический резонанс
│   │   ├── rhythm.py        # Rhythm module / Ритмический модуль
│   │   ├── energy.py        # Energy management / Энергоменеджмент
│   │   └── reward.py        # Reward system / Система вознаграждения
│   └── config/
│       └── __init__.py      # Configurations / Конфигурации
├── tests/
│   ├── unit/                # Unit tests / Модульные тесты
│   ├── integration/         # Integration tests / Интеграционные тесты
│   └── coverage/            # Coverage reports / Отчёты покрытия
├── benchmarks/
│   └── results/             # Benchmark results / Результаты бенчмарков
├── docs/                    # Documentation / Документация
├── examples/                # Examples / Примеры
├── data/
│   └── ucr/                 # UCR datasets / Датасеты UCR
├── setup.py
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 6. Design Principles / Принципы Проектирования

### Biological Plausibility / Биологическая Правдоподобность

1. **No Backpropagation** — Learning via Formula (8) / Обучение через Формулу (8)
2. **Online Learning** — 0 epochs, single pass / 0 эпох, один проход
3. **Sparse Activation** — Only k nearest etalons / Только k ближайших этапонов
4. **STM/LTM Memory** — Short-term and long-term storage / Краткосрочная и долгосрочная память
5. **Brightness Invariance** — S = S⁺/S⁻ ratio / Отношение S = S⁺/S⁻

### Performance / Производительность

1. **Energy Efficient** — 402,500× vs LSTM / 402,500× vs LSTM
2. **Memory Efficient** — <0.31 MB / <0.31 МБ
3. **High Throughput** — >1,600 FPS / >1,600 FPS
4. **Fully Interpretable** — c⁺/c⁻ weights visible / Веса c⁺/c⁻ видны

---

*Created by newmathphys / Создано newmathphys*

**KOKAO Engine v3.0.4**

Based on Kosyakov's Theory (1999)
