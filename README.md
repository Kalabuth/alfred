```markdown
# 🏠 Backend de Servicios de Domicilio

## 📋 Descripción

Backend en Django 4.2 + DRF para un sistema de **Servicios de Domicilio**, que incluye:

- 🔑 Autenticación vía API-Key (djangorestframework-api-key) y JWT (JSON Web Token)
- 📍 Gestión de **Direcciones**, **Conductores** y **Servicios**
- 🚗 Asignación automática del conductor más cercano
- 🐳 Docker & Docker Compose para despliegue local
- 📄 Documentación de la API con Swagger & ReDoc

---

## 🚀 Características

1. **Direcciones**
   - CRUD completo: `street`, `latitude`, `longitude`
   - Endpoints:
     - `GET /addresses/`
     - `POST /addresses/`
     - `GET /addresses/{id}/`
     - `PUT /addresses/{id}/`

2. **Conductores**
   - CRUD de conductores: nombre, ubicación (`Address`), disponibilidad y rating
   - Acción para actualizar disponibilidad
   - Endpoints:
     - `GET /drivers/`
     - `POST /drivers/`
     - `GET /drivers/{id}/`
     - `POST /drivers/{id}/update_availability/`

3. **Servicios**
   - Solicitud de servicios de domicilio: `client_address`, `driver`, `status` (PENDING/ASSIGNED/COMPLETED), timestamps
   - Asignación automática al conductor más cercano usando fórmula de Haversine
   - Endpoints:
     - `POST /services/`
     - `POST /services/{id}/complete/`
     - `GET /services/`
     - `GET /services/{id}/`

4. **Autenticación y Seguridad**
   - Autenticación JWT (`/auth/login/`, `/auth/register/`)
   - Protección por **API-Key** en todas las vistas usando `ApiKeyProtectedViewMixin`

5. **Documentación**
   - Swagger UI → `/swagger/`
   - ReDoc UI → `/redoc/`

---

## 🔐 Autenticación

### Registro y Login

- `POST /auth/register/` → Crea un nuevo usuario cliente o conductor
- `POST /auth/login/` → Devuelve `access` y `refresh` tokens JWT válidos

**Headers necesarios en endpoints protegidos**:

```
Authorization: Bearer <access_token>
X-API-KEY: <tu_api_key>
```

---

## 🏗️ Estructura del Proyecto

```
project_root/
├── apps/
│   ├── addresses/
│   │   ├── models/address.py
│   │   ├── serializers/address_serializer.py
│   │   ├── views/address_view.py
│   │   ├── services/
│   │   └── methods/
│   ├── drivers/
│   │   ├── models/driver.py
│   │   ├── serializers/driver_serializer.py
│   │   ├── views/driver_view.py
│   │   ├── services/
│   │   └── methods/
│   ├── services/
│   │   ├── models/service.py
│   │   ├── serializers/service_serializer.py
│   │   ├── views/service_view.py
│   │   ├── services/
│   │   └── methods/
│   └── authentication/
│       ├── serializers/
│       ├── views/auth_view.py
│       └── mixins/api_key_protected_view_mixin.py
├── common/
│   ├── utils/
│   ├── constants/
│   ├── exceptions/
│   └── mixins/
├── manage.py
├── Dockerfile
├── docker-compose.yml
```

---

## ⚙️ Configuración de Entorno

`.env` y define tus valores:

```dotenv
# Django
SECRET_KEY=…
DEBUG=True
ALLOWED_HOSTS=localhost

# API-Key
API_KEY_CUSTOM_HEADER=HTTP_X_API_KEY
```

> ⚠️ **Nota importante**: Este proyecto incluyo el archivo `.env` en el repositorio  **solo por ser una prueba técnica**.  
> En un entorno real, **no debe subirse al repositorio**. Se recomienda almacenar esta información sensible en gestores como **1Password**, **Passbolt** o **Vault**.

---

## 🔐 Creación de API Key

Puedes crear una API Key de dos maneras:

### ✅ Opción 1: Desde el panel de administración

1. Ir a: `http://localhost:8000/admin/`
2. Acceder a `API Key > API Keys`
3. Crear una nueva clave y **copiar el valor completo**, ya que no se puede volver a ver.

### 🐚 Opción 2: Desde la terminal

```bash
python manage.py shell
```

```python
from rest_framework_api_key.models import APIKey
api_key, key = APIKey.objects.create_key(name="client")
print("API Key:", key)
```

---

## 🛠️ Instalación Local

1. Clonar el repositorio:

```bash
git clone <repo_url>
cd project
```

2. Instalar dependencias:

```bash
pip install poetry
poetry install
```

3. Aplicar migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```
También puedes simplemente correr el proyecto con Docker, que se encarga automáticamente de todo.

4. Crear superusuario:

```bash
python manage.py createsuperuser
```

5. Crear una API Key (ver sección anterior)

6. Ejecutar servidor:

```bash
python manage.py runserver
```

---

## 🐳 Uso con Docker

### Build y ejecución

```bash
docker compose build
docker compose up -d
```


### Ejecutar pruebas en el contenedor web

```bash
docker compose exec web python manage.py test
```

---

## 🔍 Pruebas

Ejecutar los tests unitarios localmente:

```bash
python manage.py test
```

---

## 📑 Documentación de la API

- Swagger → [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- ReDoc → [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## 🖊️ Calidad de Código

- **Black** (formateo):

```bash
black .
```

- **Ruff** (linting):

```bash
ruff .
```

---
```