# NeoCare Backend API

Backend seguro para aplicación Kanban con autenticación JWT, control de acceso y auditoría.

## Características

- **Autenticación JWT** con tokens de acceso y refresh
- **Hashing seguro** con bcrypt
- **Control de acceso** basado en ownership de recursos
- **CRUD completo** para Boards, Lists y Cards
- **Logging estructurado** y auditoría de eventos
- **Health checks** y métricas
- **CORS configurado** para integración con frontend
- **Rate limiting** básico
- **Validaciones robustas** con Pydantic

## Requisitos

- Python 3.9+
- PostgreSQL 12+

## Instalación

1. **Clonar repositorio**
```bash
cd NeoCare-MVBackend
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp env.example .env
```

Editar `.env` con tus credenciales:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/neocare
SECRET_KEY=tu-clave-secreta-minimo-32-caracteres
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
BCRYPT_ROUNDS=12
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
```

5. **Crear base de datos**
```bash
createdb neocare
```

6. **Ejecutar migraciones**
```bash
cd backend
alembic upgrade head
```

7. **Iniciar servidor**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Documentación API

Una vez iniciado el servidor, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints principales

### Autenticación
- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Login y obtener tokens
- `POST /auth/refresh` - Renovar access token
- `POST /auth/logout` - Logout (requiere auth)
- `GET /auth/me` - Obtener usuario actual (requiere auth)

### Boards
- `GET /boards/` - Listar boards del usuario
- `POST /boards/` - Crear board
- `GET /boards/{id}` - Obtener board específico
- `PUT /boards/{id}` - Actualizar board
- `DELETE /boards/{id}` - Eliminar board

### Lists
- `GET /lists/board/{board_id}` - Listar listas de un board
- `POST /lists/` - Crear lista
- `PUT /lists/{id}` - Actualizar lista
- `DELETE /lists/{id}` - Eliminar lista

### Cards
- `GET /cards/` - Listar tarjetas del usuario
- `POST /cards/` - Crear tarjeta
- `PUT /cards/{id}` - Actualizar tarjeta
- `DELETE /cards/{id}` - Eliminar tarjeta

### Health
- `GET /health/` - Health check público
- `GET /health/db` - Health check de base de datos
- `GET /health/metrics` - Métricas del sistema (requiere auth)

## Seguridad

### Autenticación
- Tokens JWT con expiración configurable
- Refresh tokens para renovación segura
- Bcrypt para hashing de contraseñas (12 rounds)
- Validación de fortaleza de contraseñas

### Autorización
- Todos los endpoints protegidos requieren Bearer token
- Validación de ownership en todos los recursos
- Prevención de IDOR (Insecure Direct Object Reference)

### Protecciones adicionales
- CORS configurado
- Rate limiting básico (100 req/min por IP)
- Logging de intentos de autenticación
- Headers de seguridad en responses

## Logging y Auditoría

Los logs se almacenan en `logs/app_YYYYMMDD.log`:
- Intentos de login (exitosos y fallidos)
- Registro de nuevos usuarios
- Acceso a recursos
- Errores y excepciones
- Tiempo de procesamiento de requests

## Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Con cobertura
pytest --cov=backend --cov-report=html
```

## Despliegue

### Variables de entorno en producción
- Cambiar `SECRET_KEY` a valor aleatorio fuerte
- Configurar `DATABASE_URL` con credenciales de producción
- Ajustar `CORS_ORIGINS` a dominios permitidos
- Establecer `ENVIRONMENT=production`
- Incrementar `BCRYPT_ROUNDS` si es posible (14-16)

### Recomendaciones
- Usar HTTPS obligatorio
- Implementar rate limiting robusto (Redis + slowapi)
- Configurar backup automático de base de datos
- Monitoreo con Prometheus/Grafana
- Logs centralizados (ELK, CloudWatch, etc.)

## Migraciones

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

## Estructura del proyecto

```
backend/
├── core/
│   ├── config.py          # Configuración centralizada
│   ├── logging_config.py  # Setup de logging
│   └── security.py        # Utilidades de seguridad
├── models/
│   ├── user.py
│   ├── board.py
│   ├── list.py
│   └── card.py
├── routers/
│   ├── auth.py           # Autenticación
│   ├── boards.py         # CRUD boards
│   ├── lists.py          # CRUD lists
│   ├── cards.py          # CRUD cards
│   └── health.py         # Health checks
├── schemas/
│   └── card.py           # Schemas Pydantic
└── main.py               # Aplicación FastAPI
```

## Integración con Frontend

### Headers requeridos
```javascript
headers: {
  'Authorization': `Bearer ${accessToken}`,
  'Content-Type': 'application/json'
}
```

### Manejo de tokens
1. Guardar `access_token` y `refresh_token` del login
2. Incluir `access_token` en header Authorization
3. Si recibe 401, usar `refresh_token` en `/auth/refresh`
4. Si refresh falla, redirigir a login

### Ejemplo de llamada
```javascript
const response = await fetch('http://localhost:8000/boards/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
  }
});
```

## Soporte

Para problemas o preguntas, revisar logs en `logs/` o contactar al equipo de desarrollo.
