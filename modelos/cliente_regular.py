# -- coding: utf-8 --
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from modelos.cliente_base import Cliente
from modelos.excepciones import ValidacionError


class ClienteRegular(Cliente):
    """
    Cliente estándar del sistema GIC.
    Su beneficio económico se calcula en base al nivel de satisfacción (1-5).
    Beneficio = nivel_satisfaccion × $100
    """

    campos = Cliente.campos_base + ['nivel_satisfaccion']

    def __init__(self, **kwargs):
        kwargs['tipo_cliente'] = 'ClienteRegular'
        super().__init__(**kwargs)
        self.nivel_satisfaccion = kwargs.get('nivel_satisfaccion', 3)
        if not (1 <= self.nivel_satisfaccion <= 5):
            raise ValidacionError(
                f"Nivel de satisfacción debe estar entre 1 y 5, "
                f"recibido: {self.nivel_satisfaccion}"
            )

    def calcular_beneficio(self) -> float:
        """Beneficio = nivel_satisfaccion × $100. Ej: nivel 4 → $400"""
        return float(self.nivel_satisfaccion * 100)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['nivel_satisfaccion'] = self.nivel_satisfaccion
        return data

    def __str__(self) -> str:
        base_str = super().__str__()
        estrellas = "⭐" * self.nivel_satisfaccion
        return (
            f"{base_str}\n"
            f"  Satisfacción: {estrellas} ({self.nivel_satisfaccion}/5)\n"
            f"  Beneficio:    ${self.calcular_beneficio():.2f}"
        )
