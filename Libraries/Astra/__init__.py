# Astra v0.1 - Numerical Computing Library for Selene
"""
Astra es la librería nativa de Selene para la computación numérica.
Ofrece tipos de datos de alto rendimiento (vectores y matrices) con una
sintaxis sencilla e intuitiva, diseñada para el ecosistema de Selene.

Backend: NumPy
"""
from __future__ import annotations
import numpy as np
from typing import List, Dict, Callable, Any

# ----------------------------------------------------------------------
# Clases Principales: Vector y Matriz
# ----------------------------------------------------------------------

class Vector:
    """
    Representa un vector (array de 1D) en Astra.
    Es un contenedor para un array de NumPy con una API amigable.
    """
    def __init__(self, data: List[float | int]):
        self._data = np.array(data)

    def __repr__(self) -> str:
        return f"Vector({self._data.tolist()})"

    def __str__(self) -> str:
        return f"V{self._data.tolist()}"

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

class Matriz:
    """
    Representa una matriz (array de 2D) en Astra.
    """
    def __init__(self, data: List[List[float | int]]):
        self._data = np.array(data)
        if self._data.ndim != 2:
            raise ValueError("Los datos de una matriz deben ser bidimensionales.")

    def __repr__(self) -> str:
        return f"Matriz({self._data.tolist()})"

    def __str__(self) -> str:
        return f"M{self._data.tolist()}"

    @property
    def forma(self) -> tuple[int, int]:
        """Devuelve la forma de la matriz (filas, columnas)."""
        return self._data.shape

# ----------------------------------------------------------------------
# Funciones de Creación (expuestas a Selene)
# ----------------------------------------------------------------------

def crear_vector(data: List[float | int]) -> Vector:
    """Crea un objeto Vector."""
    return Vector(data)

def crear_matriz(data: List[List[float | int]]) -> Matriz:
    """Crea un objeto Matriz."""
    return Matriz(data)

# ----------------------------------------------------------------------
# Built-ins de Astra
# ----------------------------------------------------------------------

# Este diccionario mapea los nombres de las funciones en Selene
# a las funciones reales de Python en esta librería.
# El intérprete usará esto para saber qué funciones están disponibles.
ASTRA_BUILTINS: Dict[str, Callable] = {
    "vector": crear_vector,
    "matriz": crear_matriz,
}

# También exponemos las clases para que puedan ser usadas en el entorno
ASTRA_BUILTINS["Vector"] = Vector
ASTRA_BUILTINS["Matriz"] = Matriz