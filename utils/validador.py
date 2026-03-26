import re
from datetime import datetime
from typing import Optional
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from modelos.excepciones import (
    EmailInvalidoError,
    TelefonoInvalidoError,
    DireccionInvalidaError,
    CiudadInvalidaError,
    RUTInvalidoError,
    DescuentoInvalidoError,
    FechaVencimientoInvalidaError,
    NumeroEmpleadosInvalidoError
)


class ValidadorDatos:

    # EXPRESIONES REGULARES


    # Email: formato usuario@dominio.ext
    REGEX_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Teléfono sudamericano: +XX XXXXXXXXX (con espacios opcionales)
# Acepta: +56912345678, +56 9 1234 5678, +5491112345678, +54 9 11 1234 5678
    REGEX_TELEFONO = r'^\+\d{1,3}[\s]?\d{1,4}[\s]?\d{1,4}[\s]?\d{2,4}[\s]?\d{0,4}[\s]?\d{0,4}$'




    # RUT/DNI por país 
    REGEX_RUT_CHILE = r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$'
    REGEX_DNI_ARGENTINA = r'^\d{7,8}$'  # 7-8 dígitos
    REGEX_CPF_BRASIL = r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'  # 123.456.789-01
    REGEX_DNI_PERU = r'^\d{8}$'  # 8 dígitos
    REGEX_CEDULA_COLOMBIA = r'^\d{6,10}$'  # 6-10 dígitos
    REGEX_CI_URUGUAY = r'^\d{1}\.?\d{3}\.?\d{3}-?\d{1}$'  # 1.234.567-8

    # Ciudad: solo letras, espacios y acentos (mínimo 3 caracteres)
    REGEX_CIUDAD = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{3,}$'

    # VALIDACIÓN DE EMAIL

    @staticmethod
    def validar_email(email: str) -> str:
        if not email or not isinstance(email, str):
            raise EmailInvalidoError(email)

        email = email.strip().lower()

        if not re.match(ValidadorDatos.REGEX_EMAIL, email):
            raise EmailInvalidoError(email)

        return email

    # VALIDACIÓN DE TELÉFONO

    @staticmethod
    def validar_telefono(telefono: str) -> str:
        if not telefono or not isinstance(telefono, str):
            raise TelefonoInvalidoError(telefono)

        telefono = telefono.strip()

        telefono = re.sub(r'\s+', ' ', telefono)

        if not re.match(ValidadorDatos.REGEX_TELEFONO, telefono):
            raise TelefonoInvalidoError(telefono)

        return telefono

    # VALIDACIÓN DE DIRECCIÓN

    @staticmethod
    def validar_direccion(direccion: str) -> str:
        if not direccion or not isinstance(direccion, str):
            raise DireccionInvalidaError(direccion)

        direccion = direccion.strip()

        if len(direccion) < 10:
            raise DireccionInvalidaError(direccion)

        return direccion

    # VALIDACIÓN DE CIUDAD

    @staticmethod
    def validar_ciudad(ciudad: str) -> str:
        if not ciudad or not isinstance(ciudad, str):
            raise CiudadInvalidaError(ciudad)

        ciudad = ciudad.strip()

        if not re.match(ValidadorDatos.REGEX_CIUDAD, ciudad):
            raise CiudadInvalidaError(ciudad)

        return ciudad

    # VALIDACIÓN DE RUT/DNI 

    @staticmethod
    def validar_rut_dni(documento: str, pais: str = "CHILE") -> str:
        if not documento or not isinstance(documento, str):
            raise RUTInvalidoError(documento)

        documento = documento.strip().upper()
        pais = pais.strip().upper()

        if pais == "CHILE":
            return ValidadorDatos._validar_rut_chile(documento)

        elif pais == "ARGENTINA":
            return ValidadorDatos._validar_dni_argentina(documento)

        elif pais == "BRASIL" or pais == "BRAZIL":
            return ValidadorDatos._validar_cpf_brasil(documento)

        elif pais == "PERU" or pais == "PERÚ":
            return ValidadorDatos._validar_dni_peru(documento)

        elif pais == "COLOMBIA":
            return ValidadorDatos._validar_cedula_colombia(documento)

        elif pais == "URUGUAY":
            return ValidadorDatos._validar_ci_uruguay(documento)

        else:
            raise RUTInvalidoError(f"País no soportado: {pais}")

    @staticmethod
    def _validar_rut_chile(rut: str) -> str:
        if not re.match(ValidadorDatos.REGEX_RUT_CHILE, rut):
            raise RUTInvalidoError(f"RUT chileno inválido: {rut}")
        rut_limpio = rut.replace('.', '').replace('-', '')
        cuerpo = rut_limpio[:-1]
        dv = rut_limpio[-1]
        if len(cuerpo) >= 7:
            rut_formateado = f"{cuerpo[:-6]}.{cuerpo[-6:-3]}.{cuerpo[-3:]}-{dv}"
        else:
            rut_formateado = f"{cuerpo}-{dv}"

        return rut_formateado

    @staticmethod
    def _validar_dni_argentina(dni: str) -> str:
        dni_limpio = dni.replace('.', '').replace('-', '')
        if not re.match(ValidadorDatos.REGEX_DNI_ARGENTINA, dni_limpio):
            raise RUTInvalidoError(f"DNI argentino inválido: {dni}")
        if len(dni_limpio) == 8:
            return f"{dni_limpio[0:2]}.{dni_limpio[2:5]}.{dni_limpio[5:8]}"
        else: 
            return f"{dni_limpio[0:1]}.{dni_limpio[1:4]}.{dni_limpio[4:7]}"

    @staticmethod
    def _validar_cpf_brasil(cpf: str) -> str:
        cpf_limpio = cpf.replace('.', '').replace('-', '')

        if not re.match(ValidadorDatos.REGEX_CPF_BRASIL, cpf.replace('.', '').replace('-', '')):
            raise RUTInvalidoError(f"CPF brasileño inválido: {cpf}")
        return f"{cpf_limpio[0:3]}.{cpf_limpio[3:6]}.{cpf_limpio[6:9]}-{cpf_limpio[9:11]}"

    @staticmethod
    def _validar_dni_peru(dni: str) -> str:
        dni_limpio = dni.replace('.', '').replace('-', '')

        if not re.match(ValidadorDatos.REGEX_DNI_PERU, dni_limpio):
            raise RUTInvalidoError(f"DNI peruano inválido: {dni}")

        return dni_limpio

    @staticmethod
    def _validar_cedula_colombia(cedula: str) -> str:
        cedula_limpia = cedula.replace('.', '').replace('-', '')

        if not re.match(ValidadorDatos.REGEX_CEDULA_COLOMBIA, cedula_limpia):
            raise RUTInvalidoError(f"Cédula colombiana inválida: {cedula}")

        return cedula_limpia

    @staticmethod
    def _validar_ci_uruguay(ci: str) -> str:

        ci_limpia = ci.replace('.', '').replace('-', '')

        if not re.match(ValidadorDatos.REGEX_CI_URUGUAY, ci.replace('.', '').replace('-', '')):
            raise RUTInvalidoError(f"CI uruguaya inválida: {ci}")

        if len(ci_limpia) == 8:
            return f"{ci_limpia[0]}.{ci_limpia[1:4]}.{ci_limpia[4:7]}-{ci_limpia[7]}"
        else:
            return ci_limpia

    @staticmethod
    def validar_rut(rut: str) -> str:
        return ValidadorDatos.validar_rut_dni(rut, "CHILE")

    # VALIDACIÓN DE NOMBRE

    @staticmethod
    def validar_nombre(nombre: str) -> str:
        if not nombre or not isinstance(nombre, str):
            raise ValueError("El nombre no puede estar vacío")

        nombre = nombre.strip()

        if len(nombre) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")

        return nombre

    # VALIDACIONES ESPECÍFICAS DE CLIENTE PREMIUM

    @staticmethod
    def validar_descuento(descuento: float) -> float:
        try:
            descuento = float(descuento)
        except (ValueError, TypeError):
            raise DescuentoInvalidoError(descuento)

        if not (0.0 <= descuento <= 1.0):
            raise DescuentoInvalidoError(descuento)

        return descuento


    @staticmethod
    def validar_fecha_vencimiento(fecha: datetime) -> datetime:
        if not isinstance(fecha, datetime):
            raise FechaVencimientoInvalidaError(fecha)

        if fecha <= datetime.now():
            raise FechaVencimientoInvalidaError(fecha.strftime('%Y-%m-%d'))

        return fecha


    @staticmethod
    def validar_puntos(puntos: int) -> int:
        try:
            puntos = int(puntos)
        except (ValueError, TypeError):
            raise ValueError(f"Puntos inválidos: {puntos}. Debe ser un número entero.")

        if puntos < 0:
            raise ValueError("Los puntos no pueden ser negativos")

        return puntos

    # VALIDACIONES ESPECÍFICAS DE CLIENTE CORPORATIVO

    @staticmethod
    def validar_numero_empleados(numero: int) -> int:
        try:
            numero = int(numero)
        except (ValueError, TypeError):
            raise NumeroEmpleadosInvalidoError(numero)

        if numero <= 0:
            raise NumeroEmpleadosInvalidoError(numero)

        return numero



