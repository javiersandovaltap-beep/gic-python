# -- coding: utf-8 --
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from modelos.cliente_base import Cliente
from utils.validador import ValidadorDatos
from modelos.excepciones import DatosInsuficientesError


class ClienteCorporativo(Cliente):
    """
    Cliente empresarial con descuento por volumen y múltiples empleados.
    Beneficio = numero_empleados × $1.000 × descuento_volumen
    Ej: 150 empleados + 20% descuento → $30.000
    """

    campos = Cliente.campos_base + [
        'razon_social',
        'rut_empresa',
        'pais_empresa',
        'contacto_principal',
        'descuento_volumen',
        'numero_empleados'
    ]

    def __init__(self, **kwargs):
        kwargs['tipo_cliente'] = 'ClienteCorporativo'
        campos_corp_obligatorios = ['razon_social', 'rut_empresa', 'contacto_principal']
        campos_faltantes = [c for c in campos_corp_obligatorios if c not in kwargs]
        if campos_faltantes:
            raise DatosInsuficientesError(campos_faltantes)

        super().__init__(**kwargs)
        self.razon_social       = ValidadorDatos.validar_nombre(kwargs['razon_social'])
        self.pais_empresa       = kwargs.get('pais_empresa', 'CHILE').upper()
        self.rut_empresa        = ValidadorDatos.validar_rut_dni(
                                      kwargs['rut_empresa'],
                                      self.pais_empresa
                                  )
        self.contacto_principal = ValidadorDatos.validar_nombre(kwargs['contacto_principal'])
        self.descuento_volumen  = ValidadorDatos.validar_descuento(
                                      kwargs.get('descuento_volumen', 0.05)
                                  )
        self.numero_empleados   = ValidadorDatos.validar_numero_empleados(
                                      kwargs.get('numero_empleados', 1)
                                  )

    def calcular_beneficio(self) -> float:
        """Beneficio = numero_empleados × $1.000 × descuento_volumen"""
        return float(self.numero_empleados * 1000 * self.descuento_volumen)

    def aplicar_descuento_volumen(self, monto_compra: float) -> float:
        """Retorna el monto final luego de aplicar el descuento corporativo."""
        return float(monto_compra - (monto_compra * self.descuento_volumen))

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'razon_social':      self.razon_social,
            'rut_empresa':       self.rut_empresa,
            'pais_empresa':      self.pais_empresa,
            'contacto_principal': self.contacto_principal,
            'descuento_volumen': self.descuento_volumen,
            'numero_empleados':  self.numero_empleados
        })
        return data

    def __str__(self) -> str:
        base_str = super().__str__()
        return (
            f"{base_str}\n"
            f"  Razón Social: {self.razon_social}\n"
            f"  RUT/DNI:      {self.rut_empresa} ({self.pais_empresa})\n"
            f"  Contacto:     {self.contacto_principal}\n"
            f"  Empleados:    {self.numero_empleados}\n"
            f"  Desc. Vol.:   {self.descuento_volumen * 100:.1f}%\n"
            f"  Beneficio:    ${self.calcular_beneficio():,.2f}"
        )
