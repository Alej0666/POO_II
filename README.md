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
