# 📘 README - Sistema Gestor Inteligente de Clientes (GIC)

## 🎯 Descripción General

El **Sistema Gestor Inteligente de Clientes (GIC)** es una aplicación en Python para la gestión completa de clientes con CRUD, validaciones, persistencia y logging. Implementa de manera integral los pilares de **Programación Orientada a Objetos (POO)**.

### Características Principales

✅ **3 Tipos de Clientes**: Regular, Premium, Corporativo  
✅ **CRUD Completo**: Crear, Leer, Actualizar, Eliminar, Reactivar  
✅ **Validaciones**: Email, teléfono, RUT/DNI multi-país con regex  
✅ **Persistencia JSON**: Almacenamiento y respaldos automáticos  
✅ **Logging**: Registro de todas las operaciones  
✅ **Excepciones Personalizadas**: Manejo de errores robusto  
✅ **Interfaz Interactiva**: Menú de consola amigable  

---

## 🏗️ Estructura del Proyecto

```
proyecto_gic/
│
├── main.py                          # Punto de entrada
│
├── modelos/
│   ├── __init__.py
│   ├── excepciones.py              # Jerarquía de excepciones (15+)
│   └── cliente.py                  # Clases con herencia (Regular/Premium/Corporativo)
│
├── utils/
│   ├── __init__.py
│   ├── validador.py                # Validaciones con regex
│   └── persistencia.py             # Manejo de JSON con respaldos
│
├── gestor/
│   ├── __init__.py
│   ├── logger.py                   # Sistema de logging (INFO/WARNING/ERROR)
│   └── gestor_clientes.py          # CRUD completo
│
├── interfaz/
│   ├── __init__.py
│   └── menu_consola.py             # Menú interactivo (9 opciones)
│
├── data/
│   ├── clientes.json               # Se crea automáticamente
│   └── respaldos/                  # Respaldos automáticos
│
└── logs/
    └── sistema.log                 # Se crea automáticamente
```

---

## 🚀 Instalación y Ejecución

### 1. Requisitos

- **Python 3.8+**
- Windows, Linux o macOS

### 2. Crear Carpeta del Proyecto

```bash
mkdir proyecto_gic
cd proyecto_gic
```

### 3. Crear Estructura de Carpetas

**En Windows (cmd):**
```bash
mkdir modelos utils gestor interfaz data logs
type nul > modelos\__init__.py
type nul > utils\__init__.py
type nul > gestor\__init__.py
type nul > interfaz\__init__.py
```

**En Linux/macOS:**
```bash
mkdir modelos utils gestor interfaz data logs
touch modelos/__init__.py utils/__init__.py gestor/__init__.py interfaz/__init__.py
```

### 4. Copiar Archivos Python

Copia los 8 archivos Python en sus carpetas correspondientes:
- `modelos/excepciones.py`
- `modelos/cliente.py`
- `utils/validador.py`
- `utils/persistencia.py`
- `gestor/logger.py`
- `gestor/gestor_clientes.py`
- `interfaz/menu_consola.py`
- `main.py` (en la raíz)

### 5. Ejecutar el Sistema

```bash
cd proyecto_gic
python main.py
```

---

## 📋 Menú Principal - 9 Opciones

```
==================================================================
MENU PRINCIPAL
==================================================================
1.  Crear cliente
2.  Listar clientes
3.  Buscar cliente
4.  Actualizar cliente
5.  Eliminar cliente
6.  Reactivar cliente
7.  Ver estadisticas
8.  Reporte de beneficios
9.  Ver detalles de cliente
0.  Salir
==================================================================
```

### Opciones Detalladas

#### 1. Crear Cliente
- **Subtipos**: Regular, Premium, Corporativo
- **Validaciones**: Email duplicado, teléfono duplicado
- **Teléfono**: Formato internacional (+código_país número)
- **Ejemplo**: `+56912345678` (Chile), `+5491112345678` (Argentina)

#### 2. Listar Clientes
- **Filtros por estado**: Activos, inactivos, todos
- **Filtros por tipo**: Regular, Premium, Corporativo
- **Muestra**: Nombre, ID, tipo, email, ciudad, estado, beneficio

#### 3. Buscar Cliente
- **Por ID**: Identificador único
- **Por Email**: Dirección de correo
- **Por Teléfono**: Número de contacto

#### 4. Actualizar Cliente
- **Campos modificables**: Nombre, email, teléfono, dirección, ciudad
- **Campos específicos**: Puntos (Premium), empleados (Corporativo)
- **Validaciones**: Duplicados, formato

#### 5. Eliminar Cliente
- **Soft delete**: Marca como inactivo (recuperable)
- **Confirmación**: Requiere confirmación del usuario
- **Guardado**: Automático en JSON

#### 6. Reactivar Cliente
- **Restaura**: Cliente marcado como inactivo
- **Requiere**: Confirmación del usuario

#### 7. Ver Estadísticas
- **Total de clientes**: Activos, inactivos
- **Por tipo**: Regular, Premium, Corporativo
- **Beneficios totales**: Suma de todos los beneficios

#### 8. Reporte de Beneficios
- **Ordenado por**: Beneficio (mayor a menor)
- **Muestra**: Cliente, tipo, beneficio económico
- **Total**: Suma de beneficios

#### 9. Ver Detalles Completo
- **Información completa**: Todos los campos del cliente
- **Beneficio económico**: Calculado según tipo
- **Fecha de registro**: Exacta con timestamp

---

## 📊 Especificaciones de Clientes

### Cliente Regular

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| nombre | str | Nombre completo |
| email | str | Correo electrónico |
| telefono | str | Número con código país |
| direccion | str | Domicilio |
| ciudad | str | Localidad |
| nivel_satisfaccion | int (1-5) | Satisfacción del cliente |
| **Beneficio** | **int** | **nivel_satisfaccion * 100** |

**Ejemplo**: Satisfacción 4 = Beneficio $400

---

### Cliente Premium

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| nombre | str | Nombre completo |
| email | str | Correo electrónico |
| telefono | str | Número con código país |
| direccion | str | Domicilio |
| ciudad | str | Localidad |
| descuento | float (0.0-1.0) | Porcentaje de descuento |
| puntos_acumulados | int | Puntos de lealtad |
| fecha_vencimiento_premium | date | Vigencia de beneficios |
| **Beneficio** | **float** | **(puntos * 10) + (descuento * 1000)** |

**Ejemplo**: Puntos 250, Descuento 0.15 = Beneficio $4000

---

### Cliente Corporativo

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| nombre | str | Nombre de la empresa |
| email | str | Email corporativo |
| telefono | str | Número corporativo |
| direccion | str | Domicilio de la empresa |
| ciudad | str | Localidad |
| razon_social | str | Razón social |
| rut_empresa | str | RUT/DNI (formato país) |
| pais_empresa | str | País (CHILE, ARGENTINA, etc.) |
| contacto_principal | str | Persona de contacto |
| descuento_volumen | float (0.0-1.0) | Descuento por volumen |
| numero_empleados | int | Cantidad de empleados |
| **Beneficio** | **float** | **(empleados * 100) + (descuento * 5000)** |

**Ejemplo**: Empleados 5, Descuento 0.10 = Beneficio $1500

---

## 🌍 Validaciones Internacionales

### Teléfono
Formato: `+XX X XXXX XXXX`
- **Chile**: +56 9 1234 5678
- **Argentina**: +54 9 11 1234 5678
- **Brasil**: +55 11 91234 5678
- **Perú**: +51 987 654 321
- **Colombia**: +57 300 123 4567
- **Uruguay**: +598 99 123 456

### RUT/DNI por País

| País | Formato | Ejemplo |
|------|---------|---------|
| Chile | XX.XXX.XXX-K | 12.345.678-9 |
| Argentina | XXXXXXXX | 12345678 |
| Brasil | XXX.XXX.XXX-XX | 123.456.789-01 |
| Perú | XXXXXXXX | 12345678 |
| Colombia | XXXXXX-XXXXXXXXX | 1234567 |
| Uruguay | X.XXX.XXX-X | 1.234.567-8 |

---

## 💾 Persistencia de Datos

### Formato JSON
```json
{
  "id_cliente": "550e8400-e29b-41d4-a716-446655440000",
  "nombre": "Maria Gonzalez",
  "email": "maria@email.com",
  "telefono": "+56912345678",
  "direccion": "Av. Providencia 123",
  "ciudad": "Santiago",
  "activo": true,
  "fecha_registro": "2026-02-16T20:33:15.123456",
  "tipo_cliente": "ClientePremium",
  "descuento": 0.15,
  "puntos_acumulados": 250,
  "fecha_vencimiento_premium": "2027-02-16T20:33:15.123456"
}
```

### Respaldos Automáticos
- Se crea respaldo cada vez que se guarda
- Ubicación: `data/respaldos/`
- Nombre: `clientes_YYYYMMDD_HHMMSS.json`

---

## 📝 Logging

### Niveles de Log

| Nivel | Uso | Ejemplo |
|-------|-----|---------|
| **INFO** | Operaciones normales | "Cliente creado" |
| **WARNING** | Advertencias | "Validación fallida" |
| **ERROR** | Errores recuperables | "Archivo no encontrado" |
| **CRITICAL** | Errores críticos | "Base de datos corrupta" |

### Ubicación
- Archivo: `logs/sistema.log`
- Formato: `YYYY-MM-DD HH:MM:SS | NIVEL | MENSAJE`

### Ejemplo de Log
```
2026-02-16 20:33:15 | INFO     | SISTEMA GIC INICIADO
2026-02-16 20:33:16 | INFO     | Cliente creado | ID: 550e8400... | Tipo: ClientePremium | Nombre: Maria Gonzalez
2026-02-16 20:33:17 | INFO     | Cliente actualizado | ID: 550e8400... | Campos: email, puntos_acumulados
2026-02-16 20:33:18 | WARNING  | Validacion fallida | Campo: email | Valor: usuario.com | Motivo: Falta @
```

---

## 🔒 Manejo de Excepciones

### Jerarquía de Excepciones

```
Exception
└── ErrorGestionClientes (Base)
    ├── ClienteNoEncontradoError
    ├── ClienteInactivoError
    ├── EmailDuplicadoError
    ├── TelefonoDuplicadoError
    ├── ValidacionError
    │   ├── EmailInvalidoError
    │   ├── TelefonoInvalidoError
    │   ├── DireccionInvalidaError
    │   ├── CiudadInvalidaError
    │   ├── RUTInvalidoError
    │   ├── DescuentoInvalidoError
    │   ├── NombreInvalidoError
    │   └── NumeroEmpleadosInvalidoError
    └── OperacionCRUDError
```

### Ejemplos de Manejo

```python
try:
    cliente = gestor.crear_cliente('premium', ...)
except EmailDuplicadoError:
    print("Este email ya existe")
except TelefonoDuplicadoError:
    print("Este teléfono ya está registrado")
except ValidacionError as e:
    print(f"Dato inválido: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
```

---

## 🧪 Pruebas

### Probar Módulos Individuales

```bash
# Excepciones
python modelos/excepciones.py

# Validaciones
python utils/validador.py

# Clientes
python modelos/cliente.py

# Persistencia
python utils/persistencia.py

# Logger
python gestor/logger.py

# CRUD
python gestor/gestor_clientes.py

# Menú
python interfaz/menu_consola.py

# Sistema completo
python main.py
```

---

## 📊 Ejemplo Completo de Uso

```bash
$ python main.py

======================================================================
GESTOR INTELIGENTE DE CLIENTES (GIC)
======================================================================
Iniciando sistema...
Sistema iniciado correctamente

======================================================================
MENU PRINCIPAL
======================================================================
...
Seleccione una opcion: 1

Tipo de cliente:
1. Cliente Regular
2. Cliente Premium
3. Cliente Corporativo

Seleccione tipo (1-3): 2

--- DATOS DEL CLIENTE PREMIUM ---
Nombre completo: Maria Gonzalez
Email: maria@email.com
Telefono (formato internacional con codigo de pais)
Ejemplos: +56912345678 (Chile), +5491112345678 (Argentina)
Telefono: +56912345678
Direccion: Av. Providencia 123
Ciudad: Santiago
Descuento (0.0-1.0) [default: 0.10]: 0.15
Puntos acumulados [default: 0]: 250

======================================================================
CLIENTE PREMIUM CREADO EXITOSAMENTE
======================================================================
[ClientePremium] Maria Gonzalez
  ID: 550e8400-e29b-41d4-a716-446655440000
  Email: maria@email.com
  Teléfono: +56912345678
  Ciudad: Santiago
  Estado: ✓ Activo
  Beneficio: $4,000.00
```

---

## 💡 Características Adicionales

### CRUD Completo
- **Crear**: Validaciones automáticas de duplicados
- **Leer**: Búsqueda por ID, email o teléfono
- **Actualizar**: Modificación con validaciones
- **Eliminar**: Soft delete (recuperable)
- **Reactivar**: Restauración de clientes eliminados

### Validaciones Multi-País
- Teléfono: Formato internacional (+código_país)
- RUT/DNI: Específico por país (Chile, Argentina, Brasil, Perú, Colombia, Uruguay)

### Persistencia Inteligente
- Guarda automáticamente en JSON
- Crea respaldos cada vez que se guarda
- Carga datos al iniciar

### Sistema de Logging Completo
- Todas las operaciones registradas
- Información, advertencias y errores
- Útil para auditoría y debugging

---

---

## 🆘 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'modelos'"
**Solución**: Verifica que `__init__.py` existe en cada carpeta.

### Error: "FileNotFoundError: [Errno 2] No such file or directory: 'data/clientes.json'"
**Solución**: La carpeta `data/` se crea automáticamente al guardar. Si persiste, créala manualmente.

### Error: "Cannot find module validador"
**Solución**: Verifica que los imports en los archivos usan rutas relativas correctas.

---

## 📚 Documentación Adicional

- **DOCUMENTACION_POO.md**: Explicación detallada de herencia, polimorfismo, encapsulación y abstracción
- **DIAGRAMA_UML.txt**: Diagrama de clases en formato PlantUML
- **ESPECIFICACIONES.txt**: Requisitos del proyecto (si aplica)

---

## 👨‍💻 Autor

Sistema Gestor Inteligente de Clientes (GIC) - Febrero 2026

---

## 📝 Notas Finales

Este sistema demuestra:
- ✅ Programación Orientada a Objetos integral
- ✅ CRUD completo funcional
- ✅ Validaciones robustas
- ✅ Persistencia profesional
- ✅ Interfaz amigable
- ✅ Código limpio y mantenible

