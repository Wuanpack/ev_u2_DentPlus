# 🦷 Sistema de Afiliados DentPlus

Sistema web para la gestión de pacientes afiliados de la clínica dental DentPlus. Permite registrar, consultar, editar y desactivar afiliados, además de simular descuentos según el tipo de membresía de cada paciente.

Desarrollado con arquitectura **MVC** usando Python, Flask y SQLite.

---

## Stack Tecnológico

- **Lenguaje:** Python 3.13
- **Framework:** Flask
- **Base de datos:** SQLite (incluido en Python, sin instalación adicional)
- **Motor de plantillas:** Jinja2 (incluido en Flask)
- **Estilos:** Bootstrap 5

---

## Arquitectura MVC

```
ev_u2_DentPlus/
├── app.py                          # Punto de entrada — crea la app y registra rutas
├── models/
│   └── afiliado.py                 # Model — lógica de datos y consultas SQL
├── controllers/
│   └── afiliado_controller.py      # Controller — coordinación HTTP y lógica de rutas
├── templates/
│   ├── layout.html                 # Vista base compartida (navbar, Bootstrap)
│   └── afiliados/
│       ├── index.html              # Vista — listado de afiliados
│       ├── detalle.html            # Vista — detalle + simulador de descuento
│       └── formulario.html        # Vista — formulario de crear/editar
└── requirements.txt
```

| Capa | Archivo | Responsabilidad |
|---|---|---|
| Model | `models/afiliado.py` | Acceso a base de datos y lógica de negocio |
| View | `templates/` | Presentación HTML con Jinja2 |
| Controller | `controllers/afiliado_controller.py` | Manejo de peticiones HTTP |
| Router | `app.py` + Blueprint | Mapeo de URLs a funciones |

---

## Modelo de Datos

### Tabla `afiliados`

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | INTEGER | Identificador único, generado automáticamente |
| `firstName` | TEXT | Nombre del afiliado |
| `lastName` | TEXT | Apellido del afiliado |
| `email` | TEXT | Correo electrónico (único) |
| `membershipType` | TEXT | Tipo de membresía: `silver`, `gold` o `platinum` |
| `estado` | INTEGER | Estado del afiliado: `1` activo, `0` inactivo |

### Tipos de membresía y descuentos

| Tipo | Descuento |
|---|---|
| Silver | 5% |
| Gold | 10% |
| Platinum | 20% |

> El campo `estado` implementa **borrado lógico (soft delete)** — los afiliados nunca se eliminan físicamente de la base de datos, solo se desactivan.

---

## Funcionalidades

- Listar todos los afiliados activos
- Ver detalle de un afiliado
- Crear un nuevo afiliado
- Editar los datos de un afiliado existente
- Desactivar un afiliado (soft delete)
- **Simulador de descuento** en la vista de detalle: ingresa un monto de tratamiento y calcula el precio final según la membresía del afiliado

---

## Instalación y Ejecución

### Prerrequisitos

- Python 3.10 o superior
- pip

### Pasos

1. Clona el repositorio:

```bash
git clone https://github.com/Wuanpack/ev_u2_DentPlus.git
cd ev_u2_DentPlus
```

2. Crea y activa el entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install flask
```

4. Inicia el servidor:

```bash
python3 app.py
```

La base de datos `dentplus.db` se crea automáticamente al iniciar el servidor por primera vez.

5. Abre el navegador en:

```
http://localhost:5000
```

---

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/afiliados` | Listado de afiliados activos |
| GET | `/afiliados/nuevo` | Formulario de creación |
| POST | `/afiliados/nuevo` | Crear nuevo afiliado |
| GET | `/afiliados/<id>` | Detalle de un afiliado |
| GET | `/afiliados/<id>?monto=80000` | Detalle con simulador de descuento |
| GET | `/afiliados/<id>/editar` | Formulario de edición |
| POST | `/afiliados/<id>/editar` | Guardar cambios del afiliado |
| POST | `/afiliados/<id>/desactivar` | Desactivar afiliado |

---

## Autor

- **Nombre:** Alonso García Espinoza
- **Institución:** IP San Sebastián
- **Ramo:** Desarrollo de Software Web I — Evaluación Unidad 2
- **Docente:** Boris Belmar Muñoz