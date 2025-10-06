# Selene Language Built-in Functions
"""
Este módulo define las funciones y palabras clave incorporadas en Selene.
Cada función aquí implementa la lógica para un comando del lenguaje.
"""
from __future__ import annotations
import time
import importlib
from typing import Dict, Any, List

# El entorno (Environment) es un diccionario que mapea nombres de variables a valores.
Env = Dict[str, Any]

def _eval(expr: str, env: Env):
    """
    Evalúa una expresión en el contexto del entorno de Selene.
    Es una versión simplificada que intenta evaluar la expresión en Python.
    """
    try:
        # Primero, intenta evaluar la expresión como código Python.
        # Esto maneja variables, operaciones matemáticas, llamadas a funciones, etc.
        return eval(expr, {"__builtins__": __import__("builtins")}, env)
    except (NameError, SyntaxError):
        # Si falla, podría ser una cadena literal sin comillas.
        # Devolvemos la expresión original.
        return expr
    except Exception:
        # Para cualquier otro error, devolvemos None para indicar fallo.
        return None

def selene_toma(args: str, env: Env):
    """Asigna un valor a una variable. `toma x = 10`"""
    try:
        var, expr = map(str.strip, args.split("=", 1))
        env[var] = _eval(expr, env)
    except Exception as e:
        print(f"⚠️  Error en 'toma': {e}")

def selene_muestra(args: str, env: Env):
    """Imprime valores en la consola. `muestra "Hola", x`"""
    try:
        # Separar por comas, respetando las que están dentro de cadenas
        parts = [p.strip() for p in args.split(',')]
        results = [str(_eval(p, env)) for p in parts]
        print(" ".join(results))
    except Exception as e:
        print(f"⚠️  Error en 'muestra': {e}")

def selene_espera(args: str, env: Env):
    """Pausa la ejecución por un número de segundos. `espera 1.5`"""
    try:
        seconds = float(_eval(args, env))
        time.sleep(seconds)
    except (ValueError, TypeError) as e:
        print(f"⚠️  Error en 'espera': se esperaba un número. {e}")

def selene_lista(args: str, env: Env):
    """Crea una lista. `lista mi_lista = 1, 2, "tres"`"""
    try:
        var, items_str = map(str.strip, args.split("=", 1))
        # Evalúa la cadena de items como una lista de Python
        env[var] = _eval(f"[{items_str}]", env)
    except Exception as e:
        print(f"⚠️  Error en 'lista': {e}")

def selene_suma(args: str, env: Env):
    """Suma los elementos de una lista. `suma total = mi_lista`"""
    try:
        var, list_name = map(str.strip, args.split("=", 1))
        items = _eval(list_name, env)
        if isinstance(items, list):
            env[var] = sum(items)
        else:
            print(f"⚠️  Error en 'suma': '{list_name}' no es una lista.")
    except Exception as e:
        print(f"⚠️  Error en 'suma': {e}")

def _tk_root_exists():
    """Verifica si existe una raíz de Tkinter."""
    try:
        import tkinter as tk
        return bool(tk._default_root)
    except ImportError:
        return False

def selene_entrada(args: str, env: Env):
    """Lee una entrada del usuario. `entrada mi_variable`"""
    try:
        parts = args.split()
        var = parts[0] if parts else "entrada"
        limit = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 128

        val: str
        if _tk_root_exists():
            from tkinter import simpledialog, Tk
            # Prevenir la creación de una ventana raíz completa si no es necesario
            root = Tk()
            root.withdraw() # Ocultar la ventana principal
            val = simpledialog.askstring("Entrada Selene", f"{var} (máx {limit} caracteres):") or ""
            root.destroy()
        else:
            val = input(f"{var}: ")
        env[var] = val[:limit]
    except Exception as e:
        print(f"⚠️  Error en 'entrada': {e}")

# Mapeo de palabras clave de Selene a funciones de Python
BUILTINS: Dict[str, callable] = {
    "toma": selene_toma,
    "muestra": selene_muestra,
    "espera": selene_espera,
    "lista": selene_lista,
    "suma": selene_suma,
    "entrada": selene_entrada,
}