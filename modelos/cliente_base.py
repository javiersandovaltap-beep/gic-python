# -- coding: utf-8 --
from abc import ABC, abstractmethod
from datetime import datetime
import uuid
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.validador import ValidadorDatos
from modelos.excepciones import (
    ValidacionError,
    DatosInsuficientesError
)


class Cliente(ABC):
    """
    Clase base abstracta para todos los tipos de cliente del sistema GIC.
    Define la interfaz común: atributos base, validaciones, serialización
    y el método abstracto calcular_beneficio() que cada subclase implementa.
    """

    campos_base = [
        'id_cliente',
        'nombre',
        'email',
        'telefono',
        'direccion',
        'ciudad',
        'fecha_registro',
        'activo',
        'tipo_cliente'
    ]

    def __init__(self, **kwargs):
        campos_obligatorios = ['nombre', 'email', 'telefono', 'direccion', 'ciudad']
        campos_faltantes = [campo for campo in campos_obligatorios if campo not in kwargs]

        if campos_faltantes:
            raise DatosInsuficientesError(campos_faltantes)

        self.id_cliente    = kwargs.get('id_cliente', str(uuid.uuid4()))
        self.nombre        = ValidadorDatos.validar_nombre(kwargs['nombre'])
        self.email         = ValidadorDatos.validar_email(kwargs['email'])
        self.telefono      = ValidadorDatos.validar_telefono(kwargs['telefono'])
        self.direccion     = ValidadorDatos.validar_direccion(kwargs['direccion'])
        self.ciudad        = ValidadorDatos.validar_ciudad(kwargs['ciudad'])
        self.fecha_registro = kwargs.get('fecha_registro', datetime.now())
        self.activo        = kwargs.get('activo', True)
        self.tipo_cliente  = kwargs.get('tipo_cliente', 'Cliente')

    @abstractmethod
    def calcular_beneficio(self) -> float:
        """
        Calcula el beneficio económico del cliente según su tipo.
        Debe ser implementado por cada subclase.
        """
        pass

    def to_dict(self) -> dict:
        """Serializa el cliente a diccionario para persistencia JSON."""
        return {
            'id_cliente':      self.id_cliente,
            'tipo_cliente':    self.tipo_cliente,
            'nombre':          self.nombre,
            'email':           self.email,
            'telefono':        self.telefono,
            'direccion':       self.direccion,
            'ciudad':          self.ciudad,
            'fecha_registro':  self.fecha_registro.isoformat(),
            'activo':          self.activo
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Reconstruye una instancia desde un diccionario (cargado desde JSON)."""
        if 'fecha_registro' in data and isinstance(data['fecha_registro'], str):
            data['fecha_registro'] = datetime.fromisoformat(data['fecha_registro'])
        return cls(**data)

    def __str__(self) -> str:
        estado = "✓ Activo" if self.activo else "✗ Inactivo"
        return (
            f"[{self.tipo_cliente}] {self.nombre}\n"
            f"  ID:         {self.id_cliente}\n"
            f"  Email:      {self.email}\n"
            f"  Teléfono:   {self.telefono}\n"
            f"  Ciudad:     {self.ciudad}\n"
            f"  Estado:     {estado}\n"
            f"  Registrado: {self.fecha_registro.strftime('%Y-%m-%d')}"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id='{self.id_cliente[:8]}...', "
            f"nombre='{self.nombre}', "
            f"email='{self.email}')"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Cliente):
            return False
        return self.id_cliente == other.id_cliente

    def __hash__(self) -> int:
        return hash(self.id_cliente)
