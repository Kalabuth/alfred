
## Descripción  
Backend en Django 4.2 + DRF para un sistema de **Servicios de Domicilio**, que incluye:

- 🔑 Autenticación vía API-Key (djangorestframework-api-key) y JWT (JSON Web Token) 
- 📍 Gestión de **Direcciones**, **Conductores** y **Servicios**  
- 🚗 Asignación automática del conductor más cercano  
- 🐳 Docker & Docker Compose para despliegue local  
- 📄 Documentación de la API con Swagger & ReDoc  

---

## 🚀 Características

1. **Direcciones**  
   - CRUD completo de direcciones: `street`, `latitude`, `longitude`.  
   - Endpoints:  
     - GET /addresses/  
     - POST /addresses/  
     - GET /addresses/{id}/  
     - PUT /addresses/{id}/  

2. **Conductores**  
   - CRUD de conductores con nombre, ubicación (`Address`), disponibilidad y rating.  
   - Action custom para actualizar disponibilidad.  
   - Endpoints:  
     - GET /drivers/  
     - POST /drivers/  
     - GET /drivers/{id}/  
     - POST /drivers/{id}/update_availability/  

3. **Servicios**  
   - Modelado de solicitudes de domicilio: `client_address`, `driver`, `status` (PENDING/ASSIGNED/COMPLETED), tiempos y marcas de fecha.  
   - Asignación automática al conductor más cercano (fórmula de Haversine).  
   - Endpoint para crear y asignar:  
     - POST /services/  
   - Action custom para completar servicio:  
     - POST /services/{id}/complete/  
   - Listar y recuperar:  
     - GET /services/  
     - GET //services/{id}/  


4. **Autenticación & Seguridad**  
   - Protección **API-Key** en todos los ViewSets mediante `ApiKeyProtectedViewMixin`.  

5. **Documentación de la API**  
   - **Swagger UI** → `/swagger/`  
   - **ReDoc UI**  → `/redoc/`  

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
│   │   ├── date_utils.py
│   │   ├── validators.py
│   │   └── http_client.py
│   ├── constants/
│   ├── exceptions/
│   └── mixins/
├── manage.py
├── Dockerfile
├── docker-compose.yml
```

---

## ⚙️ Configuración de Entorno

Copia `env.example` → `.env` y define:

```dotenv
# Django
SECRET_KEY=…
DEBUG=True
ALLOWED_HOSTS=localhost


# API-Key
API_KEY_CUSTOM_HEADER=HTTP_X_API_KEY


```

---

## 🛠️ Instalación Local

1. **Clonar repo**  
   ```bash
   git clone <repo_url>
   cd project
   ```

2. **Instalar dependencias**  
   ```bash
   -pip install poetry
   -poetry install
   ```

3. **Migraciones**  
   ```bash
   python manage.py migrate
   ```

4. **Crear superusuario**  
   ```bash
   python manage.py createsuperuser
   ```

5. **Crear API Key**  
   ```bash
   python manage.py shell
   >>> from rest_framework_api_key.models import APIKey
   >>> _, key = APIKey.objects.create_key(name="client")
   >>> print(key)
   ```

6. **Correr servidor**  
   ```bash
   python manage.py runserver
   ```

---

## 🐳 Con Docker

```bash
docker compose build
docker compose up -d
```

- **web**: Django + Gunicorn (0.0.0.0:8000)  
- **db**: PostgreSQL  

---

## 📑 Documentación de la API

- **Swagger UI** → `http://localhost:8000/swagger/`  
- **ReDoc UI**  → `http://localhost:8000/redoc/`  

---

## 🔒 Seguridad

- **API-Key** en todas las vistas.  
---

## 🔍 Pruebas

```bash
python manage.py test
```

---

## 🖊️ Calidad de Código

- **Black**  
  ```bash
  black . 
  ```

- **Ruff**  
  ```bash
  ruff . 
  ```

---