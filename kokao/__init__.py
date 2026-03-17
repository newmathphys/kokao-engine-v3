"""
KOKAO Engine v3.0.4

Biologically Plausible Cognitive Architecture based on 
Kosyakov's Theory of Functionally-Independent Structures.

Achieves 92.92% average accuracy on 9 real UCR datasets.

Authors:
    Vital Kalinouski / Виталий Калиновский
    V. Ovseychik / В. Овсейчик

Organization: newmathphys

Based on ideas from Yu.B. Kosyakov's book "My Brain" (1999).
Основано на идеях из книги Ю.Б. Косякова "Мой мозг" (1999).

Note: The mathematical method is in the public domain 
      (Russian Patent №2109332 expired).
      Математический метод находится в общественном достоянии 
      (патент РФ №2109332 утратил силу).
"""

__version__ = "3.0.6"
__author__ = "Vital Kalinouski, V. Ovseychik"
__email__ = "newmathphys@gmail.com"
__license__ = "MIT"
__organization__ = "newmathphys"

from kokao.main import KOKAOEngine

__all__ = ["KOKAOEngine", "__version__", "__author__", "__email__"]
