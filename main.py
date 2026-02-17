 # -*- coding: utf-8 -*-
"""
Sistema Gestor Inteligente de Clientes (GIC)
Punto de entrada principal del sistema

Autor: Javier Sandoval Tapia
Fecha: Febrero 2026
Version: 1.0

Uso:
    python main.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from interfaz.menu_consola import iniciar_menu


def main():
    try:
        iniciar_menu()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("SISTEMA INTERRUMPIDO POR EL USUARIO")
        print("=" * 70)
        print("Hasta pronto!\n")
        sys.exit(0)
    except Exception as e:
        print("\n\n" + "=" * 70)
        print("ERROR CRITICO DEL SISTEMA")
        print("=" * 70)
        print(f"Error: {e}")
        print("\nPor favor, revise los logs en: logs/sistema.log")
        print("=" * 70 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

