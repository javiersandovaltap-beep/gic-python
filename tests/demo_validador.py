# -- coding: utf-8 --
"""
Demo del sistema de validaciones del GIC.
Ejecutar directamente para verificar regex y reglas de negocio:

    python tests/demo_validador.py
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.validador import ValidadorDatos


def test_validaciones():
    print("=" * 70)
    print("DEMO DE VALIDACIONES - GIC (MULTI-PAÍS)")
    print("=" * 70)

    # ── 1. Validaciones exitosas ──────────────────────────────────────────
    print("\n1️⃣  VALIDACIONES EXITOSAS")
    print("-" * 70)
    pruebas_exitosas = [
        ("Email",              ValidadorDatos.validar_email,              "juan@email.com"),
        ("Teléfono Chile",     ValidadorDatos.validar_telefono,           "+56 9 1234 5678"),
        ("Teléfono Argentina", ValidadorDatos.validar_telefono,           "+54 9 11 1234 5678"),
        ("Teléfono Brasil",    ValidadorDatos.validar_telefono,           "+55 11 9 1234 5678"),
        ("Dirección",          ValidadorDatos.validar_direccion,          "Av. Providencia 123, Santiago"),
        ("Ciudad",             ValidadorDatos.validar_ciudad,             "Santiago"),
        ("Nombre",             ValidadorDatos.validar_nombre,             "Juan Pérez"),
        ("Descuento",          ValidadorDatos.validar_descuento,          0.15),
        ("Puntos",             ValidadorDatos.validar_puntos,             150),
        ("Empleados",          ValidadorDatos.validar_numero_empleados,   50),
    ]
    for nombre, funcion, valor in pruebas_exitosas:
        try:
            resultado = funcion(valor)
            print(f"  ✅ {nombre:<22} '{valor}' → '{resultado}'")
        except Exception as e:
            print(f"  ❌ {nombre:<22} ERROR: {e}")

    # ── 2. RUT/DNI por país ───────────────────────────────────────────────
    print("\n2️⃣  VALIDACIONES RUT/DNI POR PAÍS")
    print("-" * 70)
    documentos_pais = [
        ("RUT Chile",              "12.345.678-9",   "CHILE"),
        ("RUT Chile (sin puntos)", "12345678-9",     "CHILE"),
        ("DNI Argentina",          "12345678",       "ARGENTINA"),
        ("CPF Brasil",             "12345678901",    "BRASIL"),
        ("CPF Brasil (formato)",   "123.456.789-01", "BRASIL"),
        ("DNI Perú",               "12345678",       "PERU"),
        ("Cédula Colombia",        "1234567890",     "COLOMBIA"),
        ("CI Uruguay",             "1234567-8",      "URUGUAY"),
    ]
    for nombre, documento, pais in documentos_pais:
        try:
            resultado = ValidadorDatos.validar_rut_dni(documento, pais)
            print(f"  ✅ {nombre:<28} '{documento}' → '{resultado}'")
        except Exception as e:
            print(f"  ❌ {nombre:<28} ERROR: {e}")

    # ── 3. Errores esperados ──────────────────────────────────────────────
    print("\n3️⃣  ERRORES ESPERADOS")
    print("-" * 70)
    pruebas_fallidas = [
        ("Email inválido",          ValidadorDatos.validar_email,            "usuario.com"),
        ("Teléfono inválido",       ValidadorDatos.validar_telefono,         "123456"),
        ("Dirección corta",         ValidadorDatos.validar_direccion,        "Calle 1"),
        ("Ciudad inválida",         ValidadorDatos.validar_ciudad,           "123"),
        ("RUT Chile inválido",      ValidadorDatos.validar_rut_dni,          ("12345", "CHILE")),
        ("DNI Argentina inválido",  ValidadorDatos.validar_rut_dni,          ("123", "ARGENTINA")),
        ("Descuento >100%",         ValidadorDatos.validar_descuento,        1.5),
        ("Empleados negativos",     ValidadorDatos.validar_numero_empleados, -10),
    ]
    for nombre, funcion, valor in pruebas_fallidas:
        try:
            if isinstance(valor, tuple):
                resultado = funcion(*valor)
            else:
                resultado = funcion(valor)
            print(f"  ⚠ {nombre:<26} NO falló (debería haber fallado)")
        except Exception as e:
            print(f"  ✅ {nombre:<26} {e.__class__.__name__} capturado correctamente")

    print("\n" + "=" * 70)
    print("✅ Demo completada")
    print("=" * 70)


if __name__ == "__main__":
    test_validaciones()
