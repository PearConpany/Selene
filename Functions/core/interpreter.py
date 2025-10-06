# Selene 1.0 - Refactored Interpreter
"""
Cambios clave
-------------
1. **Arquitectura Modular**: El intérprete se ha refactorizado en tres
   componentes principales:
   - `interpreter.py`: El motor principal que orquesta la ejecución.
   - `lang/parser.py`: Se encarga de analizar la sintaxis de Selene.
   - `lang/builtins.py`: Implementa las funciones nativas del lenguaje.
2. **Optimización**: La separación de responsabilidades mejora la claridad
   y el rendimiento, sentando las bases para futuras optimizaciones.
3. **Extensibilidad**: El nuevo diseño facilita la adición de nuevas
   librerías y funcionalidades (como 'Astra').
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Dict, List, Any

# Añadir directorios al path para permitir importaciones relativas
PROJ_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJ_DIR))
sys.path.insert(0, str(PROJ_DIR / "Functions" / "core"))

from lang.parser import is_block_start, to_python, parse_import
from lang.builtins import BUILTINS, _eval

Env = Dict[str, Any]

# ----------------------------------------------------------------------
# Motor de Ejecución
# ----------------------------------------------------------------------

def run_lines(lines: List[str], env: Env) -> None:
    """Ejecuta una lista de líneas de código Selene."""
    i = 0
    while i < len(lines):
        raw_line = lines[i]
        i += 1

        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent_level = len(raw_line) - len(raw_line.lstrip())
        stripped_line = raw_line.strip()

        if is_block_start(stripped_line):
            header = stripped_line
            body = []
            while i < len(lines) and (not lines[i].strip() or (len(lines[i]) - len(lines[i].lstrip()) > indent_level)):
                body.append(lines[i])
                i += 1
            _exec_block(header, body, env)
        else:
            _exec_simple(stripped_line, env)

def _exec_simple(line: str, env: Env) -> None:
    """Ejecuta una única instrucción de Selene."""
    cmd, *rest = line.split(None, 1)
    args = rest[0] if rest else ""

    if cmd.lower() in {"salir", "exit", "quit"}:
        raise SystemExit

    # Buscar en los built-ins
    if cmd in BUILTINS:
        BUILTINS[cmd](args, env)
        return

    # Intentar como importación de librería nativa
    if cmd == "importa":
        lib_name = args.strip()
        if lib_name:
            _handle_native_import(lib_name, env)
        else:
            print("⚠️ Error: se requiere el nombre de una librería (ej. 'importa astra').")
        return

    # Intentar como importación de módulo Python
    if cmd == "de":
        _handle_import(line, env)
        return

    # Si no es un comando conocido, intentar evaluar como expresión
    # (ej. llamada a función, acceso a objeto)
    try:
        _eval(line, env)
    except Exception as e:
        print(f"🛑 Error al ejecutar '{line}': {e}")


def _exec_block(header: str, body: List[str], env: Env) -> None:
    """Ejecuta un bloque de código (si, mientras, define, etc.)."""
    h = header.lower().strip()

    # Bloques de control que se ejecutan recursivamente
    if h.startswith("si "):
        cond = header.strip()[3:].rstrip(":")
        if _eval(cond, env):
            run_lines(body, env)
    elif h.startswith("mientras "):
        cond = header.strip()[9:].rstrip(":")
        while _eval(cond, env):
            run_lines(body, env)
    # Bloques que se traducen a Python
    elif h.startswith("define ") or h.startswith("clase "):
        selene_code = [header] + body
        python_code = to_python(selene_code)
        try:
            exec(python_code, env)
        except Exception as e:
            print(f"🛑 Error al definir bloque:\n{python_code}\n{e}")
    else:
        print(f"⚠️ Bloque desconocido: {header}")


def _handle_native_import(lib_name: str, env: Env) -> None:
    """Maneja la importación de librerías nativas de Selene (ej. 'importa astra')."""
    import importlib
    try:
        # Capitalizar para coincidir con la convención de nombres de módulo (ej. astra -> Astra)
        module = importlib.import_module(lib_name.capitalize())

        # Las librerías nativas deben exponer un diccionario de built-ins
        builtins_dict_name = f"{lib_name.upper()}_BUILTINS"
        if hasattr(module, builtins_dict_name):
            lib_builtins = getattr(module, builtins_dict_name)
            env.update(lib_builtins)
            print(f"✓ Librería '{lib_name}' cargada.")
        else:
            print(f"⚠️ Error: La librería '{lib_name}' no tiene una definición de built-ins ({builtins_dict_name}).")

    except ImportError:
        print(f"⚠️ Error: No se pudo encontrar la librería nativa '{lib_name}'.")
    except Exception as e:
        print(f"⚠️ Error al cargar la librería '{lib_name}': {e}")


def _handle_import(line: str, env: Env) -> None:
    """Maneja las instrucciones de importación de módulos de Python."""
    import importlib
    parsed = parse_import(line)
    if not parsed:
        print(f"⚠️ Error de sintaxis en import: {line}")
        return

    import_type = parsed[0]

    try:
        if import_type == "module":
            _, mod_name, alias = parsed
            env[alias] = importlib.import_module(mod_name)
        elif import_type == "object":
            _, mod_name, obj_name, alias = parsed
            module = importlib.import_module(mod_name)
            if obj_name == "*":
                # Importar todo del módulo
                for name in getattr(module, "__all__", dir(module)):
                    if not name.startswith("_"):
                        env[name] = getattr(module, name)
            else:
                # Importar un objeto específico
                env[alias] = getattr(module, obj_name)
    except (ImportError, AttributeError) as e:
        print(f"⚠️ Error al importar '{line}': {e}")
    except ValueError:
        print(f"⚠️ Error de sintaxis en import: {line}")

# ----------------------------------------------------------------------
# Puntos de Entrada
# ----------------------------------------------------------------------

def run_file(path: Path) -> None:
    """Ejecuta un archivo .se."""
    env: Env = {}
    # Inicializar con funciones built-in
    env.update(BUILTINS)
    run_lines(path.read_text(encoding="utf-8").splitlines(), env)

def run_repl() -> None:
    """Inicia el REPL interactivo."""
    env: Env = {}
    # Inicializar con funciones built-in
    env.update(BUILTINS)
    print("Selene 1.0 REPL – 'salir' para terminar")
    while True:
        try:
            line = input("selene> ")
            if line.strip():
                run_lines([line], env)
        except (EOFError, KeyboardInterrupt, SystemExit):
            print("\n¡Adiós!")
            break