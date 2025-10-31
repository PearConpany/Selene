# Selene Language Parser
"""
Este módulo se encarga de analizar la sintaxis de Selene.
Transforma el código Selene en una representación intermedia o en Python
directamente, para que el intérprete lo ejecute.
"""
from __future__ import annotations
import re
import textwrap
from typing import List, Dict, Any, Tuple

# Expresiones regulares para la sintaxis de Selene
_BLOCK   = re.compile(r"^(si|mientras|repite|define|clase)\b.*(?::|=>)\s*$", re.I)
_IMP_OBJ = re.compile(r"de\s+([\w\.]+)\s+importa\s+([\w_\*]+)(?:\s+como\s+([\w_]+))?", re.I)
_IMP_MOD = re.compile(r"de\s+m[oó]?dulos\s+importa\s+([\w\.]+)(?:\s+como\s+([\w_]+))?", re.I)

def is_block_start(line: str) -> bool:
    """Determina si una línea es el comienzo de un bloque."""
    return bool(_BLOCK.match(line))

def parse_import(line: str) -> Tuple[str, str, str] | Tuple[str, str, None] | None:
    """Parsea una línea de importación."""
    if (m := _IMP_MOD.fullmatch(line)):
        return "module", m.group(1), m.group(2) or m.group(1)
    if (m := _IMP_OBJ.fullmatch(line)):
        return "object", m.group(1), m.group(2), m.group(3) or m.group(2)
    return None

def strip_colon(txt: str) -> str:
    """Elimina los dos puntos al final de una cadena si existen."""
    return txt[:-1] if txt.endswith(":") else txt

def to_python(lines: List[str]) -> str:
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
            out.append(indent_str + "if " + strip_colon(t[3:]) + ":")
        elif t.startswith("sino si "):
            out.append(indent_str + "elif " + strip_colon(t[8:]) + ":")
        elif t.startswith("sino"):
            out.append(indent_str + "else:")
        elif t.startswith("mientras "):
            out.append(indent_str + "while " + strip_colon(t[9:]) + ":")
        elif t.startswith("para "):
            match = re.match(r"para\s+(\w+)\s+en\s+(.+)", t)
            if match:
                var, iterable = match.groups()
                out.append(indent_str + f"for {var} in {strip_colon(iterable)}:")
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