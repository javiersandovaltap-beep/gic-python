# -*- coding: utf-8 -*-
"""
Modulo de Interfaz de Consola - GIC
Menu interactivo para operaciones CRUD del sistema.
"""

import sys
from pathlib import Path
from typing import Optional

sys.path.append(str(Path(__file__).parent.parent))

from gestor.gestor_clientes import GestorClientes
from modelos.cliente import ClienteRegular, ClientePremium, ClienteCorporativo
from modelos.excepciones import (
    ErrorGestionClientes,
    ClienteNoEncontradoError,
    EmailDuplicadoError,
    TelefonoDuplicadoError,
    ValidacionError
)


class MenuConsola:
    """Interfaz de usuario por consola para el sistema GIC."""
    
    def __init__(self):
        print("\n" + "=" * 70)
        print("GESTOR INTELIGENTE DE CLIENTES (GIC)")
        print("=" * 70)
        print("Iniciando sistema...")
        
        try:
            self.gestor = GestorClientes()
            print("Sistema iniciado correctamente\n")
        except Exception as e:
            print(f"\nError al iniciar el sistema: {e}")
            sys.exit(1)
    
    
    def mostrar_menu_principal(self) -> None:
        """Muestra el menu principal del sistema."""
        while True:
            print("\n" + "=" * 70)
            print("MENU PRINCIPAL")
            print("=" * 70)
            print("1.  Crear cliente")
            print("2.  Listar clientes")
            print("3.  Buscar cliente")
            print("4.  Actualizar cliente")
            print("5.  Eliminar cliente")
            print("6.  Reactivar cliente")
            print("7.  Ver estadisticas")
            print("8.  Reporte de beneficios")
            print("9.  Ver detalles de cliente")
            print("0.  Salir")
            print("=" * 70)
            
            opcion = input("\nSeleccione una opcion: ").strip()
            
            if opcion == '1':
                self.menu_crear_cliente()
            elif opcion == '2':
                self.menu_listar_clientes()
            elif opcion == '3':
                self.menu_buscar_cliente()
            elif opcion == '4':
                self.menu_actualizar_cliente()
            elif opcion == '5':
                self.menu_eliminar_cliente()
            elif opcion == '6':
                self.menu_reactivar_cliente()
            elif opcion == '7':
                self.menu_ver_estadisticas()
            elif opcion == '8':
                self.menu_reporte_beneficios()
            elif opcion == '9':
                self.menu_ver_detalles()
            elif opcion == '0':
                self.salir()
                break
            else:
                print("\nOpcion invalida. Intente nuevamente.")
            
            input("\nPresione ENTER para continuar...")
    
    
    def menu_crear_cliente(self) -> None:
        """Menu para crear un nuevo cliente."""
        print("\n" + "-" * 70)
        print("CREAR NUEVO CLIENTE")
        print("-" * 70)
        
        print("\nTipo de cliente:")
        print("1. Cliente Regular")
        print("2. Cliente Premium")
        print("3. Cliente Corporativo")
        
        tipo_opcion = input("\nSeleccione tipo (1-3): ").strip()
        
        if tipo_opcion == '1':
            self._crear_cliente_regular()
        elif tipo_opcion == '2':
            self._crear_cliente_premium()
        elif tipo_opcion == '3':
            self._crear_cliente_corporativo()
        else:
            print("\nTipo invalido.")
    
    
    def _crear_cliente_regular(self) -> None:
        try:
            print("\n--- DATOS DEL CLIENTE REGULAR ---")
            
            nombre = input("Nombre completo: ").strip()
            email = input("Email: ").strip()
            
            print("\nTelefono (formato internacional con codigo de pais)")
            print("Ejemplos: +56912345678 (Chile), +5491112345678 (Argentina)")
            telefono = input("Telefono: ").strip()
            
            direccion = input("Direccion: ").strip()
            ciudad = input("Ciudad: ").strip()
            
            nivel_sat = input("Nivel de satisfaccion (1-5) [default: 3]: ").strip()
            nivel_satisfaccion = int(nivel_sat) if nivel_sat else 3
            
            cliente = self.gestor.crear_cliente(
                'regular',
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion,
                ciudad=ciudad,
                nivel_satisfaccion=nivel_satisfaccion
            )
            
            print("\n" + "=" * 70)
            print("CLIENTE CREADO EXITOSAMENTE")
            print("=" * 70)
            print(cliente)
            
        except (EmailDuplicadoError, TelefonoDuplicadoError) as e:
            print(f"\nError: {e}")
        except ValidacionError as e:
            print(f"\nError de validacion: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
    
    
    def _crear_cliente_premium(self) -> None:
        try:
            print("\n--- DATOS DEL CLIENTE PREMIUM ---")
            
            nombre = input("Nombre completo: ").strip()
            email = input("Email: ").strip()
            
            print("\nTelefono (formato internacional con codigo de pais)")
            print("Ejemplos: +56912345678 (Chile), +5491112345678 (Argentina)")
            telefono = input("Telefono: ").strip()
            
            direccion = input("Direccion: ").strip()
            ciudad = input("Ciudad: ").strip()
            
            descuento_str = input("Descuento (0.0-1.0) [default: 0.10]: ").strip()
            descuento = float(descuento_str) if descuento_str else 0.10
            
            puntos_str = input("Puntos acumulados [default: 0]: ").strip()
            puntos_acumulados = int(puntos_str) if puntos_str else 0
            
            cliente = self.gestor.crear_cliente(
                'premium',
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion,
                ciudad=ciudad,
                descuento=descuento,
                puntos_acumulados=puntos_acumulados
            )
            
            print("\n" + "=" * 70)
            print("CLIENTE PREMIUM CREADO EXITOSAMENTE")
            print("=" * 70)
            print(cliente)
            
        except (EmailDuplicadoError, TelefonoDuplicadoError) as e:
            print(f"\nError: {e}")
        except ValidacionError as e:
            print(f"\nError de validacion: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
    
    
    def _crear_cliente_corporativo(self) -> None:
        try:
            print("\n--- DATOS DEL CLIENTE CORPORATIVO ---")
            
            nombre = input("Nombre de la empresa: ").strip()
            email = input("Email corporativo: ").strip()
            
            print("\nTelefono corporativo (formato internacional con codigo de pais)")
            print("Ejemplos: +562234567890 (Chile fijo), +541143216789 (Argentina fijo)")
            telefono = input("Telefono: ").strip()
            
            direccion = input("Direccion: ").strip()
            ciudad = input("Ciudad: ").strip()
            
            razon_social = input("Razon social: ").strip()
            rut_empresa = input("RUT/DNI empresa: ").strip()
            
            pais_empresa = input("Pais (CHILE/ARGENTINA/BRASIL/PERU/COLOMBIA/URUGUAY) [default: CHILE]: ").strip().upper()
            if not pais_empresa:
                pais_empresa = "CHILE"
            
            contacto_principal = input("Contacto principal: ").strip()
            
            descuento_str = input("Descuento por volumen (0.0-1.0) [default: 0.05]: ").strip()
            descuento_volumen = float(descuento_str) if descuento_str else 0.05
            
            empleados_str = input("Numero de empleados [default: 1]: ").strip()
            numero_empleados = int(empleados_str) if empleados_str else 1
            
            cliente = self.gestor.crear_cliente(
                'corporativo',
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion,
                ciudad=ciudad,
                razon_social=razon_social,
                rut_empresa=rut_empresa,
                pais_empresa=pais_empresa,
                contacto_principal=contacto_principal,
                descuento_volumen=descuento_volumen,
                numero_empleados=numero_empleados
            )
            
            print("\n" + "=" * 70)
            print("CLIENTE CORPORATIVO CREADO EXITOSAMENTE")
            print("=" * 70)
            print(cliente)
            
        except (EmailDuplicadoError, TelefonoDuplicadoError) as e:
            print(f"\nError: {e}")
        except ValidacionError as e:
            print(f"\nError de validacion: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
    
    
    def menu_listar_clientes(self) -> None:
        print("\n" + "-" * 70)
        print("LISTAR CLIENTES")
        print("-" * 70)
        
        print("\nFiltrar por estado:")
        print("1. Solo activos")
        print("2. Solo inactivos")
        print("3. Todos")
        
        filtro_estado = input("\nSeleccione opcion (1-3): ").strip()
        
        if filtro_estado == '1':
            activos = True
        elif filtro_estado == '2':
            activos = False
        else:
            activos = None
        
        print("\nFiltrar por tipo:")
        print("1. Regular")
        print("2. Premium")
        print("3. Corporativo")
        print("4. Todos")
        
        filtro_tipo = input("\nSeleccione opcion (1-4): ").strip()
        
        tipo = None
        if filtro_tipo == '1':
            tipo = 'regular'
        elif filtro_tipo == '2':
            tipo = 'premium'
        elif filtro_tipo == '3':
            tipo = 'corporativo'
        
        clientes = self.gestor.listar_clientes(activos=activos, tipo=tipo)
        
        if not clientes:
            print("\nNo se encontraron clientes con esos filtros.")
            return
        
        print("\n" + "=" * 70)
        print(f"CLIENTES ENCONTRADOS: {len(clientes)}")
        print("=" * 70)
        
        for i, cliente in enumerate(clientes, 1):
            estado = "Activo" if cliente.activo else "Inactivo"
            print(f"\n{i}. {cliente.nombre}")
            print(f"   ID: {cliente.id_cliente[:8]}...")
            print(f"   Tipo: {cliente.tipo_cliente}")
            print(f"   Email: {cliente.email}")
            print(f"   Ciudad: {cliente.ciudad}")
            print(f"   Estado: {estado}")
            print(f"   Beneficio: ${cliente.calcular_beneficio():,.2f}")
    
    
    def menu_buscar_cliente(self) -> None:
        print("\n" + "-" * 70)
        print("BUSCAR CLIENTE")
        print("-" * 70)
        
        print("\nBuscar por:")
        print("1. ID")
        print("2. Email")
        print("3. Telefono")
        
        criterio_opcion = input("\nSeleccione criterio (1-3): ").strip()
        
        if criterio_opcion == '1':
            criterio = 'id'
            valor = input("\nIngrese el ID: ").strip()
        elif criterio_opcion == '2':
            criterio = 'email'
            valor = input("\nIngrese el email: ").strip()
        elif criterio_opcion == '3':
            criterio = 'telefono'
            valor = input("\nIngrese el telefono: ").strip()
        else:
            print("\nCriterio invalido.")
            return
        
        cliente = self.gestor.buscar_cliente(criterio, valor, incluir_inactivos=True)
        
        if cliente:
            print("\n" + "=" * 70)
            print("CLIENTE ENCONTRADO")
            print("=" * 70)
            print(cliente)
        else:
            print("\nCliente no encontrado.")
    
    
    def menu_actualizar_cliente(self) -> None:
        print("\n" + "-" * 70)
        print("ACTUALIZAR CLIENTE")
        print("-" * 70)
        
        id_cliente = input("\nIngrese el ID del cliente: ").strip()
        
        try:
            cliente = self.gestor.obtener_cliente_por_id(id_cliente)
            
            print("\n--- CLIENTE ACTUAL ---")
            print(cliente)
            
            print("\n--- NUEVOS DATOS (dejar vacio para mantener) ---")
            
            cambios = {}
            
            nuevo_nombre = input(f"Nombre [{cliente.nombre}]: ").strip()
            if nuevo_nombre:
                cambios['nombre'] = nuevo_nombre
            
            nuevo_email = input(f"Email [{cliente.email}]: ").strip()
            if nuevo_email:
                cambios['email'] = nuevo_email
            
            nuevo_telefono = input(f"Telefono [{cliente.telefono}]: ").strip()
            if nuevo_telefono:
                cambios['telefono'] = nuevo_telefono
            
            nueva_direccion = input(f"Direccion [{cliente.direccion}]: ").strip()
            if nueva_direccion:
                cambios['direccion'] = nueva_direccion
            
            nueva_ciudad = input(f"Ciudad [{cliente.ciudad}]: ").strip()
            if nueva_ciudad:
                cambios['ciudad'] = nueva_ciudad
            
            if isinstance(cliente, ClientePremium):
                nuevos_puntos = input(f"Puntos [{cliente.puntos_acumulados}]: ").strip()
                if nuevos_puntos:
                    cambios['puntos_acumulados'] = int(nuevos_puntos)
            
            elif isinstance(cliente, ClienteCorporativo):
                nuevos_empleados = input(f"Empleados [{cliente.numero_empleados}]: ").strip()
                if nuevos_empleados:
                    cambios['numero_empleados'] = int(nuevos_empleados)
            
            if not cambios:
                print("\nNo se realizaron cambios.")
                return
            
            self.gestor.actualizar_cliente(id_cliente, **cambios)
            
            print("\n" + "=" * 70)
            print("CLIENTE ACTUALIZADO EXITOSAMENTE")
            print("=" * 70)
            
            cliente_actualizado = self.gestor.obtener_cliente_por_id(id_cliente)
            print(cliente_actualizado)
            
        except ClienteNoEncontradoError as e:
            print(f"\nError: {e}")
        except (EmailDuplicadoError, TelefonoDuplicadoError) as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
    
    
    def menu_eliminar_cliente(self) -> None:
        print("\n" + "-" * 70)
        print("ELIMINAR CLIENTE")
        print("-" * 70)
        
        id_cliente = input("\nIngrese el ID del cliente: ").strip()
        
        try:
            cliente = self.gestor.obtener_cliente_por_id(id_cliente)
            
            print("\n--- CLIENTE A ELIMINAR ---")
            print(f"Nombre: {cliente.nombre}")
            print(f"Email: {cliente.email}")
            print(f"Tipo: {cliente.tipo_cliente}")
            
            confirmacion = input("\nEsta seguro de eliminar este cliente? (S/N): ").strip().upper()
            
            if confirmacion == 'S':
                self.gestor.eliminar_cliente(id_cliente)
                print("\nCliente eliminado exitosamente.")
            else:
                print("\nOperacion cancelada.")
            
        except ClienteNoEncontradoError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
    
    
    def menu_reactivar_cliente(self) -> None:
        print("\n" + "-" * 70)
        print("REACTIVAR CLIENTE")
        print("-" * 70)
        
        id_cliente = input("\nIngrese el ID del cliente: ").strip()
        
        try:
            cliente = self.gestor.obtener_cliente_por_id(id_cliente)
            
            if cliente.activo:
                print("\nEste cliente ya esta activo.")
                return
            
            print("\n--- CLIENTE A REACTIVAR ---")
            print(f"Nombre: {cliente.nombre}")
            print(f"Email: {cliente.email}")
            print(f"Tipo: {cliente.tipo_cliente}")
            
            confirmacion = input("\nEsta seguro de reactivar este cliente? (S/N): ").strip().upper()
            
            if confirmacion == 'S':
                self.gestor.reactivar_cliente(id_cliente)
                print("\nCliente reactivado exitosamente.")
            else:
                print("\nOperacion cancelada.")
            
        except ClienteNoEncontradoError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
    
    
    def menu_ver_estadisticas(self) -> None:
        print("\n" + "-" * 70)
        print("ESTADISTICAS DEL SISTEMA")
        print("-" * 70)
        
        stats = self.gestor.obtener_estadisticas()
        
        print("\n" + "=" * 70)
        print("RESUMEN GENERAL")
        print("=" * 70)
        print(f"Total de clientes:        {stats['total_clientes']}")
        print(f"Clientes activos:         {stats['clientes_activos']}")
        print(f"Clientes inactivos:       {stats['clientes_inactivos']}")
        
        print("\n" + "=" * 70)
        print("POR TIPO DE CLIENTE")
        print("=" * 70)
        print(f"Clientes Regulares:       {stats['por_tipo']['regular']}")
        print(f"Clientes Premium:         {stats['por_tipo']['premium']}")
        print(f"Clientes Corporativos:    {stats['por_tipo']['corporativo']}")
        
        print("\n" + "=" * 70)
        print("BENEFICIOS")
        print("=" * 70)
        print(f"Beneficios totales:       ${stats['beneficios_totales']:,.2f}")
    
    
    def menu_reporte_beneficios(self) -> None:
        print("\n" + "-" * 70)
        print("REPORTE DE BENEFICIOS POR CLIENTE")
        print("-" * 70)
        
        reporte = self.gestor.generar_reporte_beneficios()
        
        if not reporte:
            print("\nNo hay clientes activos para generar reporte.")
            return
        
        print("\n" + "=" * 70)
        print(f"{'CLIENTE':<30} {'TIPO':<20} {'BENEFICIO':>15}")
        print("=" * 70)
        
        for item in reporte:
            nombre = item['nombre'][:28]
            tipo = item['tipo'].replace('Cliente', '')
            beneficio = item['beneficio']
            
            print(f"{nombre:<30} {tipo:<20} ${beneficio:>14,.2f}")
        
        total = sum(item['beneficio'] for item in reporte)
        print("=" * 70)
        print(f"{'TOTAL':<30} {'':<20} ${total:>14,.2f}")
        print("=" * 70)
    
    
    def menu_ver_detalles(self) -> None:
        print("\n" + "-" * 70)
        print("VER DETALLES DE CLIENTE")
        print("-" * 70)
        
        id_cliente = input("\nIngrese el ID del cliente: ").strip()
        
        try:
            cliente = self.gestor.obtener_cliente_por_id(id_cliente)
            
            print("\n" + "=" * 70)
            print("DETALLES COMPLETOS DEL CLIENTE")
            print("=" * 70)
            print(cliente)
            
            print("\n" + "=" * 70)
            print("INFORMACION ADICIONAL")
            print("=" * 70)
            print(f"Beneficio economico:      ${cliente.calcular_beneficio():,.2f}")
            print(f"Fecha de registro:        {cliente.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')}")
            
        except ClienteNoEncontradoError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
    
    
    def salir(self) -> None:
        print("\n" + "=" * 70)
        print("CERRANDO SISTEMA")
        print("=" * 70)
        
        try:
            self.gestor.cerrar()
            print("Datos guardados correctamente.")
            print("Hasta pronto!")
            print("=" * 70 + "\n")
        except Exception as e:
            print(f"Error al cerrar el sistema: {e}")


def iniciar_menu():
    try:
        menu = MenuConsola()
        menu.mostrar_menu_principal()
    except KeyboardInterrupt:
        print("\n\nSistema interrumpido por el usuario.")
        print("Hasta pronto!\n")
    except Exception as e:
        print(f"\n\nError critico: {e}")
        print("El sistema se cerrara.\n")


if __name__ == "__main__":
    iniciar_menu()


