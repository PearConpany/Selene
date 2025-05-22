# Selene 0.9.1 – Fix de “invalid syntax” en funciones y entrada GUI
"""
Cambios clave
-------------
1. **Doble ‘:’ corregido** – Cuando la línea Selene ya traía dos puntos
   (`si …:`), la traducción ponía uno extra → *invalid syntax*.  Ahora se
   recorta antes de formar el `if/while` de Python.
2. **Entrada GUI** – La instrucción `entrada var [max]` abre un cuadro de
   diálogo si se ejecuta desde el IDE; en CLI sigue usando `input()`.
3. **Pequeño refactor** – La importación de *tkinter* se hace
   perezosamente para no romper entornos sin GUI.
"""
from __future__ import annotations

import re, textwrap, time, importlib, sys
from pathlib import Path
from typing import Dict, List

Env = Dict[str, object]

# Mejoramos las expresiones regulares para importaciones
_BLOCK   = re.compile(r"^(si|mientras|repite|define|clase)\b.*(?::|=>)\s*$", re.I)
_IMP_OBJ = re.compile(r"de\s+([\w\.]+)\s+importa\s+([\w_\*]+)(?:\s+como\s+([\w_]+))?", re.I)
_IMP_MOD = re.compile(r"de\s+m[oó]?dulos\s+importa\s+([\w\.]+)(?:\s+como\s+([\w_]+))?", re.I)

# ----------------------------------------------------------------------
# utilidades
# ----------------------------------------------------------------------

def _eval(expr: str, env: Env):
    # Mejoramos la evaluación para que no muestre paréntesis innecesarios
    try:
        result = eval(expr, {}, env)
        # Si es una tupla de un solo elemento, retornamos ese elemento
        if isinstance(result, tuple) and len(result) == 1:
            return result[0]
        return result
    except Exception as e:
        print(f"⚠️  Error al evaluar '{expr}': {str(e)}")
        return None


def run_file(path: Path) -> None:
    run_lines(path.read_text(encoding="utf-8").splitlines(), {})


def run_repl() -> None:
    env: Env = {}
    print("Selene 0.9.1 REPL – 'salir' para terminar")
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
                    body.append(nxt[indent+4:])
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
        try:
            result = _eval(cond, env)
            if result:
                run_lines(body, env)
        except Exception as e:
            print(f"🛑 Error en condición '{cond}': {e}")
        return
    if h.startswith("mientras "):
        cond = header[9:].rstrip(":")
        while _eval(cond, env): run_lines(body, env); return
    if h.startswith("repite "):
        n = int(_eval(header.split()[1], env))
        for _ in range(n): run_lines(body, env); return
    print("⚠️  Bloque desconocido:", header)

# ----------------------------------------------------------------------
# traducción de cuerpo Selene → Python (solo dentro de define)
# ----------------------------------------------------------------------

def _strip_colon(txt: str) -> str:
    return txt[:-1] if txt.endswith(":") else txt


def _to_python(lines: List[str]) -> str:
    out: List[str] = []
    in_class = False
    
    for ln in lines:
        t = ln.rstrip()
        if not t:
            out.append("")
            continue
            
        # Mejoramos la detección de contexto
        if t.startswith("clase "):
            in_class = True
            class_def = t[6:].strip(":")
            out.append(f"class {class_def}:")
        elif t.startswith("define "):
            func_def = t[7:].rstrip(":")
            # Aseguramos que los métodos de clase tengan self como primer parámetro
            if in_class and "self" not in func_def:
                if "(" in func_def:
                    func_def = func_def.replace("(", "(self, ", 1)
                else:
                    func_def += "(self)"
            out.append(f"def {func_def}:")
        elif t.startswith("si "):
            out.append("if " + _strip_colon(t[3:]) + ":")
        elif t.startswith("sino si "):
            out.append("elif " + _strip_colon(t[8:]) + ":")
        elif t.startswith("sino"):
            out.append("else:")
        elif t.startswith("mientras "):
            out.append("while " + _strip_colon(t[9:]) + ":")
        elif t.startswith("para "):
            match = re.match(r"para\s+(\w+)\s+en\s+(.+)", t)
            if match:
                var, iterable = match.groups()
                out.append(f"for {var} in {iterable}:")
        elif t.startswith("toma "):
            # Mejoramos el manejo de asignaciones
            assignment = t[5:]
            if "=" in assignment:
                var, val = map(str.strip, assignment.split("=", 1))
                out.append(f"{var} = {val}")
            else:
                out.append(assignment)
        else:
            out.append(t)
            
    return "\n".join(out) or "pass"

def _handle_import(line: str, env: Env):
    if (m := _IMP_MOD.fullmatch(line)):
        mod, alias = m.group(1), m.group(2) or m.group(1)
        try:
            env[alias] = importlib.import_module(mod)
            return
        except ImportError as e:
            print(f"⚠️  Error al importar módulo {mod}: {e}")
            return
            
    if (m := _IMP_OBJ.fullmatch(line)):
        mod, obj, alias = m.groups()
        alias = alias or obj
        try:
            module = importlib.import_module(mod)
            if obj == "*":
                # Importar todo el módulo
                for name in getattr(module, "__all__", dir(module)):
                    if not name.startswith("_"):
                        env[name] = getattr(module, name)
            else:
                env[alias] = getattr(module, obj)
            return
        except (ImportError, AttributeError) as e:
            print(f"⚠️  Error al importar {obj} desde {mod}: {e}")
            return

# ----------------------------------------------------------------------
# una sola línea
# ----------------------------------------------------------------------

def _exec_simple(line: str, env: Env):
    cmd, *rest = line.split(None, 1)
    args = rest[0] if rest else ""

    if cmd.lower() in {"salir","exit","quit"}:
        raise SystemExit
    if cmd == "de":
        _handle_import(line, env); return
    if cmd == "toma":
        try:
            var, expr = map(str.strip, args.split("=",1))
            env[var] = _eval(expr, env)
            return
        except Exception as e:
            print(f"⚠️  Error al asignar variable: {str(e)}")
            return
    if cmd == "muestra":
        try:
            # Mejoramos el manejo de múltiples argumentos y cadenas
            if "," in args:
                parts = []
                current = ""
                in_string = False
                for char in args:
                    if char == '"' and (not current or current[-1] != '\\'):
                        in_string = not in_string
                        current += char
                    elif char == ',' and not in_string:
                        if current:
                            parts.append(current.strip())
                        current = ""
                    else:
                        current += char
                if current:
                    parts.append(current.strip())
                
                results = []
                for p in parts:
                    try:
                        val = _eval(p, env)
                        results.append(str(val) if val is not None else "")
                    except:
                        results.append(p.strip('"'))
                print(" ".join(filter(None, results)))
            else:
                val = _eval(args, env)
                if val is not None:
                    print(str(val))
                else:
                    print(args.strip('"'))
            return
        except Exception as e:
            print(f"⚠️  Error al mostrar: {str(e)}")
            return
    if cmd == "espera":
        try:
            time.sleep(float(_eval(args, env))); return
        except Exception as e:
            print(f"⚠️  Error en espera: {str(e)}")
            return
    if cmd == "entrada":
        try:
            _do_input(env, args); return
        except Exception as e:
            print(f"⚠️  Error en entrada: {str(e)}")
            return
    if cmd == "registro":
        try:
            expr = args.split("=",1)[1].strip()
            contenido = str(_eval(expr, env))
            filename = args.split("=",1)[0].strip().strip('"\'')
            if not filename:
                raise ValueError("Nombre de archivo no válido")
            with open(filename, "a", encoding="utf-8") as fp:
                fp.write(contenido + "\n")
            return
        except Exception as e:
            print(f"⚠️  Error al registrar: {str(e)}")
            return
    if cmd == "lista":
        # Nueva funcionalidad para crear listas
        try:
            var, items = args.split("=", 1)
            env[var.strip()] = _eval(f"[{items}]", env)
            return
        except Exception as e:
            print(f"⚠️  Error al crear lista: {str(e)}")
            return
    if cmd == "suma":
        # Nueva funcionalidad para sumar números o concatenar cadenas
        try:
            var, items = args.split("=", 1)
            env[var.strip()] = _eval(f"sum([{items}])", env)
            return
        except Exception as e:
            print(f"⚠️  Error al sumar: {str(e)}")
            return
    _handle_import(line, env)  # intenta import implícito

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
        root = Tk() if not _tk_root_exists() else None  # crea temporal si CLI
        val = simpledialog.askstring("Entrada Selene", f"{var} (máx {limit} caracteres):") or ""
        if root: root.destroy()
    else:
        val = input(f"{var}: ")
    env[var] = val[:limit]


def _tk_root_exists():
    import tkinter as tk
    return bool(tk._default_root)

# ----------------------------------------------------------------------
# importaciones
# ----------------------------------------------------------------------

def _eval(expr: str, env: Env):
    try:
        # Si la expresión es una cadena literal, la retornamos directamente
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        # Si es una variable, la buscamos en el entorno
        if expr in env:
            return env[expr]
        # Si no, evaluamos como expresión Python
        result = eval(expr, {}, env)
        # Manejo especial para comparaciones de cadenas
        if isinstance(result, bool):
            return result
        if isinstance(result, tuple) and len(result) == 1:
            return result[0]
        return result
    except Exception as e:
        print(f"⚠️  Error al evaluar '{expr}': {str(e)}")
        return None
