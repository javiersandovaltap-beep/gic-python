# -- coding: utf-8 --
"""
Demo de las clases Cliente del sistema GIC.
Ejecutar directamente para verificar el comportamiento de cada tipo:

    python tests/demo_clientes.py
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from modelos.cliente_regular import ClienteRegular
from modelos.cliente_premium import ClientePremium
from modelos.cliente_corporativo import ClienteCorporativo


def test_clientes():

    print("=" * 70)
    print("DEMO DE CLASES CLIENTE - GIC")
    print("=" * 70)

    cliente_regular     = None
    cliente_premium     = None
    cliente_corporativo = None

    # ── 1. Cliente Regular ────────────────────────────────────────────────
    print("\n1️⃣  CLIENTE REGULAR:")
    print("-" * 70)
    try:
        cliente_regular = ClienteRegular(
            nombre="Juan Pérez",
            email="juan@email.com",
            telefono="+56 9 1234 5678",
            direccion="Av. Providencia 123, Depto 45",
            ciudad="Santiago",
            nivel_satisfaccion=4
        )
        print(cliente_regular)
    except Exception as e:
        print(f"❌ Error: {e}")

    # ── 2. Cliente Premium ────────────────────────────────────────────────
    print("\n\n2️⃣  CLIENTE PREMIUM:")
    print("-" * 70)
    try:
        cliente_premium = ClientePremium(
            nombre="María González",
            email="maria@email.com",
            telefono="+54 9 11 1234 5678",
            direccion="Calle Corrientes 1234",
            ciudad="Buenos Aires",
            descuento=0.15,
            puntos_acumulados=250
        )
        print(cliente_premium)
        cliente_premium.agregar_puntos(50)
        print(f"\n  Después de agregar 50 puntos: {cliente_premium.puntos_acumulados} pts")
    except Exception as e:
        print(f"❌ Error: {e}")

    # ── 3. Cliente Corporativo ────────────────────────────────────────────
    print("\n\n3️⃣  CLIENTE CORPORATIVO:")
    print("-" * 70)
    try:
        cliente_corporativo = ClienteCorporativo(
            nombre="TechCorp Solutions",
            email="contacto@techcorp.cl",
            telefono="+56 2 2345 6789",
            direccion="Av. Vitacura 5678, Piso 10",
            ciudad="Santiago",
            razon_social="TechCorp Solutions SpA",
            rut_empresa="76.123.456-7",
            pais_empresa="CHILE",
            contacto_principal="Roberto Díaz",
            descuento_volumen=0.20,
            numero_empleados=150
        )
        print(cliente_corporativo)
        compra = 10000
        con_descuento = cliente_corporativo.aplicar_descuento_volumen(compra)
        print(f"\n  Compra ${compra:,.2f} con descuento → ${con_descuento:,.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # ── 4. Polimorfismo ───────────────────────────────────────────────────
    print("\n\n4️⃣  POLIMORFISMO — calcular_beneficio():")
    print("-" * 70)
    clientes = [c for c in [cliente_regular, cliente_premium, cliente_corporativo]
                if c is not None]
    if clientes:
        print()
        for cliente in clientes:
            print(f"  • {cliente.tipo_cliente:<25} ${cliente.calcular_beneficio():>10,.2f}")
    else:
        print("  ⚠ No se pudieron instanciar clientes.")

    # ── 5. Serialización ──────────────────────────────────────────────────
    print("\n\n5️⃣  SERIALIZACIÓN to_dict():")
    print("-" * 70)
    if cliente_premium:
        for clave, valor in cliente_premium.to_dict().items():
            print(f"  {clave:<30} {valor}")
    else:
        print("  ⚠ No hay cliente premium para serializar.")

    print("\n" + "=" * 70)
    print("✅ Demo completada")
    print("=" * 70)


if __name__ == "__main__":
    test_clientes()
