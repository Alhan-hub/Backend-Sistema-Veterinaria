# 🐾 Sistema de Gestión Veterinaria

Sistema desarrollado en **Python** para la administración básica de una veterinaria. Permite gestionar usuarios, propietarios, mascotas (perros, gatos y aves como tipos) y operaciones como registro de vacunas, agendamiento de citas y generación de facturas.

## Estado del proyecto

La aplicación se expone como **API REST con FastAPI**. La ejecución principal está en `main.py`, que define la aplicación, registra los routers de cada entidad y arranca el servidor con **Uvicorn**. La persistencia sigue basada en **SQLAlchemy (ORM)** y en la `DATABASE_URL` configurada (por ejemplo, Neon).

Los cuerpos de entrada y las respuestas HTTP se modelan con **Pydantic** (esquemas definidos junto a los endpoints en `src/api/`).

## Requisitos

- Python `3.10+` (recomendado)
- Acceso a una base de datos PostgreSQL compatible (por ejemplo Neon) con `DATABASE_URL` en `.env`
- Dependencias del proyecto (ver `requirements.txt`):
  - `sqlalchemy`
  - `psycopg2-binary`
  - `pydantic` (incluye extras de email)
  - `python-dotenv`
  - `fastapi`
  - `uvicorn[standard]`

## Estructura del proyecto

```text
Backend-Sistema-Veterinaria/
├── main.py                 # FastAPI + registro de routers + arranque con Uvicorn
├── init_db.py
├── requirements.txt
├── .env                    # configuración local (no se debe versionar)
└── src/
    ├── api/                # routers REST y esquemas Pydantic por recurso
    │   ├── propietario.py
    │   ├── mascota.py
    │   ├── cita.py
    │   ├── factura.py
    │   ├── usuario.py
    │   └── vacuna.py
    ├── database/
    │   └── config.py       # .env, engine, SessionLocal, get_db, create_tables
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
- expone `get_db()` como dependencia de FastAPI para sesiones por petición (usado en varios routers)

### Ejemplo de `.env`

Se recomienda crear/ajustar el archivo `.env` con este formato (se deben reemplazar los valores):

```env
DATABASE_URL='postgresql://neondb_owner:npg_eZASH5VRmxa2@ep-wandering-firefly-ampk9ss8-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
```

Notas:

- Si la conexión es de **Neon** con `neon.tech`, el proyecto fuerza `sslmode=require` mediante `connect_args`.
- No se recomienda versionar la `.env` (contiene credenciales). Puede agregarse a `.gitignore`.

## Inicializar tablas en la base de datos

Antes de levantar la API por primera vez, crear el esquema en la base con `init_db.py`:

```powershell
python init_db.py
```

Este script llama a `create_tables()` (SQLAlchemy `Base.metadata.create_all(...)`).

Si falla con un error de autenticación, `init_db.py` muestra una guía específica (incluye revisar el connection string y codificar caracteres especiales si aplica).

## Instalación y ejecución (API)

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

### 3) Ejecutar la aplicación

Desde la raíz del proyecto:

```powershell
python main.py
```

Equivale a servir la app `main:app` con Uvicorn en `http://127.0.0.1:8000` y recarga automática en desarrollo (`reload=True`).

También puede usarse Uvicorn directamente:

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Documentación interactiva (Swagger / OpenAPI)

FastAPI genera automáticamente la especificación OpenAPI y la interfaz **Swagger UI**:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Ahí se documentan y pueden probarse los endpoints (métodos HTTP, cuerpos JSON, respuestas y códigos de estado).

### Ruta raíz

- `GET /` — estado del servicio y enlace a la documentación.

## Endpoints por entidad (REST)

Convención general: **GET** lista y por id, **POST** creación, **PUT** actualización, **DELETE** eliminación (salvo detalles indicados). Las rutas base asumen el prefijo vacío (`/`); los IDs son **UUID** salvo que el cliente envíe otro formato válido.

| Entidad | Lista | Por id | Crear | Actualizar | Eliminar |
|--------|--------|--------|--------|------------|----------|
| **Propietarios** | `GET /propietarios` | `GET /propietarios/{id}` | `POST /propietarios` | `PUT /propietarios/{id}` | `DELETE /propietarios/{id}` |
| **Mascotas** | `GET /mascotas` | `GET /mascotas/{id}` | `POST /mascotas` | `PUT /mascotas/{id}` | `DELETE /mascotas/{id}` |
| **Citas** | `GET /citas` | `GET /citas/{id}` | `POST /citas` | `PUT /citas/{id}` | `DELETE /citas/{id}` |
| **Facturas** | `GET /facturas` | `GET /facturas/{id}` | `POST /facturas` | `PUT /facturas/{id}` | `DELETE /facturas/{id}` |
| **Usuarios** | `GET /usuarios` | `GET /usuarios/{usuario_id}` | `POST /usuarios` | `PUT /usuarios/{usuario_id}` | `DELETE /usuarios/{usuario_id}` |
| **Vacunas** | `GET /vacunas` | `GET /vacunas/{vacuna_id}` | `POST /vacunas` | `PUT /vacunas/{vacuna_id}` | `DELETE /vacunas/{vacuna_id}` |

**Notas:**

- **Propietarios** y **mascotas:** creación/actualización requieren `id_usuario_creacion` / `id_usuario_edita` según el esquema en Swagger.
- **Citas** y **facturas:** estado inicial de cita y reglas de negocio (p. ej. una factura por cita) están en la capa CRUD; errores de validación pueden responder **400** con detalle en el cuerpo.
- **Usuarios:** **POST** valida unicidad de `nombre_usuario` y `email`.
- **Vacunas:** existe además `GET /vacunas/mascota/{mascota_id}` para listar vacunas de una mascota.

Los detalles de cada campo (JSON de entrada/salida) están en **Swagger** (`/docs`).

## Configuración principal del API (`main.py`)

En `main.py` se define el objeto `FastAPI` (título, descripción, versión), se incluyen los routers de `src.api` y, bajo `if __name__ == "__main__"`, se invoca `uvicorn.run("main:app", ...)`. Cualquier ajuste global de la API (metadata, CORS futuro, routers adicionales) conviene centralizarlo ahí.

## Importante: Video del enunciado

El siguiente video muestra la explicación del CRUD de `propietario`, cómo los cambios se reflejan en Neon y el uso de la API con FastAPI (incluida la documentación en Swagger):

[Ver video en YouTube](https://youtu.be/VgQHMOsCV54)

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
- SQLAlchemy + persistencia y ORM (modelos declarativos, sesiones, CRUD)
- **API REST con FastAPI** (routers, dependencias, códigos HTTP)
- **Esquemas de validación y serialización con Pydantic**
- **Documentación automática OpenAPI / Swagger UI**
- Tipos de mascotas (por ejemplo: `Perro`, `Gato`, `Ave`) almacenados como texto en `tipo_mascota`
- Modularización (`src/api`, `crud`, `entities`, `database`)

## Solución de problemas rápida

- `Se requiere DATABASE_URL en el archivo .env`: crear `.env` en la raíz y definir `DATABASE_URL`.
- Fallo al conectar a Neon en `init_db.py`: verificar el connection string y actualizar `.env` (incluye caracteres especiales en la URL).
- Error por “tablas no existen”: ejecutar `python init_db.py` antes de levantar la API.
- El servidor no inicia o el puerto está ocupado: cambiar el puerto en `uvicorn.run(...)` o en la línea de comandos de Uvicorn (`--port`).
