# TaskFlow - POO II (UNAULA)

Sistema de gestión de tareas desarrollado como proyecto incremental para la asignatura **IF0100 - POO II** (UNAULA).

---

## Estructura del Proyecto

```
POO II/
├── src/
│   ├── __init__.py
│   └── domain/
│       ├── __init__.py
│       ├── enums.py       # PrioridadTarea, EstadoTarea
│       ├── usuario.py     # Clase Usuario
│       ├── tarea.py       # Clase Tarea
│       └── proyecto.py    # Clase Proyecto
├── tests/                 # Tests unitarios pytest (E2)
│   ├── __init__.py
│   ├── conftest.py        # Fixtures compartidas
│   ├── test_usuario.py
│   ├── test_tarea.py
│   ├── test_proyecto.py
│   └── test_enums.py
├── features/              # Tests BDD behave (E2)
│   ├── environment.py
│   ├── usuarios.feature
│   ├── proyectos.feature
│   ├── tareas.feature
│   └── steps/
│       ├── usuarios_steps.py
│       ├── proyectos_steps.py
│       └── tareas_steps.py
├── test_dominio.py        # Tests básicos E1
├── pytest.ini             # Configuración de pytest
├── .coveragerc            # Configuración de cobertura
├── requirements.txt       # Dependencias
└── README.md
```

---

## Requisitos Previos

- Python 3.10 o superior
- pip

---

## Instalación

```bash
# Clonar el repositorio (si aplica)
git clone <--->
cd "POO II"

# Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución de Tests

### Tests unitarios (pytest)

```bash
# Ejecutar todos los tests con detalle
pytest tests/ -v

# Con reporte de cobertura en terminal e HTML
pytest --cov=src --cov-report=html --cov-report=term

# Tests del dominio básico (E1)
pytest test_dominio.py -v
```

### Tests BDD (behave)

```bash
behave features/
```

---

## E3 — Prototipo Web (FastAPI + HTMX)

### Instalar dependencias web

```bash
pip install -r requirements.txt
```

### Ejecutar el servidor

```bash
uvicorn api.main:app --reload
```

El servidor arranca en `http://127.0.0.1:8000`.

| URL | Descripción |
|-----|-------------|
| `http://127.0.0.1:8000/` | Interfaz web principal |
| `http://127.0.0.1:8000/docs` | Swagger UI interactivo |

### Flujo de uso rápido

1. Crear un usuario en la columna derecha (username, email).
2. Anotar el **ID** que devuelve el endpoint (ver `/docs` → `GET /usuarios`).
3. Crear un proyecto indicando el ID del líder.
4. Agregar tareas desde el card del proyecto.
5. Marcar tareas como completadas o cambiar prioridad directamente desde la lista.

---

## E4 — Persistencia (SQLAlchemy + Alembic)

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Aplicar migraciones

```bash
python apply_migrations.py
```

O con Alembic directamente:

```bash
alembic upgrade head
```

Esto crea la base de datos `taskflow.db` con las tablas `usuarios`, `proyectos` y `tareas`.

### Verificar migraciones aplicadas

```bash
alembic current   # Muestra la migración actual
alembic history --verbose   # Historial completo
```

### Estructura de base de datos

```
usuarios (id, username*, email*, activo)
  ↓ 1-to-Many
proyectos (id, nombre, descripcion, usuario_id)
  ↓ 1-to-Many
tareas (id, titulo, descripcion, prioridad, estado, proyecto_id)
```

*unique: username, email

---

## Ejemplo de Uso

```python
from src.domain.enums import PrioridadTarea, EstadoTarea
from src.domain.usuario import Usuario
from src.domain.tarea import Tarea
from src.domain.proyecto import Proyecto

# Crear usuario
usuario = Usuario("juandev", "juan@example.com", "Juan Pérez")
print(usuario)          # @juandev
print(repr(usuario))    # Usuario('juandev', 'juan@example.com')

# Crear tareas
t1 = Tarea("Diseñar base de datos", PrioridadTarea.ALTA, "Modelo ER completo")
t2 = Tarea("Crear endpoints REST", PrioridadTarea.MEDIA)

# Cambiar estado de una tarea
t1.iniciar()
t1.completar()
print(t1)  # [ALTA] Diseñar base de datos (completada)

# Crear proyecto y agregar tareas
proyecto = Proyecto("TaskFlow Backend", usuario, "API REST del sistema")
proyecto.agregar_tarea(t1)
proyecto.agregar_tarea(t2)

# Consultar tareas
pendientes = proyecto.obtener_tareas_pendientes()
altas = proyecto.obtener_tareas_por_prioridad(PrioridadTarea.ALTA)
```

---

## Clases Principales

| Clase | Descripción |
|---|---|
| `Usuario` | Representa un usuario del sistema con username inmutable y email validado. |
| `Tarea` | Tarea individual con estado (PENDIENTE/EN_PROGRESO/COMPLETADA) y prioridad. |
| `Proyecto` | Agrupa tareas bajo un líder; relación de composición con `Tarea`. |
| `PrioridadTarea` | Enum: `ALTA=1`, `MEDIA=2`, `BAJA=3`. |
| `EstadoTarea` | Enum: `PENDIENTE`, `EN_PROGRESO`, `COMPLETADA`. |

---

## E5 — CRUD REST + JWT + Arquitectura en Capas

**Evaluación final**: Implementación completa de API REST con autenticación JWT y arquitectura limpia en capas.

### Características principales

- ✅ **CRUD SQLAlchemy**: Operaciones de usuario, proyecto y tarea (25%)
- ✅ **Autenticación JWT**: Token Bearer con python-jose y Argon2 (25%)
- ✅ **Arquitectura en Capas**: Routers → Services → Repositories → Models (20%)
- ✅ **Validación y Errores**: HTTP 400/401/403/404 con mensajes detallados (15%)
- ✅ **Inyección de Dependencias**: Depends() de FastAPI en protección de rutas (10%)
- ✅ **Patrones OOP**: Generic BaseRepository[T], Service locators, Enums (5%)

### Setup de Evaluación 5

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Aplicar migraciones
python -m alembic upgrade head

# 3. Iniciar servidor
python -m uvicorn api.main:app --reload --port 8000
```

Servidor disponible en `http://127.0.0.1:8000`

**Swagger UI**: `http://127.0.0.1:8000/docs`

### Estructura de la API (E5)

#### Capas implementadas

```
api/
├── routes/           # Routers: HTTP endpoints
│   ├── auth.py       # POST /auth/register, /auth/login
│   ├── usuarios.py   # CRUD de usuarios
│   ├── proyectos.py  # CRUD de proyectos (with JWT)
│   └── tareas.py     # CRUD de tareas (nested)
├── services/         # Business logic
│   ├── usuario_service.py
│   ├── proyecto_service.py
│   └── tarea_service.py
├── repositories/     # Data access (with GenericBaseRepository[T])
│   ├── base.py
│   ├── usuario_repo.py
│   ├── proyecto_repo.py
│   └── tarea_repo.py
├── schemas/          # Pydantic v2 DTO validation
│   ├── usuario.py
│   ├── proyecto.py
│   └── tarea.py
├── auth.py           # JWT: create_access_token, get_current_user
└── main.py           # FastAPI app setup
```

### Ejemplos de uso (curl)

#### 1. Registrar usuario

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"ana","email":"ana@example.com","password":"secret123"}'

# Respuesta (201):
# {
#   "id": 1,
#   "username": "ana",
#   "email": "ana@example.com",
#   "nombre_completo": null,
#   "activo": true
# }
```

#### 2. Login y obtener JWT

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ana&password=secret123"

# Respuesta (200):
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer"
# }
```

#### 3. Crear proyecto (autenticado)

```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST http://localhost:8000/proyectos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Mi Proyecto","descripcion":"Descripción"}'

# Respuesta (201):
# {
#   "id": 1,
#   "nombre": "Mi Proyecto",
#   "descripcion": "Descripción",
#   "usuario_id": 1
# }
```

#### 4. Listar proyectos (autenticado)

```bash
curl -X GET http://localhost:8000/proyectos \
  -H "Authorization: Bearer $TOKEN"

# Respuesta (200): [{"id":1,"nombre":"...","usuario_id":1}]
```

#### 5. Crear tarea en proyecto

```bash
curl -X POST http://localhost:8000/proyectos/1/tareas \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Tarea 1","prioridad":"ALTA","estado":"pendiente"}'

# Respuesta (201):
# {
#   "id": 1,
#   "titulo": "Tarea 1",
#   "prioridad": "ALTA",
#   "estado": "pendiente",
#   "proyecto_id": 1
# }
```

### Códigos HTTP devueltos

| Código | Situación | Ejemplo |
|--------|-----------|---------|
| `200 OK` | Login exitoso, GET exitoso | Token JWT devuelto |
| `201 Created` | Recurso creado | Usuario/Proyecto/Tarea |
| `400 Bad Request` | Validación falla | Email duplicado, campo vacío |
| `401 Unauthorized` | Falta token JWT | Authorization header missing |
| `403 Forbidden` | No es propietario | Acceso a proyecto de otro usuario |
| `404 Not Found` | Recurso no existe | Proyecto ID 999 |

### Seguridad y Validaciones

**Autenticación**: OAuth2PasswordBearer + JWT (HS256, 30 min expiry)

**Hashing**: Argon2id (10+ char passwords)

**Validaciones en models**:
- Username: 3+ caracteres, único
- Email: Formato válido, único
- Proyecto nombre: 3+ caracteres
- Tarea título: 3+ caracteres
- Prioridad: Enum (ALTA, MEDIA, BAJA)
- Estado: Enum (pendiente, en_progreso, completada)

**Protección de rutas**: `Depends(get_current_user)` valida JWT y retorna Usuario

### Migraciones (Alembic)

```bash
# Ver migración actual
alembic current

# Aplicar todas las migraciones
alembic upgrade head

# Ver historial
alembic history --verbose

# Crear nueva migración
alembic revision --autogenerate -m "descripción"
```

**Migraciones incluidas**:
- `001_initial.py`: Tablas usuarios, proyectos, tareas
- `002_add_hashed_password.py`: Columna hashed_password
- `003_add_nombre_completo.py`: Columna nombre_completo

### Base de datos

Usa **SQLite** (`taskflow.db`) en desarrollo, configurable a **PostgreSQL** vía `.env`:

```bash
DATABASE_URL=postgresql+psycopg://user:pass@localhost/taskflow
```

---

## Autor

Desarrollado para **UNAULA — POO II (IF0100)**
