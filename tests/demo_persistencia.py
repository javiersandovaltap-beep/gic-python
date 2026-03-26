# -- coding: utf-8 --
"""
Demo del sistema de persistencia JSON del GIC.
Ejecutar directamente para verificar guardado, carga y respaldos:

    python tests/demo_persistencia.py
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.persistencia import PersistenciaJSON


def test_persistencia():
    print("=" * 70)
    print("DEMO DE PERSISTENCIA JSON - GIC")
    print("=" * 70)

    persistencia = PersistenciaJSON("data/clientes_test.json")

    clientes_prueba = [
        {
            'id_cliente':   'test-001',
            'nombre':       'Cliente Prueba 1',
            'email':        'cliente1@test.com',
            'tipo_cliente': 'ClienteRegular'
        },
        {
            'id_cliente':   'test-002',
            'nombre':       'Cliente Prueba 2',
            'email':        'cliente2@test.com',
            'tipo_cliente': 'ClientePremium'
        }
    ]

    # ── 1. Guardar ────────────────────────────────────────────────────────
    print("\n1️⃣  GUARDAR CLIENTES")
    print("-" * 70)
    try:
        resultado = persistencia.guardar(clientes_prueba)
        print(f"  ✅ Clientes guardados: {resultado}")
        print(f"     Archivo: {persistencia.ruta_archivo}")
    except Exception as e:
        print(f"  ❌ Error al guardar: {e}")

    # ── 2. Cargar ─────────────────────────────────────────────────────────
    print("\n2️⃣  CARGAR CLIENTES")
    print("-" * 70)
    try:
        clientes_cargados = persistencia.cargar_clientes()
        print(f"  ✅ Clientes cargados: {len(clientes_cargados)}")
        for c in clientes_cargados:
            print(f"  • {c['nombre']} ({c['tipo_cliente']})")
    except Exception as e:
        print(f"  ❌ Error al cargar: {e}")

    # ── 3. Crear respaldo ─────────────────────────────────────────────────
    print("\n3️⃣  CREAR RESPALDO")
    print("-" * 70)
    try:
        ruta_respaldo = persistencia.crear_respaldo()
        if ruta_respaldo:
            print(f"  ✅ Respaldo creado: {Path(ruta_respaldo).name}")
        else:
            print("  ⚠ No se creó respaldo")
    except Exception as e:
        print(f"  ❌ Error al crear respaldo: {e}")

    # ── 4. Listar respaldos ───────────────────────────────────────────────
    print("\n4️⃣  LISTAR RESPALDOS")
    print("-" * 70)
    try:
        respaldos = persistencia.listar_respaldos()
        print(f"  ✅ Respaldos disponibles: {len(respaldos)}")
        for r in respaldos[:3]:
            fecha = r['fecha'].strftime('%Y-%m-%d %H:%M:%S')
            print(f"  • {r['nombre']} — {fecha}")
    except Exception as e:
        print(f"  ❌ Error al listar: {e}")

    # ── 5. Estadísticas ───────────────────────────────────────────────────
    print("\n5️⃣  ESTADISTICAS DEL ARCHIVO")
    print("-" * 70)
    try:
        stats = persistencia.obtener_estadisticas_archivo()
        print(f"  Archivo:          {stats['ruta']}")
        print(f"  Existe:           {stats['existe']}")
        print(f"  Tamaño:           {stats['tamano']} bytes")
        print(f"  Total clientes:   {stats['total_clientes']}")
        print(f"  Respaldos:        {stats['respaldos_disponibles']}")
    except Exception as e:
        print(f"  ❌ Error en estadísticas: {e}")

    # ── 6. Validar archivo ────────────────────────────────────────────────
    print("\n6️⃣  VALIDACION DE ARCHIVO")
    print("-" * 70)
    try:
        es_valido = persistencia.validar_archivo()
        icono = "✅" if es_valido else "❌"
        print(f"  {icono} Archivo válido: {es_valido}")
    except Exception as e:
        print(f"  ❌ Error en validación: {e}")

    print("\n" + "=" * 70)
    print("✅ Demo completada")
    print("=" * 70)


if __name__ == "__main__":
    test_persistencia()
