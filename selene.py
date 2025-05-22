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
sys.path.insert(0, str(PROJ_DIR))                     # para imports relativos
sys.path.insert(0, str(PROJ_DIR / "Functions"))       # núcleo + IDE

from Functions.core.interpreter import run_repl, run_file

def main() -> None:
    if len(sys.argv) == 1:                            # REPL
        run_repl()
    elif sys.argv[1] == "--ide":                      # IDE
        from Luna.run import launch_luna              # import perezoso
        launch_luna()
    elif len(sys.argv) == 2:                          # archivo.se
        run_file(Path(sys.argv[1]))
    else:
        print("Uso: python selene.py [archivo.se] [--ide]")

if __name__ == "__main__":
    main()
