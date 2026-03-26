# -- coding: utf-8 --
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.append(str(Path(__file__).parent.parent))

from modelos.cliente_base import Cliente
from utils.validador import ValidadorDatos


class ClientePremium(Cliente):
    """
    Cliente con beneficios de descuento y puntos de lealtad.
    Beneficio = (puntos_acumulados × 10) + (descuento × 1000)
    Ej: 250 pts + 15% descuento → $2.650
    """

    campos = Cliente.campos_base + [
        'descuento',
        'fecha_vencimiento_premium',
        'puntos_acumulados'
    ]

    def __init__(self, **kwargs):
        kwargs['tipo_cliente'] = 'ClientePremium'
        super().__init__(**kwargs)
        self.descuento = ValidadorDatos.validar_descuento(
            kwargs.get('descuento', 0.1)
        )
        fecha_venc = kwargs.get('fecha_vencimiento_premium')
        if fecha_venc is None:
            self.fecha_vencimiento_premium = datetime.now() + timedelta(days=365)
        elif isinstance(fecha_venc, str):
            self.fecha_vencimiento_premium = datetime.fromisoformat(fecha_venc)
        else:
            self.fecha_vencimiento_premium = fecha_venc

        self.puntos_acumulados = ValidadorDatos.validar_puntos(
            kwargs.get('puntos_acumulados', 0)
        )

    def calcular_beneficio(self) -> float:
        """Beneficio = (puntos × 10) + (descuento × 1000)"""
        return float(self.puntos_acumulados * 10 + self.descuento * 1000)

    def agregar_puntos(self, puntos: int) -> None:
        """Suma puntos validados al acumulado del cliente."""
        self.puntos_acumulados += ValidadorDatos.validar_puntos(puntos)

    def canjear_puntos(self, puntos: int) -> float:
        """
        Descuenta puntos y retorna el valor monetario canjeado.
        Cada punto equivale a $10.
        """
        puntos = ValidadorDatos.validar_puntos(puntos)
        if puntos > self.puntos_acumulados:
            raise ValueError(
                f"Puntos insuficientes. "
                f"Disponibles: {self.puntos_acumulados}, solicitados: {puntos}"
            )
        self.puntos_acumulados -= puntos
        return float(puntos * 10)

    def renovar_premium(self, dias: int = 365) -> None:
        """Extiende la vigencia premium por los días indicados."""
        self.fecha_vencimiento_premium += timedelta(days=dias)

    def esta_vigente(self) -> bool:
        """Retorna True si la membresía premium no ha vencido."""
        return datetime.now() < self.fecha_vencimiento_premium

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'descuento':                  self.descuento,
            'fecha_vencimiento_premium':  self.fecha_vencimiento_premium.isoformat(),
            'puntos_acumulados':          self.puntos_acumulados
        })
        return data

    def __str__(self) -> str:
        base_str = super().__str__()
        vigencia   = "✓ Vigente" if self.esta_vigente() else "✗ Vencida"
        vencimiento = self.fecha_vencimiento_premium.strftime('%Y-%m-%d')
        return (
            f"{base_str}\n"
            f"  Descuento:    {self.descuento * 100:.1f}%\n"
            f"  Puntos:       {self.puntos_acumulados} pts\n"
            f"  Vencimiento:  {vencimiento} ({vigencia})\n"
            f"  Beneficio:    ${self.calcular_beneficio():,.2f}"
        )
