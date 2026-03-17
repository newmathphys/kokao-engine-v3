#!/usr/bin/env python3
"""
KOKAO Engine v3.0.4 — Basic Usage Example
Пример базового использования

This example demonstrates:
- Creating a KOKAOEngine model
- Training on synthetic data (online, 0 epochs)
- Making predictions with confidence scores
- Evaluating accuracy

Этот пример демонстрирует:
- Создание модели KOKAOEngine
- Обучение на синтетических данных (онлайн, 0 эпох)
- Предсказания с оценками уверенности
- Оценку точности
"""

import numpy as np
from kokao import KOKAOEngine


def generate_synthetic_data(n_samples=1000, n_features=140, n_classes=5):
    """
    Generate synthetic time series data for demonstration.
    
    Args:
        n_samples: Number of samples / Количество сэмплов
        n_features: Number of features / Количество признаков
        n_classes: Number of classes / Количество классов
    
    Returns:
        X: Data array of shape (n_samples, n_features)
        y: Labels array of shape (n_samples,)
    """
    np.random.seed(42)
    X = np.zeros((n_samples, n_features))
    y = np.zeros(n_samples, dtype=int)
    
    samples_per_class = n_samples // n_classes
    
    for class_idx in range(n_classes):
        start_idx = class_idx * samples_per_class
        end_idx = start_idx + samples_per_class
        
        # Generate class-specific patterns / Генерируем паттерны для класса
        base_pattern = np.sin(np.linspace(0, 2 * np.pi * (class_idx + 1), n_features))
        noise = np.random.normal(0, 0.1, n_features)
        
        X[start_idx:end_idx] = base_pattern + noise
        y[start_idx:end_idx] = class_idx
    
    return X, y


def main():
    """Main demonstration function / Основная демонстрационная функция."""
    
    print("=" * 60)
    print("KOKAO Engine v3.0.4 — Basic Usage Example")
    print("Пример базового использования")
    print("=" * 60)
    print()
    
    # Generate synthetic data / Генерируем синтетические данные
    print("📊 Generating synthetic data... / Генерация синтетических данных...")
    X, y = generate_synthetic_data(n_samples=500, n_features=140, n_classes=5)
    print(f"   Data shape: {X.shape}")
    print(f"   Labels: {np.unique(y)}")
    print()
    
    # Split into train/test / Разделяем на train/test
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    print(f"   Train samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")
    print()
    
    # Create KOKAO Engine / Создаём движок KOKAO
    print("🧠 Creating KOKAO Engine... / Создание движка KOKAO...")
    engine = KOKAOEngine(
        d_model=140,
        n_classes=5,
        K_max=1500,
        delta_base=0.05,
        learning_rate=0.02,
        adaptive_learning=True,
        stochastic_gain=0.1,
        rhythm_enabled=True,
        energy_efficient=True
    )
    print(f"   Version: {engine.__class__.__module__}")
    print()
    
    # Train (online, 0 epochs) / Обучение (онлайн, 0 эпох)
    print("📚 Training (online, 0 epochs)... / Обучение (онлайн, 0 эпох)...")
    engine.fit(X_train, y_train, verbose=True)
    print()
    
    # Get statistics / Получаем статистику
    stats = engine.get_statistics()
    print(f"   Etalons created: {stats.get('n_etalons', 'N/A')}")
    print(f"   Energy remaining: {stats.get('energy', 'N/A'):.4f}" if 'energy' in stats else "")
    print()
    
    # Predict single sample / Предсказание одного сэмпла
    print("🔮 Predicting single sample... / Предсказание одного сэмпла...")
    sample_idx = 0
    x_sample = X_test[sample_idx]
    y_true = y_test[sample_idx]
    
    pred, conf = engine.predict(x_sample)
    print(f"   True label: {y_true}")
    print(f"   Prediction: {pred}")
    print(f"   Confidence: {conf:.4f}")
    print()
    
    # Evaluate on test set / Оценка на тестовой выборке
    print("📈 Evaluating on test set... / Оценка на тестовой выборке...")
    accuracy = engine.evaluate(X_test, y_test)
    print(f"   Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print()
    
    # Batch prediction / Пакетное предсказание
    print("📦 Batch prediction... / Пакетное предсказание...")
    predictions, confidences = engine.predict_batch(X_test)
    print(f"   Predictions shape: {predictions.shape}")
    print(f"   Mean confidence: {confidences.mean():.4f}")
    print()
    
    print("=" * 60)
    print("✅ Example completed successfully!")
    print("✅ Пример завершён успешно!")
    print("=" * 60)
    
    return accuracy


if __name__ == "__main__":
    main()
