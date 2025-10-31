#!/usr/bin/env python
"""
Punto de entrada unificado.
  •  python selene.py              ->  REPL Selene
  •  python selene.py archivo.se   ->  Ejecuta script
  •  python selene.py --ide        ->  Abre IDE Luna
"""
from pathlib import Path
import sys

PROJ_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJ_DIR))                     # Proj root
sys.path.insert(0, str(PROJ_DIR / "Functions"))       # Core del lenguaje
sys.path.insert(0, str(PROJ_DIR / "Luna"))            # IDE
sys.path.insert(0, str(PROJ_DIR / "Libraries"))       # Librerías nativas

from Functions.core.interpreter import run_repl, run_file
from Luna.run import launch_luna

def main() -> None:
    if len(sys.argv) == 1:
        run_repl()
    elif sys.argv[1] == "--ide":
        launch_luna()
    elif len(sys.argv) == 2 and sys.argv[1] != "--ide":
        run_file(Path(sys.argv[1]))
    else:
        print("Uso: python selene.py [archivo.se] [--ide]")

if __name__ == "__main__":
    main()