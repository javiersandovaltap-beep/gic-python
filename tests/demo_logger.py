# -- coding: utf-8 --
"""
Demo del sistema de logging del GIC.
Ejecutar directamente para verificar niveles INFO/WARNING/ERROR:

    python tests/demo_logger.py
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from gestor.logger import LoggerSistema


def test_logger():
    print("=" * 70)
    print("DEMO DE SISTEMA DE LOGGING - GIC")
    print("=" * 70)

    logger = LoggerSistema(
        nombre_logger="GIC_TEST",
        ruta_log="logs/test_sistema.log",
        mostrar_consola=True
    )

    # ── 1. Inicio ─────────────────────────────────────────────────────────
    print("\n1️⃣  INICIO DEL SISTEMA")
    print("-" * 70)
    logger.log_inicio_sistema()

    # ── 2. Operaciones ────────────────────────────────────────────────────
    print("\n2️⃣  LOGS DE OPERACIONES")
    print("-" * 70)
    logger.log_cliente_creado(
        "550e8400-e29b-41d4-a716-446655440000",
        "ClientePremium",
        "Juan Perez"
    )
    logger.log_cliente_actualizado(
        "550e8400-e29b-41d4-a716-446655440000",
        ["email", "telefono"]
    )
    logger.log_busqueda("email", "juan@email.com", True)

    # ── 3. Advertencias ───────────────────────────────────────────────────
    print("\n3️⃣  LOGS DE ADVERTENCIAS")
    print("-" * 70)
    logger.log_error_validacion("email", "usuario.com", "Falta el simbolo @")

    # ── 4. Errores ────────────────────────────────────────────────────────
    print("\n4️⃣  LOGS DE ERRORES")
    print("-" * 70)
    try:
        raise ValueError("Error de prueba")
    except Exception as e:
        logger.log_error_persistencia("guardar", str(e))

    # ── 5. Estadísticas ───────────────────────────────────────────────────
    print("\n5️⃣  ESTADISTICAS DEL LOG")
    print("-" * 70)
    stats = logger.obtener_estadisticas_log()
    print(f"  Archivo:      {stats['ruta']}")
    print(f"  Tamaño:       {stats['tamano']} bytes")
    print(f"  Total líneas: {stats['total_lineas']}")
    print(f"  INFO: {stats['info']}  |  WARNING: {stats['warning']}  |  ERROR: {stats['error']}")

    # ── 6. Últimas líneas ─────────────────────────────────────────────────
    print("\n6️⃣  ULTIMAS 5 LINEAS DEL LOG")
    print("-" * 70)
    for linea in logger.ver_ultimas_lineas(5):
        print(f"  {linea.strip()}")

    # ── 7. Cierre ─────────────────────────────────────────────────────────
    print("\n7️⃣  CIERRE DEL SISTEMA")
    print("-" * 70)
    logger.log_cierre_sistema()

    print("\n" + "=" * 70)
    print("✅ Demo completada")
    print(f"  Log generado en: logs/test_sistema.log")
    print("=" * 70)


if __name__ == "__main__":
    test_logger()
