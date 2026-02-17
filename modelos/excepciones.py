class ErrorGestionClientes(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self):
        return f"[ERROR GIC] {self.mensaje}"

# EXCEPCIONES DE VALIDACIÓN
class ValidacionError(ErrorGestionClientes):
    """Error base para todas las validaciones de datos."""
    pass

class EmailInvalidoError(ValidacionError):
    """Email no cumple con el formato requerido."""
    def __init__(self, email):
        super().__init__(f"Email inválido: '{email}'. Debe contener '@' y un dominio válido.")

class EmailDuplicadoError(ValidacionError):
    """Email ya existe en la base de datos."""
    def __init__(self, email):
        super().__init__(f"El email '{email}' ya está registrado en el sistema.")

class TelefonoInvalidoError(ValidacionError):
    """Teléfono no cumple con el formato sudamericano."""
    def __init__(self, telefono):
        super().__init__(
            f"Teléfono inválido: '{telefono}'. "
            f"Formato requerido: +XX XXXXXXXXX (código de país + número)"
        )

class TelefonoDuplicadoError(ValidacionError):
    """Teléfono ya existe en la base de datos."""
    def __init__(self, telefono):
        super().__init__(f"El teléfono '{telefono}' ya está registrado en el sistema.")

class DireccionInvalidaError(ValidacionError):
    """Dirección no cumple con el largo mínimo."""
    def __init__(self, direccion):
        super().__init__(
            f"Dirección inválida: '{direccion}'. "
            f"Debe tener al menos 10 caracteres."
        )

class CiudadInvalidaError(ValidacionError):
    """Ciudad no cumple con los requisitos."""
    def __init__(self, ciudad):
        super().__init__(
            f"Ciudad inválida: '{ciudad}'. "
            f"Debe contener solo letras y tener al menos 3 caracteres."
        )

class RUTInvalidoError(ValidacionError):
    """RUT de empresa no cumple con el formato chileno."""
    def __init__(self, rut):
        super().__init__(
            f"RUT inválido: '{rut}'. "
            f"Formato esperado: 12.345.678-9"
        )

# EXCEPCIONES DE OPERACIONES CRUD

class OperacionCRUDError(ErrorGestionClientes):
    """Error base para operaciones CRUD."""
    pass

class ClienteNoEncontradoError(OperacionCRUDError):
    """Cliente no existe en el sistema."""
    def __init__(self, id_cliente):
        super().__init__(f"Cliente con ID '{id_cliente}' no encontrado.")

class ClienteInactivoError(OperacionCRUDError):
    """Intento de operar con un cliente marcado como inactivo."""
    def __init__(self, id_cliente):
        super().__init__(
            f"Cliente con ID '{id_cliente}' está inactivo. "
            f"Use la opción 'Reactivar' para habilitarlo."
        )

class DatosInsuficientesError(OperacionCRUDError):
    """Faltan datos obligatorios para crear/actualizar un cliente."""
    def __init__(self, campos_faltantes):
        super().__init__(
            f"Datos insuficientes. Campos requeridos: {', '.join(campos_faltantes)}"
        )

# EXCEPCIONES DE PERSISTENCIA

class PersistenciaError(ErrorGestionClientes):
    """Error base para operaciones de persistencia JSON."""
    pass

class ArchivoNoEncontradoError(PersistenciaError):
    """Archivo JSON no existe."""
    def __init__(self, ruta_archivo):
        super().__init__(f"Archivo no encontrado: '{ruta_archivo}'")

class JSONCorruptoError(PersistenciaError):
    """Archivo JSON tiene formato inválido."""
    def __init__(self, ruta_archivo, detalle):
        super().__init__(
            f"El archivo '{ruta_archivo}' está corrupto o tiene formato inválido. "
            f"Detalle: {detalle}"
        )

class ErrorEscrituraError(PersistenciaError):
    """No se pudo escribir en el archivo JSON."""
    def __init__(self, ruta_archivo, detalle):
        super().__init__(
            f"Error al escribir en '{ruta_archivo}'. "
            f"Detalle: {detalle}"
        )


# EXCEPCIONES DE REGLAS DE NEGOCIO

class ReglaNegocioError(ErrorGestionClientes):
    """Error base para violaciones de reglas de negocio."""
    pass


class DescuentoInvalidoError(ReglaNegocioError):
    """Descuento fuera del rango permitido."""
    def __init__(self, descuento):
        super().__init__(
            f"Descuento inválido: {descuento}. "
            f"Debe estar entre 0.0 y 1.0 (0% - 100%)"
        )


class FechaVencimientoInvalidaError(ReglaNegocioError):
    """Fecha de vencimiento Premium es anterior a hoy."""
    def __init__(self, fecha):
        super().__init__(
            f"Fecha de vencimiento inválida: {fecha}. "
            f"Debe ser posterior a la fecha actual."
        )

class NumeroEmpleadosInvalidoError(ReglaNegocioError):
    """Número de empleados no es válido para cliente corporativo."""
    def __init__(self, numero):
        super().__init__(
            f"Número de empleados inválido: {numero}. "
            f"Debe ser un entero positivo mayor a 0."
        )


# FUNCIÓN DE PRUEBA

def test_excepciones():
    """
    Función de prueba para verificar todas las excepciones.
    Ejecutar directamente este módulo para ver ejemplos.
    """
    print("=" * 60)
    print("PRUEBA DE EXCEPCIONES PERSONALIZADAS - GIC")
    print("=" * 60)
    
    excepciones_prueba = [
        EmailInvalidoError("usuario.com"),
        EmailDuplicadoError("juan@email.com"),
        TelefonoInvalidoError("123"),
        TelefonoDuplicadoError("+56912345678"),
        ClienteNoEncontradoError("abc-123"),
        JSONCorruptoError("clientes.json", "campo 'email' faltante"),
        DescuentoInvalidoError(1.5),
    ]
    
    for i, excepcion in enumerate(excepciones_prueba, 1):
        print(f"\n{i}. {excepcion.__class__.__name__}:")
        print(f"   {excepcion}")
    
    print("\n" + "=" * 60)
    print("Todas las excepciones funcionan correctamente")
    print("=" * 60)


if __name__ == "__main__":
    test_excepciones()

