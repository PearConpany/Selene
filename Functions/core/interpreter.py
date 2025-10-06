# Selene 0.9.2 – Fix para funciones, clases y evaluación
"""
Cambios clave
-------------
1. **Funciones y Clases** – Los bloques `define` y `clase` ahora funcionan.
   Se traducen a Python y se ejecutan en el entorno actual.
2. **Llamadas a funciones** – Ahora se pueden llamar a las funciones definidas,
   e.g., `mi_funcion(10)`.
3. **Refactor de `_eval`** – Se consolidaron dos funciones `_eval` duplicadas
   en una única versión más robusta.
4. **Corrección de indentación** – Se corrigió el manejo de la indentación
   en los bloques, permitiendo estructuras anidadas correctamente.
"""
from __future__ import annotations

import re, textwrap, time, importlib, sys
from pathlib import Path
from typing import Dict, List

Env = Dict[str, object]

# Expresiones regulares para la sintaxis de Selene
_BLOCK   = re.compile(r"^(si|mientras|repite|define|clase)\b.*(?::|=>)\s*$", re.I)
_IMP_OBJ = re.compile(r"de\s+([\w\.]+)\s+importa\s+([\w_\*]+)(?:\s+como\s+([\w_]+))?", re.I)
_IMP_MOD = re.compile(r"de\s+m[oó]?dulos\s+importa\s+([\w\.]+)(?:\s+como\s+([\w_]+))?", re.I)

# ----------------------------------------------------------------------
# utilidades
# ----------------------------------------------------------------------

def _eval(expr: str, env: Env):
    """Evalúa una expresión, manejando variables y literales de cadena."""
    try:
        # Si la expresión es una cadena literal, la retornamos directamente
        if expr.startswith(('"', "'")) and expr.endswith(('"', "'")):
            return expr[1:-1]
        # Si no, evaluamos como expresión Python
        return eval(expr, {"__builtins__": __import__("builtins")}, env)
    except (NameError, SyntaxError):
        # Si falla, puede ser una cadena que no requiere evaluación
        return expr
    except Exception:
        return None


def run_file(path: Path) -> None:
    run_lines(path.read_text(encoding="utf-8").splitlines(), {})


def run_repl() -> None:
    env: Env = {}
    print("Selene 0.9.2 REPL – 'salir' para terminar")
    while True:
        try:
            run_lines([input("selene> ")], env)
        except (EOFError, KeyboardInterrupt):
            print(); break

# ----------------------------------------------------------------------
# motor principal
# ----------------------------------------------------------------------

def run_lines(lines: List[str], env: Env) -> None:
    i = 0
    while i < len(lines):
        try:
            raw = lines[i]; i += 1
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            indent = len(raw) - len(raw.lstrip())
            strip  = raw.strip()

            if _BLOCK.match(strip):
                head = strip[:-1].strip() if strip.endswith(":") else strip.rsplit("=>",1)[0].strip()
                body: List[str] = []
                while i < len(lines):
                    nxt = lines[i]
                    if nxt.strip() and len(nxt)-len(nxt.lstrip()) <= indent:
                        break
                    body.append(nxt) # Pasamos la línea completa para preservar indentación
                    i += 1
                try:
                    _exec_block(head, body, env)
                except Exception as e:
                    print(f"🛑 Error en bloque '{head}': {e}")
            else:
                try:
                    _exec_simple(strip, env)
                except Exception as e:
                    print(f"🛑 Error en línea {i}: {e}")
        except SystemExit:
            raise
        except Exception as e:
            print(f"🛑 Error general en línea {i}: {e}")
            continue

# ----------------------------------------------------------------------
# bloques
# ----------------------------------------------------------------------

def _exec_block(header: str, body: List[str], env: Env):
    h = header.lower()
    if h.startswith("si "):
        cond = header[3:].rstrip(":")
        if _eval(cond, env):
            run_lines(body, env)
        return
    if h.startswith("mientras "):
        cond = header[9:].rstrip(":")
        while _eval(cond, env):
            run_lines(body, env)
        return
    if h.startswith("repite "):
        n = int(_eval(header.split()[1], env))
        for _ in range(n):
            run_lines(body, env)
        return

    if h.startswith("define ") or h.startswith("clase "):
        full_block_selene = [header + ":"] + body
        py_code = _to_python(full_block_selene)
        try:
            exec(py_code, env)
        except Exception as e:
            print(f"🛑 Error al definir bloque '{header}': {e}\n---\n{py_code}\n---")
        return

    print("⚠️  Bloque desconocido:", header)

# ----------------------------------------------------------------------
# traducción de cuerpo Selene → Python
# ----------------------------------------------------------------------

def _strip_colon(txt: str) -> str:
    return txt[:-1] if txt.endswith(":") else txt


def _to_python(lines: List[str]) -> str:
    """Traduce un bloque de código Selene a Python, preservando la indentación."""
    out: List[str] = []
    in_class = False

    if lines and lines[0].lstrip().startswith("clase "):
        in_class = True

    for ln in lines:
        indent_str = " " * (len(ln) - len(ln.lstrip()))
        t = ln.lstrip()

        if not t:
            out.append("")
            continue

        if t.startswith("clase "):
            out.append(indent_str + f"class {t[6:]}")
        elif t.startswith("define "):
            func_def = t[7:].rstrip(":")
            if in_class and "self" not in func_def and "__init__" not in func_def:
                if "(" in func_def: func_def = func_def.replace("(", "(self, ", 1)
                else: func_def += "(self)"
            out.append(indent_str + f"def {func_def}:")
        elif t.startswith("si "):
            out.append(indent_str + "if " + _strip_colon(t[3:]) + ":")
        elif t.startswith("sino si "):
            out.append(indent_str + "elif " + _strip_colon(t[8:]) + ":")
        elif t.startswith("sino"):
            out.append(indent_str + "else:")
        elif t.startswith("mientras "):
            out.append(indent_str + "while " + _strip_colon(t[9:]) + ":")
        elif t.startswith("para "):
            match = re.match(r"para\s+(\w+)\s+en\s+(.+)", t)
            if match:
                var, iterable = match.groups()
                out.append(indent_str + f"for {var} in {_strip_colon(iterable)}:")
        elif t.startswith("toma "):
            out.append(indent_str + t[5:])
        elif t.startswith("muestra "):
            args_str = t[8:]
            parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', args_str)
            py_args = ", ".join(p.strip() for p in parts)
            out.append(indent_str + f"print({py_args})")
        else:
            out.append(ln)

    code = "\n".join(out)
    return textwrap.dedent(code) or "pass"

def _handle_import(line: str, env: Env):
    if (m := _IMP_MOD.fullmatch(line)):
        mod, alias = m.group(1), m.group(2) or m.group(1)
        try:
            env[alias] = importlib.import_module(mod)
        except ImportError as e:
            print(f"⚠️  Error al importar módulo {mod}: {e}")
    elif (m := _IMP_OBJ.fullmatch(line)):
        mod, obj, alias = m.groups()
        alias = alias or obj
        try:
            module = importlib.import_module(mod)
            if obj == "*":
                for name in getattr(module, "__all__", dir(module)):
                    if not name.startswith("_"): env[name] = getattr(module, name)
            else:
                env[alias] = getattr(module, obj)
        except (ImportError, AttributeError) as e:
            print(f"⚠️  Error al importar {obj} desde {mod}: {e}")

# ----------------------------------------------------------------------
# una sola línea
# ----------------------------------------------------------------------

def _exec_simple(line: str, env: Env):
    cmd, *rest = line.split(None, 1)
    args = rest[0] if rest else ""

    if cmd.lower() in {"salir","exit","quit"}: raise SystemExit
    if cmd == "de": _handle_import(line, env); return
    if cmd == "toma":
        var, expr = map(str.strip, args.split("=",1))
        env[var] = _eval(expr, env)
    elif cmd == "muestra":
        parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', args)
        results = [str(_eval(p.strip(), env)) for p in parts]
        print(" ".join(results))
    elif cmd == "espera":
        time.sleep(float(_eval(args, env)))
    elif cmd == "entrada":
        _do_input(env, args)
    elif cmd == "registro":
        expr = args.split("=",1)[1].strip()
        contenido = str(_eval(expr, env))
        filename = args.split("=",1)[0].strip().strip('"\'')
        with open(filename, "a", encoding="utf-8") as fp:
            fp.write(contenido + "\n")
    elif cmd == "lista":
        var, items = args.split("=", 1)
        env[var.strip()] = _eval(f"[{items}]", env)
    elif cmd == "suma":
        var, items = args.split("=", 1)
        env[var.strip()] = _eval(f"sum([{items}])", env)
    else:
        # Si no es un comando, intentar como llamada a función o import
        try:
            _eval(line, env)
        except Exception:
             _handle_import(line, env)

# ----------------------------------------------------------------------
# input (GUI si hay root Tk)
# ----------------------------------------------------------------------

def _do_input(env: Env, args: str):
    parts = args.split()
    var   = parts[0] if parts else "entrada"
    limit = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 128

    val: str
    if _tk_root_exists():
        from tkinter import simpledialog, Tk
        root = Tk() if not _tk_root_exists() else None
        val = simpledialog.askstring("Entrada Selene", f"{var} (máx {limit} caracteres):") or ""
        if root: root.destroy()
    else:
        val = input(f"{var}: ")
    env[var] = val[:limit]


def _tk_root_exists():
    import tkinter as tk
    return bool(tk._default_root)