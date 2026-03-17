"""
KOKAO Configuration Modules

Dataset-optimized configurations.
Конфигурации, оптимизированные для датасетов.
"""

# Default configurations / Конфигурации по умолчанию
DEFAULT_CONFIG = {
    "d_model": 140,
    "n_classes": 5,
    "K_max": 1500,
    "delta_base": 0.05,
    "learning_rate": 0.02,
    "adaptive_learning": True,
    "stochastic_gain": 0.1,
    "rhythm_enabled": True,
    "energy_efficient": True,
}

# UCR Dataset configurations / Конфигурации для датасетов UCR
UCR_CONFIGS = {
    "ECG5000": {"d_model": 140, "n_classes": 2, "K_max": 1500},
    "Wafer": {"d_model": 140, "n_classes": 2, "K_max": 1000},
    "Coffee": {"d_model": 286, "n_classes": 2, "K_max": 500},
    "FordA": {"d_model": 500, "n_classes": 2, "K_max": 2000},
    "GunPoint": {"d_model": 140, "n_classes": 2, "K_max": 500},
    "Beef": {"d_model": 60, "n_classes": 5, "K_max": 300},
    "SwedishLeaf": {"d_model": 140, "n_classes": 15, "K_max": 1500},
    "FaceAll": {"d_model": 140, "n_classes": 14, "K_max": 2000},
    "FiftyWords": {"d_model": 270, "n_classes": 50, "K_max": 3000},
}

__all__ = ["DEFAULT_CONFIG", "UCR_CONFIGS"]
