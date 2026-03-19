# 🐾 Sistema de Gestión Veterinaria

Sistema desarrollado en **Python** para la administración básica de una veterinaria. Permite gestionar usuarios, propietarios, mascotas (perros, gatos y aves como tipos) y realizar operaciones como registro de vacunas, agendamiento de citas y generación de facturas.

## Estado del proyecto

Es un sistema **CLI (consola)** que opera directamente contra la base de datos configurada en `DATABASE_URL` (por ejemplo, Neon). La lógica de persistencia está implementada con **SQLAlchemy**.

## Requisitos

- Python `3.10+` (recomendado)
- Acceso a una base de datos compatible con Neon con una `DATABASE_URL` (usada por SQLAlchemy)
- Dependencias del proyecto (ver `requirements.txt`):
  - `sqlalchemy`
  - `psycopg2-binary`
  - `pydantic`
  - `python-dotenv`

## Estructura del proyecto

```text
Backend-Sistema-Veterinaria/
├── main.py
├── init_db.py
├── requirements.txt
├── .env                 # configuración local (no se debe versionar)
└── src/
    ├── database/
    │   └── config.py     # carga .env y crea engine + sesión
    ├── crud/
    │   ├── usuario.py
    │   ├── propietario.py
    │   ├── mascota.py
    │   ├── cita.py
    │   ├── vacuna.py
    │   └── factura.py
    └── entities/
        ├── usuario.py
        ├── propietario.py
        ├── mascota.py
        ├── cita.py
        ├── vacuna.py
        └── factura.py
```

## Configuración de base de datos (`.env`)

El proyecto **obliga** a definir `DATABASE_URL` en un archivo `.env` en la raíz del proyecto.

`src/database/config.py` hace:

- `load_dotenv()` para cargar variables desde `.env`
- `DATABASE_URL = os.getenv("DATABASE_URL")`
- si `DATABASE_URL` no existe, lanza: `ValueError("Se requiere DATABASE_URL en el archivo .env")`

### Ejemplo de `.env`

Se recomienda crear/ajustar el archivo `.env` con este formato (se deben reemplazar los valores):

```env
DATABASE_URL='postgresql://neondb_owner:npg_eZASH5VRmxa2@ep-wandering-firefly-ampk9ss8-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
```

Notas:

- Si la conexión es de **Neon** con `neon.tech`, el proyecto fuerza `sslmode=require` mediante `connect_args`.
- No se recomienda versionar la `.env` (contiene credenciales). Puede agregarse a `.gitignore`.

## Inicializar tablas en la base de datos

Antes de ejecutar el sistema por primera vez, se debe crear el esquema en Neon mediante SQLAlchemy con `init_db.py`:

```powershell
python init_db.py
```

Este script llama a `create_tables()` (SQLAlchemy `Base.metadata.create_all(...)`).

Si falla con un error de autenticación, `init_db.py` muestra una guía específica (incluye revisar el connection string y codificar caracteres especiales si aplica).

## Instalación y ejecución (CLI)

### 1) Crear entorno virtual (Windows / PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2) Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Ejecutar el sistema

```powershell
python main.py
```

## Ejecución de `main.py` (flujo completo)

Al iniciar, `main.py`:

1. Muestra el menú `--- ACCESO AL SISTEMA VETERINARIO ---`.
2. Pide `Nombre de usuario (login): `.
3. Busca el usuario por `nombre_usuario`.
4. Si **no existe**, crea un usuario inicial con:
   - `clave`: `admin123`
   - `email`: `"{u_nom}@vet.com"`
   - `nombre_usuario`: normalizado a minúsculas
5. Luego muestra el menú principal:
   - `1. Gestionar Propietarios (CRUD)`
   - `2. Gestionar Mascotas (CRUD)`
   - `3. Agendar Cita y Facturar`
   - `4. Registro de Vacunas`
   - `5. Salir`

## Importante: Video del enunciado

El siguiente video muestra la explicación del CRUD de `propietario` y cómo los cambios se reflejan en Neon, además del funcionamiento del `main.py` en consola:

[Ver video en YouTube](https://youtu.be/qouxJlBQ0lk)

## Menú: opciones y qué hace cada una

### 1) Gestionar Propietarios (CRUD)

Submenú:

- `1` Crear: se solicitan `Nombre` y `Teléfono`, y se crea un `Propietario` asociado al usuario logueado.
- `2` Listar: se imprimen todos los propietarios (ID, nombre y creador).
- `3` Editar: se solicita `ID del propietario (UUID)` y `Nuevo teléfono`, y se actualiza solo ese campo.
- `4` Eliminar: se solicita `ID a eliminar (UUID)` y se elimina el propietario.

### 2) Gestionar Mascotas (CRUD)

- En `main.py` se implementa principalmente la creación:
  - se solicitan `Nombre mascota`, `ID Propietario (UUID)`, `Tipo (Perro/Gato/Ave)` y `Edad`.
  - se crea la mascota asociada al propietario.

Nota: el campo `tipo_mascota` se guarda como texto; el sistema no impone restricciones estrictas más allá de lo que ingreses.

### 3) Agendar Cita y Facturar

Flujo:

- se solicita `ID Mascota (UUID)`, `Motivo` y `Costo`
- se crea una `Cita` con estado inicial `pendiente`
- se genera una `Factura`

Importante (posible inconsistencia):

En `main.py`, al crear la factura se pasa como argumento el `id_propietario` usando `nueva_cita.id_mascota` (ID de mascota), aunque `Factura` espera un `id_propietario` (Foreign Key a `propietario.id_propietario`).

Si la base de datos tiene restricciones FK estrictas, esto podría provocar un error al guardar la factura. En caso de error, debe revisarse esa parte del flujo en `main.py` y pasarse el ID correcto del propietario.

### 4) Registro de Vacunas

- se solicita `Nombre Vacuna`, `ID Mascota (UUID)` y `Costo`
- se crea una `Vacuna` asociada a la mascota y al usuario que registra.

### 5) Salir

- finaliza la ejecución.

## Validaciones de entrada

- `UUID`: se valida de forma básica verificando longitud (36) y guiones (4). Se debe ingresar un UUID con formato estándar.
- `Costo`: se valida como número decimal manualmente (permite hasta un punto decimal).

## Modelo de datos (tablas principales)

### `usuario`

- `id_usuario` (UUID, PK)
- `nombre`
- `nombre_usuario` (único)
- `clave`
- `email` (único)
- `fecha_creacion` (DateTime, auto)
- `fecha_edicion` (DateTime, auto)

> Nota: la entidad `Usuario` no incluye `id_usuario_creacion` / `id_usuario_edita`; por diseño, solo registra timestamps (`fecha_creacion`, `fecha_edicion`). El “quién crea/edita” se guarda en `propietario` y `mascota` mediante `id_usuario_creacion` y `id_usuario_edita`.

### `propietario`

- `id_propietario` (UUID, PK)
- `nombre`
- `email` (opcional)
- `telefono`
- `fecha_creacion` (DateTime, auto)
- `fecha_edicion` (DateTime, auto)
- `id_usuario_creacion` (FK a `usuario.id_usuario`)
- `id_usuario_edita` (FK a `usuario.id_usuario`, opcional)

### `mascota`

- `id_mascota` (UUID, PK)
- `id_propietario` (FK a `propietario.id_propietario`)
- `nombre`
- `edad`
- `tipo_mascota`
- `raza` (opcional)
- `fecha_creacion` (DateTime, auto)
- `fecha_edicion` (DateTime, auto)
- `id_usuario_creacion` (FK a `usuario.id_usuario`)
- `id_usuario_edita` (FK a `usuario.id_usuario`, opcional)

### `cita`

- `id_cita` (UUID, PK)
- `id_mascota` (FK)
- `id_usuario_agenda` (FK)
- `fecha_hora` (auto)
- `lugar` (opcional)
- `motivo`
- `costo`
- `estado` (default: `pendiente`)

### `vacuna`

- `id_vacuna` (UUID, PK)
- `nombre`
- `costo`
- `id_mascota` (FK)
- `id_usuario_registra` (FK)

### `factura`

- `id_factura` (UUID, PK)
- `id_cita` (FK, único: 1 factura por cita)
- `id_propietario` (FK)
- `id_usuario_genera` (FK)
- `total`
- `metodo_pago`
- `fecha_pago` (auto)

## Objetivo académico

Este proyecto fue desarrollado con fines educativos para aplicar:

- Programación Orientada a Objetos (POO)
- SQLAlchemy + persistencia
- SQLAlchemy ORM (modelos declarativos con `declarative_base`, sesiones con `SessionLocal` y consultas con `db.query`)
- Tipos de mascotas (por ejemplo: `Perro`, `Gato`, `Ave`) almacenados como texto en `tipo_mascota`
- Modularización (CRUD + Entities + Database config)
- Validaciones manuales en consola

## Solución de problemas rápida

- `Se requiere DATABASE_URL en el archivo .env`: se debe crear el archivo `.env` en la raíz y definir `DATABASE_URL`.
- Fallo al conectar a Neon en `init_db.py`: debe verificarse el connection string y actualizarse el `.env` (incluye posibles caracteres especiales en la URL).
- Error por “tablas no existen”: se debe ejecutar `python init_db.py` antes de `python main.py`.
- Error al crear factura: debe revisarse el flujo de `main.py` en la opción `3` (puede estar enviando un `id_propietario` incorrecto).
