# Documentación: Aplicación de POO en el Sistema GIC

## 📚 Introducción

El Sistema Gestor Inteligente de Clientes (GIC) es una aplicación que implementa de manera integral los cuatro pilares de la Programación Orientada a Objetos (POO): **Herencia**, **Polimorfismo**, **Encapsulación** y **Abstracción**.

---

## 1️⃣ HERENCIA

### Concepto
La herencia permite que una clase (subclase) herede atributos y métodos de otra clase (superclase), promoviendo la reutilización de código.

### Implementación en GIC

```
Cliente (Clase Base Abstracta)
├── ClienteRegular
├── ClientePremium
└── ClienteCorporativo
```

### Código Base (Cliente)

```python
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class Cliente(ABC):
    """Clase abstracta base para todos los tipos de clientes."""
    
    campos_base = ['nombre', 'email', 'telefono', 'direccion', 'ciudad']
    
    def __init__(self, nombre, email, telefono, direccion, ciudad):
        self.id_cliente = str(uuid.uuid4())
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.ciudad = ciudad
        self.activo = True
        self.fecha_registro = datetime.now()
    
    @abstractmethod
    def calcular_beneficio(self):
        """Método abstracto implementado por cada subclase."""
        pass
```

### Subclases Específicas

#### ClienteRegular
```python
class ClienteRegular(Cliente):
    """Cliente estándar sin beneficios especiales."""
    
    def __init__(self, nombre, email, telefono, direccion, ciudad, 
                 nivel_satisfaccion=3):
        super().__init__(nombre, email, telefono, direccion, ciudad)
        self.tipo_cliente = 'ClienteRegular'
        self.nivel_satisfaccion = nivel_satisfaccion
    
    def calcular_beneficio(self):
        """Beneficio basado en satisfacción."""
        return self.nivel_satisfaccion * 100
```

#### ClientePremium
```python
class ClientePremium(Cliente):
    """Cliente con descuentos y programa de puntos."""
    
    def __init__(self, nombre, email, telefono, direccion, ciudad,
                 descuento=0.10, puntos_acumulados=0):
        super().__init__(nombre, email, telefono, direccion, ciudad)
        self.tipo_cliente = 'ClientePremium'
        self.descuento = descuento
        self.puntos_acumulados = puntos_acumulados
        self.fecha_vencimiento_premium = datetime.now().replace(year=datetime.now().year + 1)
    
    def calcular_beneficio(self):
        """Beneficio = puntos * 10 + descuento * 1000."""
        return (self.puntos_acumulados * 10) + (self.descuento * 1000)
```

#### ClienteCorporativo
```python
class ClienteCorporativo(Cliente):
    """Cliente empresarial con descuentos por volumen."""
    
    def __init__(self, nombre, email, telefono, direccion, ciudad,
                 razon_social, rut_empresa, pais_empresa,
                 contacto_principal, descuento_volumen=0.05,
                 numero_empleados=1):
        super().__init__(nombre, email, telefono, direccion, ciudad)
        self.tipo_cliente = 'ClienteCorporativo'
        self.razon_social = razon_social
        self.rut_empresa = rut_empresa
        self.pais_empresa = pais_empresa
        self.contacto_principal = contacto_principal
        self.descuento_volumen = descuento_volumen
        self.numero_empleados = numero_empleados
    
    def calcular_beneficio(self):
        """Beneficio = empleados * 100 + descuento * 5000."""
        return (self.numero_empleados * 100) + (self.descuento_volumen * 5000)
```

### Beneficios de la Herencia en GIC

✅ **Reutilización de código**: Campos comunes (nombre, email, etc.) definidos una sola vez
✅ **Extensibilidad**: Fácil agregar nuevos tipos de clientes
✅ **Mantenibilidad**: Cambios en la clase base afectan a todas las subclases
✅ **Polimorfismo**: Cada tipo implementa `calcular_beneficio()` a su manera

---

## 2️⃣ POLIMORFISMO

### Concepto
El polimorfismo permite que objetos de diferentes clases respondan al mismo mensaje de manera diferente.

### Implementación en GIC

El método `calcular_beneficio()` se ejecuta de forma diferente según el tipo de cliente:

```python
# En GestorClientes.obtener_estadisticas()
clientes_activos = [c for c in self.clientes if c.activo]
beneficios_totales = sum(c.calcular_beneficio() for c in clientes_activos)

# Cada cliente calcula su beneficio de forma diferente
cliente_regular = ClienteRegular("Juan", "juan@email.com", "+56912345678", 
                                  "Calle A", "Santiago", nivel_satisfaccion=4)
cliente_premium = ClientePremium("Maria", "maria@email.com", "+56987654321",
                                  "Calle B", "Valparaiso", descuento=0.20, 
                                  puntos_acumulados=500)

# Mismo método, diferente resultado
print(cliente_regular.calcular_beneficio())  # 400 (4 * 100)
print(cliente_premium.calcular_beneficio())  # 5000 (500 * 10 + 0.20 * 1000)
```

### Tabla de Polimorfismo en GIC

| Tipo Cliente | calcular_beneficio() | Fórmula |
|-------------|----------------------|---------|
| Regular | 4 * 100 | nivel_satisfacción * 100 |
| Premium | 5000 | (puntos * 10) + (descuento * 1000) |
| Corporativo | 3100 | (empleados * 100) + (descuento * 5000) |

### Método Polimórfico en Reporte

```python
def generar_reporte_beneficios(self):
    """Genera reporte llamando a calcular_beneficio() de cada cliente."""
    clientes_activos = [c for c in self.clientes if c.activo]
    
    reporte = []
    for cliente in clientes_activos:
        # Polimorfismo: mismo método, resultado diferente
        reporte.append({
            'id': cliente.id_cliente,
            'nombre': cliente.nombre,
            'tipo': cliente.tipo_cliente,
            'beneficio': cliente.calcular_beneficio()  # ← Polimorfismo
        })
    
    return reporte
```

---

## 3️⃣ ENCAPSULACIÓN

### Concepto
La encapsulación protege los datos internos de una clase permitiendo acceso controlado a través de métodos.

### Implementación en GIC

#### Atributos Protegidos

```python
class Cliente:
    def __init__(self, ...):
        self._id_cliente = str(uuid.uuid4())  # Protegido
        self._activo = True                    # Protegido
        self._fecha_registro = datetime.now()  # Protegido
```

#### Validación en el Setter

```python
class Cliente:
    def __init__(self, nombre, email, ...):
        self.nombre = ValidadorDatos.validar_nombre(nombre)
        self.email = ValidadorDatos.validar_email(email)
        self.telefono = ValidadorDatos.validar_telefono(telefono)
```

#### Métodos de Acceso Controlado

```python
class Cliente:
    def obtener_id_cliente(self):
        """Obtiene el ID (solo lectura)."""
        return self._id_cliente
    
    def es_activo(self):
        """Verifica si el cliente está activo."""
        return self._activo
    
    def desactivar(self):
        """Desactiva el cliente de forma controlada."""
        if self._activo:
            self._activo = False
            return True
        return False
```

#### Conversión Segura a Diccionario

```python
class Cliente:
    def to_dict(self):
        """Convierte el cliente a diccionario para persistencia."""
        return {
            'id_cliente': self.id_cliente,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'activo': self.activo,
            'fecha_registro': self.fecha_registro.isoformat(),
            'tipo_cliente': self.tipo_cliente
        }
```

### Beneficios de Encapsulación

✅ **Seguridad**: No se puede acceder directamente a `_activo` o `_id_cliente`
✅ **Validación**: Todos los datos pasan por validadores antes de asignarse
✅ **Mantenibilidad**: Se puede cambiar la implementación interna sin afectar el exterior
✅ **Control**: Solo los métodos autorizados pueden modificar el estado

---

## 4️⃣ ABSTRACCIÓN

### Concepto
La abstracción permite ocultar la complejidad, mostrando solo lo esencial. Se implementa mediante clases abstractas y métodos abstractos.

### Implementación en GIC

#### Clase Abstracta Base

```python
from abc import ABC, abstractmethod

class Cliente(ABC):
    """Clase abstracta que define la interfaz para todos los clientes."""
    
    @abstractmethod
    def calcular_beneficio(self):
        """Método abstracto que toda subclase debe implementar."""
        pass
    
    @abstractmethod
    def __str__(self):
        """Representación en string personalizada."""
        pass
```

#### Abstracción de Complejidad

```python
class ValidadorDatos:
    """Abstrae la complejidad de validaciones con regex."""
    
    @staticmethod
    def validar_email(email):
        """Valida email sin exponer la regex interna."""
        if not re.match(ValidadorDatos.REGEX_EMAIL, email.lower()):
            raise EmailInvalidoError(email)
        return email.lower()
    
    @staticmethod
    def validar_telefono(telefono):
        """Valida teléfono internacionalmente."""
        if not re.match(ValidadorDatos.REGEX_TELEFONO, telefono.strip()):
            raise TelefonoInvalidoError(telefono)
        return telefono.strip()
```

#### Abstracción de Persistencia

```python
class PersistenciaJSON:
    """Abstrae los detalles de guardar/cargar JSON."""
    
    def guardar(self, datos):
        """Guarda datos sin que el cliente sepa cómo."""
        # Detalles de implementación ocultos
        with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, default=str)
    
    def cargar_clientes(self):
        """Carga datos de forma abstracta."""
        # El cliente solo llama, no necesita saber cómo funciona
        if not os.path.exists(self.ruta_archivo):
            return []
        # ... detalles de carga
```

#### Abstracción de Logging

```python
class LoggerSistema:
    """Abstrae el sistema de logging completo."""
    
    def log_cliente_creado(self, id_cliente, tipo, nombre):
        """Registra cliente creado sin exponer detalles."""
        # El cliente solo llama este método
        self.info(f"Cliente creado | ID: {id_cliente} | Tipo: {tipo} | Nombre: {nombre}")
```

### Beneficios de Abstracción

✅ **Simplicidad**: El usuario del sistema no necesita saber cómo funciona internamente
✅ **Flexibilidad**: Se puede cambiar la implementación sin afectar la interfaz
✅ **Enfoque**: Se define claramente qué es obligatorio implementar
✅ **Interfaz clara**: Los métodos abstractos documentan qué debe hacer cada subclase

---

## 🎯 INTEGRACIÓN DE POO EN GIC

### Flujo Completo: Crear Cliente Premium

```python
# 1. MenuConsola (usuario final)
cliente = gestor.crear_cliente(
    'premium',
    nombre="Maria",
    email="maria@email.com",
    telefono="+56912345678",
    descuento=0.15,
    puntos_acumulados=250
)

# 2. GestorClientes (orquestador)
# - Valida email duplicado (Encapsulación: validador interno)
# - Valida teléfono (Abstracción: ValidadorDatos)
# - Crea ClientePremium (Herencia: instantia subclase)
# - Guarda en JSON (Abstracción: PersistenciaJSON)
# - Registra en log (Abstracción: LoggerSistema)

# 3. ClientePremium (polimorfismo)
cliente = ClientePremium(
    nombre="Maria",
    email="maria@email.com",
    # ... otros datos
)

# 4. Cálculo de beneficio (Polimorfismo)
beneficio = cliente.calcular_beneficio()  # Resultado: 4000
# (250 * 10) + (0.15 * 1000) = 2500 + 1500 = 4000
```

### Matriz de POO en GIC

| Pilar | Implementación | Beneficio |
|------|----------------|-----------|
| **Herencia** | Cliente → Regular/Premium/Corporativo | Reutiliza código común, permite extender |
| **Polimorfismo** | calcular_beneficio() diferente por tipo | Cada tipo calcula su beneficio a su manera |
| **Encapsulación** | Validadores internos, métodos privados | Protege datos, asegura consistencia |
| **Abstracción** | ValidadorDatos, PersistenciaJSON, Logger | Oculta complejidad, interfaz clara |

---

## 📊 Comparación: CON POO vs SIN POO

### ❌ SIN POO (Código Procedural)

```python
# Caótico, duplicado, difícil de mantener
clientes = []

def crear_cliente_regular(nombre, email, ...):
    cliente = {
        'id': str(uuid.uuid4()),
        'nombre': nombre,
        'email': email,
        'tipo': 'regular',
        # ... más datos
    }
    clientes.append(cliente)
    return cliente

def crear_cliente_premium(nombre, email, ...):
    cliente = {
        'id': str(uuid.uuid4()),
        'nombre': nombre,
        'email': email,
        'tipo': 'premium',
        'descuento': descuento,
        'puntos': puntos,
        # ... duplicado de arriba
    }
    clientes.append(cliente)
    return cliente

def crear_cliente_corporativo(...):
    # Más duplicación...
    pass

def calcular_beneficio(cliente):
    if cliente['tipo'] == 'regular':
        return cliente.get('satisfaccion', 3) * 100
    elif cliente['tipo'] == 'premium':
        return (cliente['puntos'] * 10) + (cliente['descuento'] * 1000)
    elif cliente['tipo'] == 'corporativo':
        return (cliente['empleados'] * 100) + (cliente['descuento'] * 5000)
```

### ✅ CON POO (Código Limpio)

```python
# Limpio, mantenible, escalable
class Cliente(ABC):
    def __init__(self, nombre, email, ...):
        self.id_cliente = str(uuid.uuid4())
        self.nombre = nombre
        # ... validación automática

    @abstractmethod
    def calcular_beneficio(self):
        pass

class ClienteRegular(Cliente):
    def calcular_beneficio(self):
        return self.nivel_satisfaccion * 100

class ClientePremium(Cliente):
    def calcular_beneficio(self):
        return (self.puntos_acumulados * 10) + (self.descuento * 1000)

class ClienteCorporativo(Cliente):
    def calcular_beneficio(self):
        return (self.numero_empleados * 100) + (self.descuento_volumen * 5000)

# Uso simple y consistente
gestor.crear_cliente('regular', nombre="Juan", ...)
gestor.crear_cliente('premium', nombre="Maria", ...)
```

---

## 🎓 Conclusión

El Sistema GIC demuestra cómo los 4 pilares de POO trabajan juntos:

- **Herencia**: Evita duplicación de código común
- **Polimorfismo**: Permite diferentes comportamientos con la misma interfaz
- **Encapsulación**: Protege y valida los datos
- **Abstracción**: Simplifica la complejidad, enfoca en lo esencial

Resultado: **Código profesional, mantenible y escalable** ✨
