# -- coding: utf-8 --
"""
Demo del GestorClientes del sistema GIC.
Ejecutar directamente para verificar operaciones CRUD:

    python tests/demo_gestor.py
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from gestor.gestor_clientes import GestorClientes


def test_gestor():
    print("=" * 70)
    print("DEMO DEL GESTOR DE CLIENTES - GIC")
    print("=" * 70)

    gestor = GestorClientes(
        ruta_datos="data/clientes_test.json",
        ruta_log="logs/test_gestor.log"
    )

    # ── 1. Crear clientes ─────────────────────────────────────────────────
    print("\n1️⃣  CREAR CLIENTES")
    print("-" * 70)
    cliente1 = None
    cliente2 = None
    try:
        cliente1 = gestor.crear_cliente(
            'regular',
            nombre="Ana Martinez",
            email="ana@test.com",
            telefono="+56 9 1234 5678",
            direccion="Calle Falsa 123, Depto 1",
            ciudad="Santiago"
        )
        print(f"  ✅ Regular creado:  {cliente1.nombre}")

        cliente2 = gestor.crear_cliente(
            'premium',
            nombre="Carlos Lopez",
            email="carlos@test.com",
            telefono="+56 9 8765 4321",
            direccion="Av. Principal 456, Piso 2",
            ciudad="Valparaiso",
            descuento=0.20,
            puntos_acumulados=500
        )
        print(f"  ✅ Premium creado:  {cliente2.nombre}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # ── 2. Listar clientes ────────────────────────────────────────────────
    print("\n2️⃣  LISTAR CLIENTES")
    print("-" * 70)
    clientes = gestor.listar_clientes(activos=True)
    print(f"  Total activos: {len(clientes)}")
    for c in clientes:
        print(f"  • {c.nombre} ({c.tipo_cliente})")

    # ── 3. Buscar cliente ─────────────────────────────────────────────────
    print("\n3️⃣  BUSCAR CLIENTE")
    print("-" * 70)
    cliente = gestor.buscar_cliente('email', 'ana@test.com')
    if cliente:
        print(f"  ✅ Encontrado: {cliente.nombre}")
    else:
        print("  ⚠ No encontrado.")

    # ── 4. Buscar por nombre ──────────────────────────────────────────────
    print("\n4️⃣  BUSCAR POR NOMBRE PARCIAL")
    print("-" * 70)
    resultados = gestor.buscar_por_nombre("lopez")
    print(f"  Resultados para 'lopez': {len(resultados)}")
    for c in resultados:
        print(f"  • {c.nombre} | {c.tipo_cliente}")

    # ── 5. Actualizar cliente ─────────────────────────────────────────────
    print("\n5️⃣  ACTUALIZAR CLIENTE")
    print("-" * 70)
    try:
        if cliente1:
            gestor.actualizar_cliente(
                cliente1.id_cliente,
                ciudad="Concepcion",
                direccion="Nueva Direccion 789, Casa 3"
            )
            print(f"  ✅ Ciudad actualizada: {cliente1.ciudad}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # ── 6. Estadísticas ───────────────────────────────────────────────────
    print("\n6️⃣  ESTADISTICAS")
    print("-" * 70)
    stats = gestor.obtener_estadisticas()
    print(f"  Total clientes:        {stats['total_clientes']}")
    print(f"  Activos:               {stats['clientes_activos']}")
    print(f"  Regular / Premium:     {stats['por_tipo']['regular']} / {stats['por_tipo']['premium']}")
    print(f"  Beneficios totales:    ${stats['beneficios_totales']:,.2f}")
    print(f"  Beneficio promedio:    ${stats['beneficio_promedio']:,.2f}")
    print(f"  Cliente top:           {stats['cliente_top']}")
    print(f"  Ciudad más común:      {stats['ciudad_mas_comun']}")

    # ── 7. Exportar CSV ───────────────────────────────────────────────────
    print("\n7️⃣  EXPORTAR CSV")
    print("-" * 70)
    try:
        ruta = gestor.exportar_csv("data/clientes_test_export.csv")
        print(f"  ✅ CSV exportado: {ruta}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # ── 8. Cerrar ─────────────────────────────────────────────────────────
    print("\n8️⃣  CERRAR GESTOR")
    print("-" * 70)
    gestor.cerrar()
    print("  ✅ Gestor cerrado correctamente")

    print("\n" + "=" * 70)
    print("✅ Demo completada")
    print("=" * 70)


if __name__ == "__main__":
    test_gestor()
