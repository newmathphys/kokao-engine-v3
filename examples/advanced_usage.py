#!/usr/bin/env python3
"""
KOKAO Engine v3.0.4 — Advanced Usage Example
Пример расширенного использования

This example demonstrates:
- Custom configuration for UCR datasets
- Module integration (Stochastic, Rhythm, Energy)
- Online learning with real-time feedback
- Detailed statistics and monitoring
- Memory management

Этот пример демонстрирует:
- Пользовательскую конфигурацию для датасетов UCR
- Интеграцию модулей (Stochastic, Rhythm, Energy)
- Онлайн-обучение с обратной связью в реальном времени
- Подробную статистику и мониторинг
- Управление памятью
"""

import numpy as np
from kokao import KOKAOEngine
from kokao.core import Etalon, ContextMemory, KosyakovLearningEngine
from kokao.modules import StochasticResonance, RhythmModule, EnergyManager
from kokao.config import DEFAULT_CONFIG, UCR_CONFIGS


def generate_ucr_like_data(n_samples=1000, n_features=140, n_classes=2, noise_level=0.1):
    """
    Generate UCR-like time series data.
    
    Args:
        n_samples: Number of samples
        n_features: Number of features (time steps)
        n_classes: Number of classes
        noise_level: Noise standard deviation
    
    Returns:
        X: Data array, y: Labels array
    """
    np.random.seed(42)
    X = np.zeros((n_samples, n_features))
    y = np.zeros(n_samples, dtype=int)
    
    samples_per_class = n_samples // n_classes
    
    for class_idx in range(n_classes):
        start_idx = class_idx * samples_per_class
        end_idx = start_idx + samples_per_class
        
        # Generate class-specific temporal patterns
        t = np.linspace(0, 4 * np.pi, n_features)
        
        if class_idx == 0:
            # Class 0: Sine wave with specific frequency
            base_pattern = np.sin(t * (class_idx + 1))
        elif class_idx == 1:
            # Class 1: Cosine wave
            base_pattern = np.cos(t)
        elif class_idx == 2:
            # Class 2: Combined pattern
            base_pattern = np.sin(t) + 0.5 * np.sin(2 * t)
        else:
            # Other classes: Different frequencies
            base_pattern = np.sin(t * (class_idx * 0.5))
        
        noise = np.random.normal(0, noise_level, n_features)
        X[start_idx:end_idx] = base_pattern + noise
        y[start_idx:end_idx] = class_idx
    
    return X, y


def demonstrate_modules():
    """Demonstrate individual module functionality."""
    
    print("=" * 60)
    print("MODULE DEMONSTRATION / ДЕМОНСТРАЦИЯ МОДУЛЕЙ")
    print("=" * 60)
    print()
    
    # Stochastic Resonance / Стохастический резонанс
    print("1. Stochastic Resonance Module / Стохастический резонанс")
    print("-" * 40)
    stochastic = StochasticResonance(gain=0.1)
    
    test_signal = np.sin(np.linspace(0, 2 * np.pi, 100))
    surprise = stochastic.compute_surprise(P_return=0.3)
    beta = stochastic.compute_beta(surprise)
    enhanced = stochastic.add_adaptive_noise(test_signal, volatility=0.2)
    
    print(f"   Surprise: {surprise:.4f}")
    print(f"   Beta (β): {beta:.4f} ∈ [0.1, 2.0]")
    print(f"   Signal enhanced: {enhanced.shape}")
    print()
    
    # Rhythm Module / Ритмический модуль
    print("2. Rhythm Module / Ритмический модуль")
    print("-" * 40)
    rhythm = RhythmModule()
    
    go_signal, info = rhythm.compute_go_signal(volatility=0.15)
    print(f"   Go Signal: {go_signal}")
    print(f"   Info: {info}")
    print()
    
    # Energy Manager / Энергоменеджмент
    print("3. Energy Manager / Энергоменеджмент")
    print("-" * 40)
    energy = EnergyManager(budget=1.0)
    
    print(f"   Initial Energy: {energy.energy:.4f}")
    energy.consume(cost=0.01, switches=5)
    print(f"   After consume: {energy.energy:.4f}")
    energy.recover(base=0.005, efficiency=0.9)
    print(f"   After recover: {energy.energy:.4f}")
    print(f"   Hibernation: {energy.is_hibernation_mode()}")
    print()


def demonstrate_online_learning():
    """Demonstrate online learning with real-time feedback."""
    
    print("=" * 60)
    print("ONLINE LEARNING DEMONSTRATION / ОНЛАЙН ОБУЧЕНИЕ")
    print("=" * 60)
    print()
    
    # Generate data / Генерируем данные
    X, y = generate_ucr_like_data(n_samples=300, n_features=140, n_classes=3)
    
    # Create engine with custom config / Создаём движок с конфигурацией
    engine = KOKAOEngine(
        d_model=140,
        n_classes=3,
        K_max=500,
        delta_base=0.05,
        learning_rate=0.02,
        adaptive_learning=True
    )
    
    # Online learning / Онлайн обучение
    print("Online training (sample by sample)... / Онлайн тренировка (по сэмплу)...")
    correct = 0
    total = 0
    
    for i, (x_sample, y_true) in enumerate(zip(X, y)):
        # Predict before seeing label / Предсказываем до просмотра метки
        pred, conf = engine.predict(x_sample)
        
        # Check if correct / Проверяем правильность
        if pred == y_true:
            correct += 1
        total += 1
        
        # Train on this sample / Обучаем на этом сэмпле
        engine.process(x_sample, target=y_true)
        
        # Print progress every 50 samples / Печатаем прогресс каждые 50 сэмплов
        if (i + 1) % 50 == 0:
            accuracy = correct / total
            stats = engine.get_statistics()
            print(f"   Sample {i+1}/{len(X)}: Accuracy = {accuracy:.4f}, "
                  f"Etalons = {stats.get('n_etalons', 'N/A')}")
    
    print()
    print(f"   Final Online Accuracy: {correct/total:.4f}")
    print()


def demonstrate_memory_management():
    """Demonstrate memory management and etalon analysis."""
    
    print("=" * 60)
    print("MEMORY MANAGEMENT / УПРАВЛЕНИЕ ПАМЯТЬЮ")
    print("=" * 60)
    print()
    
    # Generate data / Генерируем данные
    X, y = generate_ucr_like_data(n_samples=200, n_features=140, n_classes=2)
    
    # Create engine / Создаём движок
    engine = KOKAOEngine(
        d_model=140,
        n_classes=2,
        K_max=300,
        delta_base=0.1  # Higher delta = more etalons
    )
    
    # Train / Обучаем
    engine.fit(X, y, verbose=False)
    
    # Analyze memory / Анализируем память
    stats = engine.get_statistics()
    print(f"   Total Etalons: {stats.get('n_etalons', 'N/A')}")
    print(f"   Max Etalons (K_max): {engine.K_max}")
    print(f"   Memory Usage: ~{stats.get('n_etalons', 0) * 140 * 8 / 1024:.2f} KB")
    print()
    
    # Analyze etalon distribution / Анализируем распределение этапонов
    print("   Etalon Distribution by Class:")
    if hasattr(engine.memory, 'etalons'):
        class_counts = {}
        for etalon in engine.memory.etalons:
            cls = etalon.class_label
            class_counts[cls] = class_counts.get(cls, 0) + 1
        
        for cls, count in sorted(class_counts.items()):
            print(f"      Class {cls}: {count} etalons")
    print()


def demonstrate_ucr_configuration():
    """Demonstrate UCR dataset-specific configurations."""
    
    print("=" * 60)
    print("UCR CONFIGURATIONS / КОНФИГУРАЦИИ UCR")
    print("=" * 60)
    print()
    
    print("Available UCR Configurations:")
    for dataset_name, config in UCR_CONFIGS.items():
        print(f"   {dataset_name}:")
        print(f"      d_model={config['d_model']}, "
              f"n_classes={config['n_classes']}, "
              f"K_max={config['K_max']}")
    print()
    
    # Create engine with ECG5000 config / Создаём движок с конфигурацией ECG5000
    ecg_config = UCR_CONFIGS["ECG5000"]
    print(f"Creating engine for ECG5000 dataset...")
    engine = KOKAOEngine(
        d_model=ecg_config['d_model'],
        n_classes=ecg_config['n_classes'],
        K_max=ecg_config['K_max']
    )
    print(f"   Created with d_model={engine.d_model}, "
          f"n_classes={engine.n_classes}, K_max={engine.K_max}")
    print()


def main():
    """Main advanced demonstration function."""
    
    print()
    print("🏆 KOKAO Engine v3.0.4 — Advanced Usage Example")
    print("🏆 KOKAO Engine v3.0.4 — Пример расширенного использования")
    print()
    
    # Module demonstration / Демонстрация модулей
    demonstrate_modules()
    
    # Online learning / Онлайн обучение
    demonstrate_online_learning()
    
    # Memory management / Управление памятью
    demonstrate_memory_management()
    
    # UCR configurations / Конфигурации UCR
    demonstrate_ucr_configuration()
    
    print("=" * 60)
    print("✅ Advanced example completed successfully!")
    print("✅ Расширенный пример завершён успешно!")
    print("=" * 60)
    print()
    print("📚 For more information, see:")
    print("   - docs/MATHEMATICAL_FOUNDATION.md")
    print("   - docs/ARCHITECTURE.md")
    print("   - docs/CODE_DOCUMENTATION.md")
    print()


if __name__ == "__main__":
    main()
