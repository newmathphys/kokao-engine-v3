# 📊 Data Availability Statement / Заявление о Доступности Данных

**KOKAO Engine v3.0.4 — Benchmark Study**

**Date:** March 17, 2026  
**Version:** 3.0.4  
**Organization:** newmathphys

---

## Data Availability / Доступность Данных

All 9 UCR datasets used in this study are publicly available from the **UCR Time Series Classification Archive** [1].

Все 9 датасетов UCR, использованных в этом исследовании, общедоступны из **Архива Классификации Временных Рядов UCR** [1].

### Archive Information / Информация об Архиве

- **Name:** UCR Time Series Classification Archive
- **URL:** https://cs.ucr.edu/~eamonn/time_series_data/
- **Format:** TSV (Tab-Separated Values)
- **License:** Public Domain / Open Data

---

## Dataset Details / Детали Датасетов

### File Sizes and SHA-256 Checksums / Размеры Файлов и Контрольные Суммы SHA-256

| Dataset | Train Size | Test Size | SHA-256 (first 16 chars) | Classes |
|---------|-----------|-----------|------------------------|---------|
| **ECG5000** | 767 KB | 6.8 MB | `4dfd3b0b593e713e...` | 2 |
| **Wafer** | 1.4 MB | 855 KB | `23b8db9b250acb58...` | 2 |
| **Coffee** | 89 KB | 89 KB | `9a659adf934776be...` | 2 |
| **FordA** | 20 MB | 7.2 MB | `e27f49301970f6f0...` | 2 |
| **GunPoint** | 83 KB | 247 KB | `dc15c3da288d3762...` | 2 |
| **Beef** | 157 KB | 157 KB | `10f84125535a3659...` | 5 |
| **SwedishLeaf** | 1.6 MB | 20 MB | `077458372facdc78...` | 15 |
| **FaceAll** | 803 KB | 2.4 MB | `2b296f0dea9568fc...` | 14 |
| **FiftyWords** | 1.4 MB | 1.4 MB | `83ce84fce9ab199f...` | 50 |

**Total / Итого:** 46 MB, 18 files / файлов

---

## Data Format / Формат Данных

### TSV Structure / Структура TSV

```
<class_label>    <feature_1>    <feature_2>    ...    <feature_n>
```

**Example / Пример (ECG5000):**
```
0    3.1490142    2.9585207    3.1943066    ...    -0.3692593
1    0.06823798   0.39214283   -0.482245    ...    -0.27281624
2    0.034055203  0.1986392    0.47580504   ...    0.13863105
```

**Columns / Колонки:**
1. **Class label** (integer, 1-indexed in original, converted to 0-indexed)
2. **Features** (float64, L2-normalized during preprocessing)

---

## Data Verification / Проверка Данных

### SHA-256 Checksum Verification / Проверка Контрольных Сумм SHA-256

```bash
# Verify all files / Проверить все файлы
cd data/real_ucr/
sha256sum *.tsv > checksums.sha256

# Verify against known hashes / Проверить против известных хешей
sha256sum -c checksums.sha256
```

### Expected Checksums / Ожидаемые Контрольные Суммы

| File | SHA-256 (full) |
|------|----------------|
| `ECG5000_TRAIN.tsv` | `4dfd3b0b593e713eb671c67de619d40b3c5b070430405f217c6747140e0b8020` |
| `ECG5000_TEST.tsv` | `25ab48432cb3f234a4e4bdd6fe66b4ac0c6c92b69b5d76c2737ee31fb387ad73` |
| `Wafer_TRAIN.tsv` | `23b8db9b250acb5808f4568f50fc37ff0d948ab41f52e814bbdfd128e32b0705` |
| `Wafer_TEST.tsv` | `7d44c5784d74743e3d1ddccfac626c0c5019daf3e28a26ed85b469f4b9e98765` |
| `Coffee_TRAIN.tsv` | `9a659adf934776be784ed585cee34d9b85813df31c69bd78cda7323c284831ec` |
| `Coffee_TEST.tsv` | `05ce3635499931a5af0021b0f60e926bb1e1aeecbfda2850160bdba63cdf14ce` |
| `FordA_TRAIN.tsv` | `e27f49301970f6f09ab3409a44dd0869989e985c6d7d7b783f45297f47e85a69` |
| `FordA_TEST.tsv` | `f8f28a00d73d2d084dc9def348b5234d182b4884546a706cd8204251555c31de` |
| `GunPoint_TRAIN.tsv` | `dc15c3da288d3762712bc2c395558e70cf55962a60e43566807e0905e331ece5` |
| `GunPoint_TEST.tsv` | `caeb63458dfa0f808115b5ce0d7fba670af2ac73a29fd23a4d3d8559df3ffb6f` |
| `Beef_TRAIN.tsv` | `10f84125535a3659a99bd3565cda6d7fa6bd3dfd9b0131b8af501ced82aa3df6` |
| `Beef_TEST.tsv` | `fac75662c7fe596d8ccf7f6b73099954cb52cf149bf04d79737993178022b461` |
| `SwedishLeaf_TRAIN.tsv` | `077458372facdc78d46780d7c463886a6ec7bef32a5b8bda7668a6cba7f93150` |
| `SwedishLeaf_TEST.tsv` | `09a63f23c9a96597ca7e80cf7470355ede3050ad13f49ed4219d2d4882908923` |
| `FaceAll_TRAIN.tsv` | `2b296f0dea9568fcb781058dab49401796650ae376b5b4279038a4ef97bdd815` |
| `FaceAll_TEST.tsv` | `e07542eb606ab0758adf038eeb08ba4e18b9a5779718d00bbc3f8101d42d0aaf` |
| `FiftyWords_TRAIN.tsv` | `83ce84fce9ab199ffbb73dcffde40706cb2ae23d8794fe93d05a521d0fddd83b` |
| `FiftyWords_TEST.tsv` | `aa628755c501431d92af6156f8bd17646bacc996e3d1ad86d9d4fbe2b75f3797` |

---

## Preprocessing / Предобработка

### Applied Transformations / Применённые Преобразования

1. **Label Conversion:** 1-indexed → 0-indexed
   ```python
   y = y.astype(int) - 1  # if y.min() >= 1
   ```

2. **L2 Normalization:** Applied to all input vectors
   ```python
   x_normalized = x / (||x|| + 1e-8)
   ```

3. **No Additional Preprocessing:** No filtering, smoothing, or feature engineering applied.

---

## Configuration for Reproducibility / Конфигурация для Воспроизводимости

### Engine Configuration / Конфигурация Движка

```python
from kokao.main import KOKAOEngine

engine = KOKAOEngine(
    d_model=d_model,          # Dataset-specific (127-500)
    n_classes=n_classes,      # Dataset-specific (2-50)
    K_max=min(3000, n_train * 2),
    delta_base=0.08,
    learning_rate=0.02,
    adaptive_learning=True,
    stochastic_gain=0.1,
    rhythm_enabled=True,
    energy_efficient=False
)
```

### Training Configuration / Конфигурация Обучения

```python
# Fit on training data
engine.fit(X_train, y_train, verbose=False)

# Evaluate on test data
accuracy = engine.evaluate(X_test, y_test)
```

---

## Access Instructions / Инструкции по Доступу

### 1. Download UCR Datasets / Скачать Датасеты UCR

```bash
# Visit UCR Archive / Посетить Архив UCR
https://cs.ucr.edu/~eamonn/time_series_data/

# Or use direct download script
wget https://www.cs.ucr.edu/~eamonn/universe_archive.zip
```

### 2. Extract Data / Извлечь Данные

```bash
# Create data directory
mkdir -p data/real_ucr/

# Copy TSV files
cp /path/to/universe_archive/*.tsv data/real_ucr/
```

### 3. Verify Data / Проверить Данные

```bash
# Run verification script
python scripts/verify_data.py
```

---

## Citation / Цитирование

### For UCR Archive / Для Архива UCR

```bibtex
@article{ucr_archive,
  title={The UCR Time Series Classification Archive},
  author={Dau, Hoang Anh and Keogh, Eamonn and Kamgar, Kaveh and Yeh, Chin-Chia Michael and Zhu, Yan and Gharghabi, Shaghayegh and Ratanamahatana, Chotirat Ann and others},
  journal={IEEE/CAA Journal of Automatica Sinica},
  year={2019},
  publisher={IEEE}
}
```

### For KOKAO Engine / Для KOKAO Engine

```bibtex
@software{kokao_engine_v3,
  title={KOKAO Engine: Biologically Plausible Cognitive Architecture},
  author={Kalinouski, Vital and Ovseychik, V.},
  orcid={0009-0003-1963-2665, 0009-0000-6652-2301},
  version={3.0.4},
  year={2026},
  url={https://github.com/newmathphys/kokao-engine},
  note={Based on Kosyakov's Theory of Functionally-Independent Structures (1999). Russian Patent №2109332 (expired).}
}
```

---

## Statement for Publication / Заявление для Публикации

### English Version

> **Data Availability Statement**
>
> Results validated on 9 real UCR time series datasets (total 46 MB, 18 files). All data files verified with SHA-256 checksums. Configuration documented for reproducibility.
>
> All datasets are publicly available from the UCR Time Series Classification Archive [1]. No custom or proprietary data was used in this study.

### Russian Version

> **Заявление о Доступности Данных**
>
> Результаты валидированы на 9 реальных датасетах временных рядов UCR (общий размер 46 MB, 18 файлов). Все файлы проверены контрольными суммами SHA-256. Конфигурация задокументирована для воспроизводимости.
>
> Все датасеты общедоступны из Архива Классификации Временных Рядов UCR [1]. В этом исследовании не использовались пользовательские или проприетарные данные.

---

## References / Ссылки

1. **UCR Time Series Classification Archive**
   - URL: https://cs.ucr.edu/~eamonn/time_series_data/
   - Accessed: March 2026

2. **KOKAO Engine v3.0.4 Documentation**
   - URL: https://github.com/newmathphys/kokao-engine
   - Version: 3.0.4

3. **Kosyakov's Theory of Functionally-Independent Structures**
   - Kosyakov, Yu.B. "My Brain" (1999)
   - ISBN: 5-89164-026-0

---

## Contact / Контакты

**For data access questions / По вопросам доступа к данным:**

- **Email:** newmathphys@gmail.com
- **GitHub:** https://github.com/newmathphys/kokao-engine
- **Issues:** https://github.com/newmathphys/kokao-engine/issues

---

*Created by newmathphys / Создано newmathphys*

**KOKAO Engine v3.0.4**

Based on Kosyakov's Theory (1999)

Russian Patent №2109332 (expired) / Патент РФ №2109332 (утратил силу)

March 2026 / Март 2026
