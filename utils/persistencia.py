# -*- coding: utf-8 -*-

import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from modelos.excepciones import (
    PersistenciaError,
    ArchivoNoEncontradoError,
    JSONCorruptoError,
    ErrorEscrituraError
)

class PersistenciaJSON:
    ESTRUCTURA_BASE = {
        'metadata': {
            'version': '1.0',
            'ultima_actualizacion': None,
            'total_clientes': 0
        },
        'clientes': []
    }
    
    def __init__(self, ruta_archivo: str = "data/clientes.json", auto_respaldo: bool = True):
        self.ruta_archivo = ruta_archivo
        self.auto_respaldo = auto_respaldo
        
        # Crear carpeta de respaldos
        carpeta_archivo = Path(ruta_archivo).parent
        self.ruta_respaldo = carpeta_archivo / "respaldos"
        
        # Asegurar que existen las carpetas necesarias
        self._crear_estructura_carpetas()
        
        # Crear archivo inicial si no existe
        if not os.path.exists(self.ruta_archivo):
            self._crear_archivo_inicial()
    
    # INICIALIZACIÓN Y ESTRUCTURA
    
    def _crear_estructura_carpetas(self) -> None:
        try:
            carpeta_data = Path(self.ruta_archivo).parent
            carpeta_data.mkdir(parents=True, exist_ok=True)
            self.ruta_respaldo.mkdir(parents=True, exist_ok=True)
            
        except Exception as e:
            raise PersistenciaError(
                f"No se pudo crear la estructura de carpetas: {e}"
            )
    
    
    def _crear_archivo_inicial(self) -> None:
        try:
            estructura_inicial = self.ESTRUCTURA_BASE.copy()
            estructura_inicial['metadata']['ultima_actualizacion'] = datetime.now().isoformat()
            
            with open(self.ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(estructura_inicial, archivo, ensure_ascii=False, indent=2)
                
            print(f"✓ Archivo inicial creado: {self.ruta_archivo}")
            
        except Exception as e:
            raise ErrorEscrituraError(self.ruta_archivo, str(e))
    
    # LECTURA DE DATOS
    
    def cargar(self) -> Dict[str, Any]:
        if not os.path.exists(self.ruta_archivo):
            raise ArchivoNoEncontradoError(self.ruta_archivo)
        
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            self._validar_estructura(datos)
            
            return datos
            
        except json.JSONDecodeError as e:
            print(f"⚠ Archivo JSON corrupto: {e}")
            return self._intentar_recuperacion()
            
        except Exception as e:
            raise PersistenciaError(f"Error al cargar datos: {e}")
    
    
    def cargar_clientes(self) -> List[Dict[str, Any]]:
        datos = self.cargar()
        return datos.get('clientes', [])
    
    def guardar(self, clientes: List[Dict[str, Any]]) -> bool:
        try:
            if self.auto_respaldo and os.path.exists(self.ruta_archivo):
                self.crear_respaldo()
            
            datos = {
                'metadata': {
                    'version': '1.0',
                    'ultima_actualizacion': datetime.now().isoformat(),
                    'total_clientes': len(clientes)
                },
                'clientes': clientes
            }
            
            with open(self.ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            raise ErrorEscrituraError(self.ruta_archivo, str(e))

    # RESPALDOS

    def crear_respaldo(self) -> Optional[str]:
        if not os.path.exists(self.ruta_archivo):
            return None   
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_respaldo = f"clientes_backup_{timestamp}.json"
            ruta_respaldo_completa = self.ruta_respaldo / nombre_respaldo
            
            shutil.copy2(self.ruta_archivo, ruta_respaldo_completa)
            
            self._limpiar_respaldos_antiguos(max_respaldos=10)
            
            return str(ruta_respaldo_completa)
            
        except Exception as e:
            print(f"⚠ No se pudo crear respaldo: {e}")
            return None
    
    
    def _limpiar_respaldos_antiguos(self, max_respaldos: int = 10) -> None:
        try:
            respaldos = sorted(
                self.ruta_respaldo.glob("clientes_backup_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            
            for respaldo in respaldos[max_respaldos:]:
                respaldo.unlink()
                
        except Exception as e:
            print(f"⚠ Error al limpiar respaldos: {e}")
    
    
    def listar_respaldos(self) -> List[Dict[str, Any]]:
        respaldos = []        
        try:
            for archivo in sorted(
                self.ruta_respaldo.glob("clientes_backup_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            ):
                stat = archivo.stat()
                respaldos.append({
                    'nombre': archivo.name,
                    'ruta': str(archivo),
                    'fecha': datetime.fromtimestamp(stat.st_mtime),
                    'tamano': stat.st_size
                })
                
        except Exception as e:
            print(f"⚠ Error al listar respaldos: {e}")
        
        return respaldos
       
    def restaurar_respaldo(self, nombre_respaldo: str) -> bool:
        try:
            ruta_respaldo_completa = self.ruta_respaldo / nombre_respaldo
            
            if not ruta_respaldo_completa.exists():
                raise ArchivoNoEncontradoError(str(ruta_respaldo_completa))
            self.crear_respaldo()
            shutil.copy2(ruta_respaldo_completa, self.ruta_archivo)          
            print(f"✓ Respaldo restaurado: {nombre_respaldo}")
            return True
            
        except Exception as e:
            print(f"Error al restaurar respaldo: {e}")
            return False
    
    # VALIDACIÓN Y RECUPERACIÓN
    
    def _validar_estructura(self, datos: Dict[str, Any]) -> bool:
        if 'metadata' not in datos or 'clientes' not in datos:
            raise JSONCorruptoError(
                self.ruta_archivo,
                "Faltan las claves 'metadata' o 'clientes'"
            )
        if not isinstance(datos['clientes'], list):
            raise JSONCorruptoError(
                self.ruta_archivo,
                "'clientes' debe ser una lista"
            )
        
        return True
    
    
    def _intentar_recuperacion(self) -> Dict[str, Any]:
        print("Intentando recuperar desde respaldo...")
        
        respaldos = self.listar_respaldos()
        
        if not respaldos:
            print("⚠ No hay respaldos disponibles. Creando archivo nuevo.")
            return self.ESTRUCTURA_BASE.copy()

        respaldo_reciente = respaldos[0]
        
        try:
            with open(respaldo_reciente['ruta'], 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            self._validar_estructura(datos)
            
            print(f"✓ Datos recuperados desde: {respaldo_reciente['nombre']}")
            
            shutil.copy2(respaldo_reciente['ruta'], self.ruta_archivo)
            
            return datos
            
        except Exception as e:
            print(f"No se pudo recuperar: {e}")
            return self.ESTRUCTURA_BASE.copy()
    
    
    def validar_archivo(self) -> bool:
        try:
            datos = self.cargar()
            return True
        except Exception as e:
            print(f"Archivo inválido: {e}")
            return False

    # UTILIDADES
 
    def obtener_metadata(self) -> Dict[str, Any]:
        try:
            datos = self.cargar()
            return datos.get('metadata', {})
        except Exception:
            return {}
    
    
    def obtener_estadisticas_archivo(self) -> Dict[str, Any]:
        stats = {
            'existe': os.path.exists(self.ruta_archivo),
            'ruta': self.ruta_archivo,
            'tamano': 0,
            'total_clientes': 0,
            'ultima_modificacion': None,
            'respaldos_disponibles': len(self.listar_respaldos())
        }
        
        if stats['existe']:
            try:
                stat_archivo = os.stat(self.ruta_archivo)
                stats['tamano'] = stat_archivo.st_size
                stats['ultima_modificacion'] = datetime.fromtimestamp(
                    stat_archivo.st_mtime
                )
                
                datos = self.cargar()
                stats['total_clientes'] = len(datos.get('clientes', []))
                
            except Exception:
                pass
        
        return stats



