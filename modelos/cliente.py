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
        self.id_cliente = kwargs.get('id_cliente', str(uuid.uuid4()))
        self.nombre = ValidadorDatos.validar_nombre(kwargs['nombre'])
        self.email = ValidadorDatos.validar_email(kwargs['email'])
        self.telefono = ValidadorDatos.validar_telefono(kwargs['telefono'])       
        self.direccion = ValidadorDatos.validar_direccion(kwargs['direccion'])
        self.ciudad = ValidadorDatos.validar_ciudad(kwargs['ciudad'])
        self.fecha_registro = kwargs.get('fecha_registro', datetime.now())
        self.activo = kwargs.get('activo', True)
        self.tipo_cliente = kwargs.get('tipo_cliente', 'Cliente')
   
    @abstractmethod
    def calcular_beneficio(self) -> float:
        pass
    
    def to_dict(self) -> dict:
        return {
            'id_cliente': self.id_cliente,
            'tipo_cliente': self.tipo_cliente,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'fecha_registro': self.fecha_registro.isoformat(),
            'activo': self.activo
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        if 'fecha_registro' in data and isinstance(data['fecha_registro'], str):
            data['fecha_registro'] = datetime.fromisoformat(data['fecha_registro'])
        
        return cls(**data)
    
    def __str__(self) -> str:
        estado = "✓ Activo" if self.activo else "✗ Inactivo"
        return (
            f"[{self.tipo_cliente}] {self.nombre}\n"
            f"  ID: {self.id_cliente}\n"
            f"  Email: {self.email}\n"
            f"  Teléfono: {self.telefono}\n"
            f"  Ciudad: {self.ciudad}\n"
            f"  Estado: {estado}\n"
            f"  Registrado: {self.fecha_registro.strftime('%Y-%m-%d')}"
        )
      
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id='{self.id_cliente[:8]}...', "
            f"nombre='{self.nombre}', email='{self.email}')"
        )
      
    def __eq__(self, other) -> bool:
        if not isinstance(other, Cliente):
            return False
        return self.id_cliente == other.id_cliente
      
    def __hash__(self) -> int:
        return hash(self.id_cliente)

class ClienteRegular(Cliente):
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
        return 0.0
      
    def to_dict(self) -> dict:
        data = super().to_dict()
        data['nivel_satisfaccion'] = self.nivel_satisfaccion
        return data
     
    def __str__(self) -> str:
        base_str = super().__str__()
        estrellas = "⭐" * self.nivel_satisfaccion
        return f"{base_str}\n  Satisfacción: {estrellas} ({self.nivel_satisfaccion}/5)"

class ClientePremium(Cliente):
    campos = Cliente.campos_base + [
        'descuento',
        'fecha_vencimiento_premium',
        'puntos_acumulados'
    ]
    
    def __init__(self, **kwargs):
        kwargs['tipo_cliente'] = 'ClientePremium'
        super().__init__(**kwargs)
        descuento_raw = kwargs.get('descuento', 0.1)  # 10% por defecto
        self.descuento = ValidadorDatos.validar_descuento(descuento_raw)   
        # Fecha de vencimiento (por defecto: 1 año desde hoy)
        fecha_venc = kwargs.get('fecha_vencimiento_premium')
        if fecha_venc is None:
            from datetime import timedelta
            self.fecha_vencimiento_premium = datetime.now() + timedelta(days=365)
        elif isinstance(fecha_venc, str):
            self.fecha_vencimiento_premium = datetime.fromisoformat(fecha_venc)
        else:
            self.fecha_vencimiento_premium = fecha_venc
        # Puntos acumulados (default 0)
        self.puntos_acumulados = ValidadorDatos.validar_puntos(
            kwargs.get('puntos_acumulados', 0)
        )
    
    def calcular_beneficio(self) -> float:
        beneficio_puntos = self.puntos_acumulados * 10
        return beneficio_puntos
    
    def agregar_puntos(self, puntos: int) -> None:
        puntos = ValidadorDatos.validar_puntos(puntos)
        self.puntos_acumulados += puntos
    
    
    def canjear_puntos(self, puntos: int) -> float:
        puntos = ValidadorDatos.validar_puntos(puntos)
        
        if puntos > self.puntos_acumulados:
            raise ValueError(
                f"Puntos insuficientes. Disponibles: {self.puntos_acumulados}, "
                f"solicitados: {puntos}"
            )
        
        self.puntos_acumulados -= puntos
        return puntos * 10  # Cada punto = $10
    
    
    def renovar_premium(self, dias: int = 365) -> None:
        from datetime import timedelta
        self.fecha_vencimiento_premium += timedelta(days=dias)
      
    def esta_vigente(self) -> bool:
        return datetime.now() < self.fecha_vencimiento_premium
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'descuento': self.descuento,
            'fecha_vencimiento_premium': self.fecha_vencimiento_premium.isoformat(),
            'puntos_acumulados': self.puntos_acumulados
        })
        return data
     
    def __str__(self) -> str:
        base_str = super().__str__()
        vigencia = "✓ Vigente" if self.esta_vigente() else "✗ Vencida"
        vencimiento = self.fecha_vencimiento_premium.strftime('%Y-%m-%d')
        
        return (
            f"{base_str}\n"
            f"  Descuento: {self.descuento * 100:.1f}%\n"
            f"  Puntos: {self.puntos_acumulados} pts (${self.calcular_beneficio():.2f})\n"
            f"  Vencimiento: {vencimiento} ({vigencia})"
        )

class ClienteCorporativo(Cliente):
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
        # Validar campos obligatorios corporativos
        campos_corp_obligatorios = ['razon_social', 'rut_empresa', 'contacto_principal']
        campos_faltantes = [c for c in campos_corp_obligatorios if c not in kwargs]
        
        if campos_faltantes:
            raise DatosInsuficientesError(campos_faltantes)
        super().__init__(**kwargs)
        self.razon_social = ValidadorDatos.validar_nombre(kwargs['razon_social'])
        self.pais_empresa = kwargs.get('pais_empresa', 'CHILE').upper()
        self.rut_empresa = ValidadorDatos.validar_rut_dni(
            kwargs['rut_empresa'],
            self.pais_empresa
        )
        self.contacto_principal = ValidadorDatos.validar_nombre(kwargs['contacto_principal'])
        descuento_vol = kwargs.get('descuento_volumen', 0.05)
        self.descuento_volumen = ValidadorDatos.validar_descuento(descuento_vol)
        self.numero_empleados = ValidadorDatos.validar_numero_empleados(
            kwargs.get('numero_empleados', 1)
        )
    
    
    def calcular_beneficio(self) -> float:
        compra_promedio_empleado = 1000
        total_compras_estimadas = self.numero_empleados * compra_promedio_empleado
        ahorro = total_compras_estimadas * self.descuento_volumen
        
        return ahorro
       
    def aplicar_descuento_volumen(self, monto_compra: float) -> float:
        descuento_aplicado = monto_compra * self.descuento_volumen
        return monto_compra - descuento_aplicado
    
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'razon_social': self.razon_social,
            'rut_empresa': self.rut_empresa,
            'pais_empresa': self.pais_empresa,
            'contacto_principal': self.contacto_principal,
            'descuento_volumen': self.descuento_volumen,
            'numero_empleados': self.numero_empleados
        })
        return data
    
    
    def __str__(self) -> str:
        base_str = super().__str__()
        ahorro_anual = self.calcular_beneficio()
        
        return (
            f"{base_str}\n"
            f"  Razón Social: {self.razon_social}\n"
            f"  RUT/DNI: {self.rut_empresa} ({self.pais_empresa})\n"
            f"  Contacto: {self.contacto_principal}\n"
            f"  Empleados: {self.numero_empleados}\n"
            f"  Descuento Volumen: {self.descuento_volumen * 100:.1f}%\n"
            f"  Ahorro Estimado Anual: ${ahorro_anual:,.2f}"
        )


# FUNCIÓN DE PRUEBA


def test_clientes():
    """
    Función de prueba para verificar las clases Cliente.
    Ejecutar directamente este módulo para ver ejemplos.
    """
    print("=" * 70)
    print("PRUEBA DE CLASES CLIENTE - GIC")
    print("=" * 70)
    
    # Inicializar variables ANTES de los bloques try
    cliente_regular = None
    cliente_premium = None
    cliente_corporativo = None
    
    # Crear cliente regular
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
        print(f"\n   Beneficio económico: ${cliente_regular.calcular_beneficio():.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Crear cliente premium
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
        print(f"\n   Beneficio económico: ${cliente_premium.calcular_beneficio():,.2f}")
        
        # Agregar puntos
        cliente_premium.agregar_puntos(50)
        print(f"   Después de agregar 50 puntos: {cliente_premium.puntos_acumulados} pts")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Crear cliente corporativo
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
        print(f"\n   Beneficio económico anual: ${cliente_corporativo.calcular_beneficio():,.2f}")
        
        # Aplicar descuento a una compra
        compra_ejemplo = 10000
        con_descuento = cliente_corporativo.aplicar_descuento_volumen(compra_ejemplo)
        print(f"   Compra de ${compra_ejemplo:,.2f} con descuento: ${con_descuento:,.2f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Demostrar polimorfismo (solo si todos se crearon correctamente)
    print("\n\n4️⃣  DEMOSTRACIÓN DE POLIMORFISMO:")
    print("-" * 70)
    
    # Filtrar solo clientes creados exitosamente
    clientes = [c for c in [cliente_regular, cliente_premium, cliente_corporativo] if c is not None]
    
    if len(clientes) > 0:
        print("\n   Beneficios calculados para cada tipo de cliente:\n")
        for cliente in clientes:
            beneficio = cliente.calcular_beneficio()
            print(f"   • {cliente.tipo_cliente}: ${beneficio:,.2f}")
    else:
        print("\n   ⚠ No se pudieron crear clientes para la demostración")
    
    # Serialización (solo si cliente_premium existe)
    print("\n\n5️⃣  SERIALIZACIÓN A DICCIONARIO:")
    print("-" * 70)
    if cliente_premium:
        dict_cliente = cliente_premium.to_dict()
        print(f"\n   {dict_cliente}")
    else:
        print("\n   ⚠ No hay cliente premium para serializar")
    
    print("\n" + "=" * 70)
    print("✅ Pruebas completadas")
    print("=" * 70)


if __name__ == "__main__":
    test_clientes()


