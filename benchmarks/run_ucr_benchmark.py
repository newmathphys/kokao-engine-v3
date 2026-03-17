#!/usr/bin/env python3
"""
KOKAO Engine v3.0.4 — Benchmark Script for UCR Datasets

Бенчмарк на 8 реальных UCR датасетах:
- Beef
- Coffee
- ECG5000
- FaceAll
- FiftyWords
- FordA
- GunPoint
- SwedishLeaf
- Wafer
"""

import os
import sys
import time
import numpy as np
from pathlib import Path

# Add kokao_engine_v304 to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from kokao.main import KOKAOEngine


# UCR Dataset configurations
UCR_DATASETS = [
    {"name": "Beef", "n_classes": 5},
    {"name": "Coffee", "n_classes": 2},
    {"name": "ECG5000", "n_classes": 2},
    {"name": "FaceAll", "n_classes": 14},
    {"name": "FiftyWords", "n_classes": 50},
    {"name": "FordA", "n_classes": 2},
    {"name": "GunPoint", "n_classes": 2},
    {"name": "SwedishLeaf", "n_classes": 15},
    {"name": "Wafer", "n_classes": 2},
]


def load_ucr_dataset(data_dir: str, dataset_name: str):
    """
    Load UCR dataset from TSV files.
    
    Args:
        data_dir: Directory with data files
        dataset_name: Name of dataset (e.g., "Beef")
    
    Returns:
        X_train, y_train, X_test, y_test
    """
    train_path = Path(data_dir) / f"{dataset_name}_TRAIN.tsv"
    test_path = Path(data_dir) / f"{dataset_name}_TEST.tsv"
    
    if not train_path.exists() or not test_path.exists():
        print(f"  ⚠️ Dataset {dataset_name} not found!")
        return None, None, None, None
    
    # Load TSV files
    train_data = np.loadtxt(train_path, delimiter='\t')
    test_data = np.loadtxt(test_path, delimiter='\t')
    
    # Split labels and features
    y_train = train_data[:, 0]
    X_train = train_data[:, 1:]
    
    y_test = test_data[:, 0]
    X_test = test_data[:, 1:]
    
    # Convert to 0-indexed if needed
    if y_train.min() >= 1:
        y_train = y_train.astype(int) - 1
        y_test = y_test.astype(int) - 1
    else:
        y_train = y_train.astype(int)
        y_test = y_test.astype(int)
    
    return X_train, y_train, X_test, y_test


def run_benchmark(dataset_name: str, n_classes: int, data_dir: str):
    """
    Run benchmark on single dataset.
    
    Args:
        dataset_name: Name of dataset
        n_classes: Number of classes
        data_dir: Directory with data files
    
    Returns:
        Dictionary with results
    """
    print(f"\n{'='*60}")
    print(f"📊 Dataset: {dataset_name} ({n_classes} classes)")
    print(f"{'='*60}")
    
    # Load data
    X_train, y_train, X_test, y_test = load_ucr_dataset(data_dir, dataset_name)
    
    if X_train is None:
        return {
            "name": dataset_name,
            "status": "NOT_FOUND",
            "accuracy": 0.0,
            "train_time": 0.0,
            "predict_time": 0.0,
            "n_etalons": 0
        }
    
    n_train = len(X_train)
    n_test = len(X_test)
    d_model = X_train.shape[1]
    
    print(f"  Train samples: {n_train}")
    print(f"  Test samples: {n_test}")
    print(f"  Features: {d_model}")
    
    # Create engine with dataset-specific config
    K_max = min(3000, n_train * 2)  # Allow more etalons
    delta_base = 0.08  # More lenient creation threshold
    
    engine = KOKAOEngine(
        d_model=d_model,
        n_classes=n_classes,
        K_max=K_max,
        delta_base=delta_base,
        learning_rate=0.02,
        adaptive_learning=True,
        stochastic_gain=0.1,
        rhythm_enabled=True,
        energy_efficient=False  # Disable for better performance
    )
    
    # Train
    print(f"  📚 Training...")
    start_time = time.time()
    engine.fit(X_train, y_train, verbose=False)
    train_time = time.time() - start_time
    
    stats = engine.get_statistics()
    n_etalons = stats['n_etalons']
    print(f"  ✅ Etalons created: {n_etalons}")
    print(f"  ⏱️ Train time: {train_time:.2f}s")
    
    # Predict
    print(f"  🔮 Predicting...")
    start_time = time.time()
    predictions, confidences = engine.predict_batch(X_test)
    predict_time = time.time() - start_time
    
    print(f"  ⏱️ Predict time: {predict_time:.2f}s ({n_test/predict_time:.1f} samples/sec)")
    
    # Evaluate
    accuracy = np.mean(predictions == y_test)
    print(f"  📈 Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Mean confidence
    mean_conf = np.mean(confidences)
    print(f"  💯 Mean confidence: {mean_conf:.4f}")
    
    return {
        "name": dataset_name,
        "status": "OK",
        "accuracy": accuracy,
        "train_time": train_time,
        "predict_time": predict_time,
        "throughput": n_test / predict_time,
        "n_etalons": n_etalons,
        "n_train": n_train,
        "n_test": n_test,
        "d_model": d_model,
        "mean_confidence": mean_conf
    }


def main():
    """Main benchmark function."""
    print()
    print("🏆" * 30)
    print("🏆 KOKAO Engine v3.0.4 — UCR Benchmark")
    print("🏆 Based on Kosyakov's Theory (1999)")
    print("🏆" * 30)
    print()
    
    # Data directory - use parent project's data
    data_dir = Path(__file__).parent.parent.parent / "data" / "real_ucr"
    
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        sys.exit(1)
    
    print(f"📁 Data directory: {data_dir}")
    print(f"📊 Datasets: {len(UCR_DATASETS)}")
    
    # Run benchmarks
    results = []
    
    for dataset in UCR_DATASETS:
        result = run_benchmark(
            dataset["name"],
            dataset["n_classes"],
            str(data_dir)
        )
        results.append(result)
    
    # Summary
    print()
    print("=" * 80)
    print("📊 BENCHMARK SUMMARY / СВОДКА БЕНЧМАРКОВ")
    print("=" * 80)
    print()
    
    # Table header
    print(f"{'Dataset':<15} {'Accuracy':<12} {'Train (s)':<12} {'Pred (s)':<12} {'Throughput':<15} {'Etalons':<10}")
    print("-" * 80)
    
    total_accuracy = 0.0
    n_ok = 0
    
    for result in results:
        if result["status"] == "OK":
            print(f"{result['name']:<15} "
                  f"{result['accuracy']:.4f} ({result['accuracy']*100:.1f}%)  "
                  f"{result['train_time']:<12.2f} "
                  f"{result['predict_time']:<12.2f} "
                  f"{result['throughput']:<15.1f} "
                  f"{result['n_etalons']:<10}")
            total_accuracy += result['accuracy']
            n_ok += 1
        else:
            print(f"{result['name']:<15} NOT FOUND")
    
    print("-" * 80)
    
    if n_ok > 0:
        avg_accuracy = total_accuracy / n_ok
        print(f"{'AVERAGE':<15} {avg_accuracy:.4f} ({avg_accuracy*100:.2f}%)")
        print()
        print(f"✅ Datasets processed: {n_ok}/{len(UCR_DATASETS)}")
        print(f"📈 Average accuracy: {avg_accuracy*100:.2f}%")
    
    print()
    print("=" * 80)
    print("✅ Benchmark completed!")
    print("=" * 80)
    print()
    
    return results


if __name__ == "__main__":
    results = main()
