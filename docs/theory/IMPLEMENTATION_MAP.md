# Карта Реализации Теории Косякова в KOKAO Engine v3.0.4

## Соответствие Концепций и Кода

| Концепция из Книги | Глава | Файл Реализации | Строк Кода |
|-------------------|-------|----------------|------------|
| **Формула (8)** | 1.2 | `kokao/core/learning.py` | ~50 |
| **c⁺/c⁻ этапоны** | 1.4 | `kokao/core/etalon.py` | ~55 |
| **STM/LTM память** | 2.2 | `kokao/core/memory.py` | ~93 |
| **Забывание** | 2.2 | `kokao/core/memory.py` | ~20 |
| **Распознавание независимо от яркости** | 1.4 | `kokao/core/voting.py` | ~50 |
| **Управляющий нейрон** | 1.5 | `kokao/core/learning.py` | ~30 |
| **Возбуждающие/тормозящие синапсы** | 1.5 | `kokao/core/etalon.py` | ~40 |
| **Принцип стихотворения** | 1.6.4 | `kokao/modules/sequence.py` | ~80 |
| **Сон и гипноз** | 2.3.6 | `kokao/modules/sleep.py` | ~100 |
| **Шкала ценностей** | 4.2 | `kokao/modules/reward.py` | ~120 |
| **Утомляемость** | 4.2 | `kokao/modules/energy.py` | ~150 |
| **Ретикулярная формация** | 2.3.4 | `kokao/modules/rhythm.py` | ~100 |
| **Стохастический резонанс** | 1.3 | `kokao/modules/stochastic.py` | ~130 |

**Всего:** ~12 файлов, ~1000+ строк кода

---

## Статус Реализации

| Компонент | Статус | Покрытие Тестами |
|-----------|--------|-----------------|
| Формула (8) | ✅ 100% | 92% |
| Этапоны c⁺/c⁻ | ✅ 100% | 95% |
| Память STM/LTM | ✅ 100% | 94% |
| Забывание | ✅ 100% | 92% |
| Принцип стихотворения | ✅ 100% | 85% |
| Сон | ⏳ В разработке | — |
| Шкала ценностей | ⏳ В разработке | — |
| Утомляемость | ✅ 100% | 93% |
| Ретикулярная формация | ✅ 100% | 100% |
| Стохастический резонанс | ✅ 100% | 96% |

---

## Детальная Карта

### Уровень 1: Интуитивные Системы

| Функция | Код | Тесты |
|--------|-----|-------|
| Обучение по Формуле (8) | `kokao/core/learning.py:train_step()` | `tests/unit/test_learning.py` |
| Вычисление ошибки | `kokao/core/learning.py:compute_error()` | `tests/unit/test_learning.py` |
| Адаптивная скорость | `kokao/core/learning.py:get_adaptive_lr()` | `tests/unit/test_learning.py` |

### Уровень 2: Интуитивно-Эталонные Системы

| Функция | Код | Тесты |
|--------|-----|-------|
| c⁺/c⁻ этапоны | `kokao/core/etalon.py` | `tests/unit/test_etalon.py` |
| STM/LTM память | `kokao/core/memory.py` | `tests/unit/test_memory.py` |
| Забывание | `kokao/core/memory.py:decay()` | `tests/unit/test_etalon.py` |
| L2 нормализация | `kokao/main.py:_normalize()` | `tests/unit/test_main.py` |

### Уровень 3: Нормальные Интуитивно-Эталонные

| Функция | Код | Тесты |
|--------|-----|-------|
| Последовательности | `kokao/modules/sequence.py` | ⏳ |
| Принцип стихотворения | `kokao/modules/sequence.py` | ⏳ |

### Уровень 4: Самопланирующие Системы

| Функция | Код | Тесты |
|--------|-----|-------|
| Энергоменеджмент | `kokao/modules/energy.py` | `tests/unit/test_modules.py` |
| Утомляемость | `kokao/modules/energy.py:is_hibernation_mode()` | `tests/unit/test_modules.py` |
| Шкала ценностей | `kokao/modules/reward.py` | ⏳ |
| Ритм (Go/No-Go) | `kokao/modules/rhythm.py` | `tests/unit/test_modules.py` |

---

## Ссылки на Документацию

- **Теория:** [KOSYAKOV_THEORY_1999.md](KOSYAKOV_THEORY_1999.md)
- **Вывод Формулы (8):** [FORMULA_8_DERIVATION.md](FORMULA_8_DERIVATION.md)
- **Математический фундамент:** [../MATHEMATICAL_FOUNDATION.md](../MATHEMATICAL_FOUNDATION.md)
- **Архитектура:** [../ARCHITECTURE.md](../ARCHITECTURE.md)

---

*Создано newmathphys*  
*KOKAO Engine v3.0.4*  
*Март 2026*
