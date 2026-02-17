 # -*- coding: utf-8 -*-
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from modelos.cliente import Cliente, ClienteRegular, ClientePremium, ClienteCorporativo
from utils.validador import ValidadorDatos
from utils.persistencia import PersistenciaJSON
from gestor.logger import LoggerSistema
from modelos.excepciones import (
    ClienteNoEncontradoError,
    ClienteInactivoError,
    EmailDuplicadoError,
    TelefonoDuplicadoError,
    OperacionCRUDError
)

class GestorClientes:
    def __init__(
        self,
        ruta_datos: str = "data/clientes.json",
        ruta_log: str = "logs/sistema.log"
    ):
        self.logger = LoggerSistema(ruta_log=ruta_log)
        self.logger.log_inicio_sistema()
        self.persistencia = PersistenciaJSON(ruta_archivo=ruta_datos)
        self.clientes: List[Cliente] = []
        self._cargar_clientes_desde_json()

    # CARGA Y GUARDADO
    
    def _cargar_clientes_desde_json(self) -> None:
        try:
            clientes_dict = self.persistencia.cargar_clientes()
            
            for cliente_data in clientes_dict:
                try:
                    cliente = self._dict_a_cliente(cliente_data)
                    self.clientes.append(cliente)
                except Exception as e:
                    self.logger.warning(
                        f"No se pudo cargar cliente {cliente_data.get('id_cliente')}: {e}"
                    )
            
            self.logger.info(f"Clientes cargados desde JSON: {len(self.clientes)}")
            
        except Exception as e:
            self.logger.warning(f"No se pudieron cargar clientes: {e}")
            self.clientes = []
    
    
    def _guardar_clientes_a_json(self) -> bool:
        try:
            clientes_dict = [cliente.to_dict() for cliente in self.clientes]
            self.persistencia.guardar(clientes_dict)
            self.logger.info(f"Clientes guardados en JSON: {len(clientes_dict)}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al guardar clientes", e)
            return False
    
    
    def _dict_a_cliente(self, data: Dict[str, Any]) -> Cliente:
        tipo = data.get('tipo_cliente')

        if 'fecha_registro' in data and isinstance(data['fecha_registro'], str):
            data['fecha_registro'] = datetime.fromisoformat(data['fecha_registro'])

        if 'fecha_vencimiento_premium' in data and isinstance(data['fecha_vencimiento_premium'], str):
            data['fecha_vencimiento_premium'] = datetime.fromisoformat(data['fecha_vencimiento_premium'])
        
        if tipo == 'ClienteRegular':
            return ClienteRegular(**data)
        elif tipo == 'ClientePremium':
            return ClientePremium(**data)
        elif tipo == 'ClienteCorporativo':
            return ClienteCorporativo(**data)
        else:
            raise ValueError(f"Tipo de cliente desconocido: {tipo}")

    # CREATE - CREAR CLIENTE
    
    def crear_cliente(self, tipo_cliente: str, **datos) -> Cliente:
        try:
            email = datos.get('email', '').lower().strip()
            if self._email_existe(email):
                raise EmailDuplicadoError(email)
            
            telefono = datos.get('telefono', '').strip()
            if self._telefono_existe(telefono):
                raise TelefonoDuplicadoError(telefono)
            
            tipo_normalizado = tipo_cliente.lower()
            
            if tipo_normalizado == 'regular':
                cliente = ClienteRegular(**datos)
            elif tipo_normalizado == 'premium':
                cliente = ClientePremium(**datos)
            elif tipo_normalizado == 'corporativo':
                cliente = ClienteCorporativo(**datos)
            else:
                raise ValueError(f"Tipo de cliente invalido: {tipo_cliente}")
            
            self.clientes.append(cliente)
            
            self._guardar_clientes_a_json()
            
            self.logger.log_cliente_creado(
                cliente.id_cliente,
                cliente.tipo_cliente,
                cliente.nombre
            )
            
            return cliente
            
        except (EmailDuplicadoError, TelefonoDuplicadoError) as e:
            self.logger.warning(str(e))
            raise
        except Exception as e:
            self.logger.error("Error al crear cliente", e)
            raise

    # READ - LISTAR Y BUSCAR CLIENTES
    
    def listar_clientes(
        self,
        activos: Optional[bool] = None,
        tipo: Optional[str] = None
    ) -> List[Cliente]:
        resultado = self.clientes.copy()
        if activos is not None:
            resultado = [c for c in resultado if c.activo == activos]
        if tipo:
            tipo_clase = f"Cliente{tipo.capitalize()}"
            resultado = [c for c in resultado if c.tipo_cliente == tipo_clase]
        
        return resultado
       
    def buscar_cliente(
        self,
        criterio: str,
        valor: str,
        incluir_inactivos: bool = False
    ) -> Optional[Cliente]:
        valor = valor.strip()
        
        if criterio == 'id':
            clientes_buscar = self.clientes if incluir_inactivos else [c for c in self.clientes if c.activo]
            resultado = next((c for c in clientes_buscar if c.id_cliente == valor), None)
        
        elif criterio == 'email':
            valor = valor.lower()
            clientes_buscar = self.clientes if incluir_inactivos else [c for c in self.clientes if c.activo]
            resultado = next((c for c in clientes_buscar if c.email == valor), None)
        
        elif criterio == 'telefono':
            clientes_buscar = self.clientes if incluir_inactivos else [c for c in self.clientes if c.activo]
            resultado = next((c for c in clientes_buscar if c.telefono == valor), None)
        
        else:
            resultado = None
        
        self.logger.log_busqueda(criterio, valor, resultado is not None)
        
        return resultado
    
    
    def obtener_cliente_por_id(self, id_cliente: str) -> Cliente:
        cliente = self.buscar_cliente('id', id_cliente, incluir_inactivos=True)
        
        if not cliente:
            raise ClienteNoEncontradoError(id_cliente)
        
        return cliente

    # UPDATE - ACTUALIZAR CLIENTE
    
    def actualizar_cliente(self, id_cliente: str, **cambios) -> Cliente:
        try:
            cliente = self.obtener_cliente_por_id(id_cliente)
            if not cliente.activo:
                raise ClienteInactivoError(id_cliente)
            if 'email' in cambios:
                nuevo_email = cambios['email'].lower().strip()
                if nuevo_email != cliente.email and self._email_existe(nuevo_email):
                    raise EmailDuplicadoError(nuevo_email)
                cambios['email'] = ValidadorDatos.validar_email(nuevo_email)
            if 'telefono' in cambios:
                nuevo_telefono = cambios['telefono'].strip()
                if nuevo_telefono != cliente.telefono and self._telefono_existe(nuevo_telefono):
                    raise TelefonoDuplicadoError(nuevo_telefono)
                cambios['telefono'] = ValidadorDatos.validar_telefono(nuevo_telefono)
            
            if 'nombre' in cambios:
                cambios['nombre'] = ValidadorDatos.validar_nombre(cambios['nombre'])
            
            if 'direccion' in cambios:
                cambios['direccion'] = ValidadorDatos.validar_direccion(cambios['direccion'])
            
            if 'ciudad' in cambios:
                cambios['ciudad'] = ValidadorDatos.validar_ciudad(cambios['ciudad'])
            
            campos_modificados = []
            for campo, valor in cambios.items():
                if hasattr(cliente, campo):
                    setattr(cliente, campo, valor)
                    campos_modificados.append(campo)
            
            self._guardar_clientes_a_json()
            
            self.logger.log_cliente_actualizado(id_cliente, campos_modificados)
            
            return cliente
            
        except (ClienteNoEncontradoError, ClienteInactivoError, 
                EmailDuplicadoError, TelefonoDuplicadoError) as e:
            self.logger.warning(str(e))
            raise
        except Exception as e:
            self.logger.error(f"Error al actualizar cliente {id_cliente}", e)
            raise

    # DELETE - ELIMINAR CLIENTE (SOFT DELETE)
    
    def eliminar_cliente(self, id_cliente: str) -> bool:
        try:
            cliente = self.obtener_cliente_por_id(id_cliente)
            
            if not cliente.activo:
                self.logger.warning(f"Cliente {id_cliente} ya estaba inactivo")
                return False

            cliente.activo = False
            
            self._guardar_clientes_a_json()
            
            self.logger.log_cliente_eliminado(id_cliente, cliente.nombre)
            
            return True
            
        except ClienteNoEncontradoError as e:
            self.logger.warning(str(e))
            raise
        except Exception as e:
            self.logger.error(f"Error al eliminar cliente {id_cliente}", e)
            raise
    
    
    def reactivar_cliente(self, id_cliente: str) -> bool:
        try:
            cliente = self.obtener_cliente_por_id(id_cliente)
            
            if cliente.activo:
                self.logger.warning(f"Cliente {id_cliente} ya estaba activo")
                return False
            
            cliente.activo = True
            
            self._guardar_clientes_a_json()
            
            self.logger.log_cliente_reactivado(id_cliente, cliente.nombre)
            
            return True
            
        except ClienteNoEncontradoError as e:
            self.logger.warning(str(e))
            raise
        except Exception as e:
            self.logger.error(f"Error al reactivar cliente {id_cliente}", e)
            raise

    # VALIDACIONES DE DUPLICADOS
    
    def _email_existe(self, email: str) -> bool:
        email = email.lower().strip()
        return any(c.email == email and c.activo for c in self.clientes)
      
    def _telefono_existe(self, telefono: str) -> bool:
        telefono = telefono.strip()
        return any(c.telefono == telefono and c.activo for c in self.clientes)

    # ESTADISTICAS Y REPORTES
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        clientes_activos = [c for c in self.clientes if c.activo]
        
        estadisticas = {
            'total_clientes': len(self.clientes),
            'clientes_activos': len(clientes_activos),
            'clientes_inactivos': len(self.clientes) - len(clientes_activos),
            'por_tipo': {
                'regular': len([c for c in clientes_activos if isinstance(c, ClienteRegular)]),
                'premium': len([c for c in clientes_activos if isinstance(c, ClientePremium)]),
                'corporativo': len([c for c in clientes_activos if isinstance(c, ClienteCorporativo)])
            },
            'beneficios_totales': sum(c.calcular_beneficio() for c in clientes_activos)
        }
        
        return estadisticas
    
    
    def generar_reporte_beneficios(self) -> List[Dict[str, Any]]:
        clientes_activos = [c for c in self.clientes if c.activo]
        
        reporte = []
        for cliente in clientes_activos:
            reporte.append({
                'id': cliente.id_cliente,
                'nombre': cliente.nombre,
                'tipo': cliente.tipo_cliente,
                'beneficio': cliente.calcular_beneficio()
            })
        
        reporte.sort(key=lambda x: x['beneficio'], reverse=True)
        
        return reporte

    # CIERRE DEL SISTEMA
    
    def cerrar(self) -> None:
        try:
            self._guardar_clientes_a_json()
            self.logger.log_cierre_sistema()
        except Exception as e:
            self.logger.error("Error al cerrar el sistema", e)

# FUNCION DE PRUEBA

def test_gestor():
    """
    Funcion de prueba para verificar el GestorClientes.
    Ejecutar: python gestor/gestor_clientes.py
    """
    print("=" * 70)
    print("PRUEBA DEL GESTOR DE CLIENTES - GIC")
    print("=" * 70)
    
    # Crear gestor
    gestor = GestorClientes(
        ruta_datos="data/clientes_test.json",
        ruta_log="logs/test_gestor.log"
    )
    
    print("\n1. CREAR CLIENTES")
    print("-" * 70)
    try:
        # Cliente Regular
        cliente1 = gestor.crear_cliente(
            'regular',
            nombre="Ana Martinez",
            email="ana@test.com",
            telefono="+56912345678",
            direccion="Calle Falsa 123",
            ciudad="Santiago"
        )
        print(f"Cliente Regular creado: {cliente1.nombre}")
        
        # Cliente Premium
        cliente2 = gestor.crear_cliente(
            'premium',
            nombre="Carlos Lopez",
            email="carlos@test.com",
            telefono="+56987654321",
            direccion="Av. Principal 456",
            ciudad="Valparaiso",
            descuento=0.20,
            puntos_acumulados=500
        )
        print(f"Cliente Premium creado: {cliente2.nombre}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n2. LISTAR CLIENTES")
    print("-" * 70)
    clientes = gestor.listar_clientes(activos=True)
    print(f"Total clientes activos: {len(clientes)}")
    for c in clientes:
        print(f"  - {c.nombre} ({c.tipo_cliente})")
    
    print("\n3. BUSCAR CLIENTE")
    print("-" * 70)
    cliente = gestor.buscar_cliente('email', 'ana@test.com')
    if cliente:
        print(f"Cliente encontrado: {cliente.nombre}")
    
    print("\n4. ACTUALIZAR CLIENTE")
    print("-" * 70)
    try:
        gestor.actualizar_cliente(
            cliente1.id_cliente,
            ciudad="Concepcion",
            direccion="Nueva Direccion 789"
        )
        print(f"Cliente actualizado: {cliente1.ciudad}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n5. ESTADISTICAS")
    print("-" * 70)
    stats = gestor.obtener_estadisticas()
    print(f"Total clientes: {stats['total_clientes']}")
    print(f"Activos: {stats['clientes_activos']}")
    print(f"Por tipo: Regular={stats['por_tipo']['regular']}, Premium={stats['por_tipo']['premium']}")
    print(f"Beneficios totales: ${stats['beneficios_totales']:,.2f}")
    
    print("\n6. CERRAR GESTOR")
    print("-" * 70)
    gestor.cerrar()
    print("Gestor cerrado correctamente")
    
    print("\n" + "=" * 70)
    print("Pruebas completadas")
    print("=" * 70)


if __name__ == "__main__":
    test_gestor()

