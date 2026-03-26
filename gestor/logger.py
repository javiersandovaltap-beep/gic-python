 # -*- coding: utf-8 -*-

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
import os


class LoggerSistema:
    def __init__(
        self,
        nombre_logger: str = "GIC",
        ruta_log: str = "logs/sistema.log",
        nivel_log: int = logging.INFO,
        mostrar_consola: bool = False
    ):

        self.nombre_logger = nombre_logger
        self.ruta_log = ruta_log
        self.nivel_log = nivel_log
        self.mostrar_consola = mostrar_consola
        self._crear_carpeta_logs()
        self.logger = self._configurar_logger()

    # CONFIGURACION INICIAL
   
    def _crear_carpeta_logs(self) -> None:
        carpeta_logs = Path(self.ruta_log).parent
        carpeta_logs.mkdir(parents=True, exist_ok=True)
      
    def _configurar_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.nombre_logger)
        logger.setLevel(self.nivel_log)
        
        if logger.handlers:
            logger.handlers.clear()
        
        formato = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler = logging.FileHandler(
            self.ruta_log,
            encoding='utf-8',
            mode='a'  # Append mode
        )
        file_handler.setLevel(self.nivel_log)
        file_handler.setFormatter(formato)
        logger.addHandler(file_handler)
        
        if self.mostrar_consola:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.nivel_log)
            console_handler.setFormatter(formato)
            logger.addHandler(console_handler)
        
        return logger

    # METODOS DE LOGGING POR NIVEL
    
    def info(self, mensaje: str) -> None:
        self.logger.info(mensaje)
        
    def warning(self, mensaje: str) -> None:
        self.logger.warning(mensaje)
    
    def error(self, mensaje: str, excepcion: Optional[Exception] = None) -> None:
        if excepcion:
            self.logger.error(f"{mensaje} | Excepcion: {type(excepcion).__name__}: {excepcion}")
        else:
            self.logger.error(mensaje)
    
    
    def critical(self, mensaje: str) -> None:
        self.logger.critical(mensaje)
 
    # METODOS ESPECIFICOS PARA OPERACIONES GIC
    
    def log_inicio_sistema(self) -> None:
        self.info("=" * 60)
        self.info("SISTEMA GIC INICIADO")
        self.info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.info("=" * 60)
    
    
    def log_cierre_sistema(self) -> None:
        self.info("=" * 60)
        self.info("SISTEMA GIC CERRADO")
        self.info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.info("=" * 60)
    
    
    def log_cliente_creado(self, id_cliente: str, tipo: str, nombre: str) -> None:
        self.info(f"Cliente creado | ID: {id_cliente} | Tipo: {tipo} | Nombre: {nombre}")
       
    def log_cliente_actualizado(self, id_cliente: str, campos: list) -> None:
        campos_str = ", ".join(campos)
        self.info(f"Cliente actualizado | ID: {id_cliente} | Campos: {campos_str}")
       
    def log_cliente_eliminado(self, id_cliente: str, nombre: str) -> None:
        self.info(f"Cliente eliminado | ID: {id_cliente} | Nombre: {nombre}")
       
    def log_cliente_reactivado(self, id_cliente: str, nombre: str) -> None:
        self.info(f"Cliente reactivado | ID: {id_cliente} | Nombre: {nombre}")
       
    def log_busqueda(self, criterio: str, valor: str, encontrado: bool) -> None:
        estado = "encontrado" if encontrado else "no encontrado"
        self.info(f"Busqueda | Criterio: {criterio} | Valor: {valor} | Estado: {estado}")
       
    def log_exportacion(self, formato: str, cantidad: int) -> None:
        self.info(f"Exportacion | Formato: {formato} | Clientes: {cantidad}")
       
    def log_importacion(self, formato: str, cantidad: int, exitosos: int, fallidos: int) -> None:
        self.info(
            f"Importacion | Formato: {formato} | Total: {cantidad} | "
            f"Exitosos: {exitosos} | Fallidos: {fallidos}"
        )
      
    def log_error_validacion(self, campo: str, valor: str, motivo: str) -> None:
        self.warning(f"Validacion fallida | Campo: {campo} | Valor: {valor} | Motivo: {motivo}")
       
    def log_error_persistencia(self, operacion: str, detalle: str) -> None:
        self.error(f"Error de persistencia | Operacion: {operacion} | Detalle: {detalle}")

    # UTILIDADES
    
    def limpiar_logs_antiguos(self, dias: int = 30) -> int:
        try:
            if not os.path.exists(self.ruta_log):
                return 0
            
            fecha_limite = datetime.now().timestamp() - (dias * 24 * 60 * 60)
            
            with open(self.ruta_log, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
            
            lineas_nuevas = []
            lineas_eliminadas = 0
            
            for linea in lineas:
                try:
                    fecha_str = linea.split('|')[0].strip()
                    fecha_log = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                    
                    if fecha_log.timestamp() >= fecha_limite:
                        lineas_nuevas.append(linea)
                    else:
                        lineas_eliminadas += 1
                        
                except Exception:
                    lineas_nuevas.append(linea)
            
            with open(self.ruta_log, 'w', encoding='utf-8') as f:
                f.writelines(lineas_nuevas)
            
            self.info(f"Limpieza de logs | Lineas eliminadas: {lineas_eliminadas}")
            return lineas_eliminadas
            
        except Exception as e:
            self.error(f"Error al limpiar logs", e)
            return 0
    
    
    def obtener_estadisticas_log(self) -> dict:
        stats = {
            'existe': os.path.exists(self.ruta_log),
            'ruta': self.ruta_log,
            'tamano': 0,
            'total_lineas': 0,
            'info': 0,
            'warning': 0,
            'error': 0,
            'critical': 0
        }
        
        if not stats['existe']:
            return stats
        
        try:
            stats['tamano'] = os.path.getsize(self.ruta_log)
            
            with open(self.ruta_log, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
                stats['total_lineas'] = len(lineas)
                
                for linea in lineas:
                    if '| INFO' in linea:
                        stats['info'] += 1
                    elif '| WARNING' in linea:
                        stats['warning'] += 1
                    elif '| ERROR' in linea:
                        stats['error'] += 1
                    elif '| CRITICAL' in linea:
                        stats['critical'] += 1
        
        except Exception:
            pass
        
        return stats
    
    
    def ver_ultimas_lineas(self, n: int = 20) -> list:
        try:
            if not os.path.exists(self.ruta_log):
                return []
            
            with open(self.ruta_log, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
            
            return lineas[-n:]
            
        except Exception as e:
            return [f"Error al leer log: {e}"]

