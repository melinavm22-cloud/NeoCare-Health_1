
VISTA MIS_HORAS

## PERMISOS 🔐

### Acceso permitido
- Solo el usuario autenticado puede consultar sus propios worklogs semanales.
- El token JWT es obligatorio en todas las peticiones.
- El backend filtra automáticamente por user_id, sin permitir acceso a registros ajenos.

### Acceso denegado. 
- Usuarios sin token → 401 Unauthorized
- Intento de acceder a worklogs de otro usuario → 403 Forbidden (o filtrado silencioso según implementación)
- Token expirado → 401 Unauthorized

### Reglas adicionales
- Un usuario solo puede editar o eliminar sus propios worklogs.
- Los worklogs deben pertenecer a tarjetas accesibles por el usuario (según permisos del tablero).


## CASOS LÍMITE ⚠️

### Semana sin registros.
- Respuesta válida con totales en cero y lista vacía.

### Notas vacías  
- Campo opcional, puede venir como null o cadena vacía.

### Horas mínimas  
- El backend permite valores > 0 (recomendado: 0.25).

### Fecha fuera de la semana solicitada  
- El backend no la incluirá en la respuesta.

### Semana mal formateada (YYYY-WW incorrecto)  
- 422 Unprocessable Entity

### Token expirado o inválido  
- 401 Unauthorized

### Worklog de otro usuario  
- No aparece en la respuesta (filtrado automático).


## CÓMO TESTEAR WORKLOGS CON POSTMAN 🧪

### Obtener token.
- Enviar POST en:
POST /auth/login

- Body del mensaje en JSON:
{
  "email": "admin@neocare.com",
  "password": "admin123"
}

- Copiar el token JWT de la respuesta.


### Consultar worklogs semanales.
- Crear nueva petición GET en:
http://localhost:8000/users/me/worklogs?week=2025-04

- En Headers:
Authorization: Bearer <token>

- Enviar y verificar:
· Lista de worklogs
· Totales diarios
· Total semanal


### Crear un worklog.
- En la siguiente dirección:
POST /cards/{card_id}/worklogs

- Body del mensaje en JSON:
{
  "date": "2025-01-20",
  "hours": 2.5,
  "note": "Revisión de endpoints"
}

### Editar un worklog.
- En la siguiente dirección:
PATCH /worklogs/{id}

- Body del mensaje en JSON:
{
  "hours": 3,
  "note": "Ajuste tras pruebas"
}

### Eliminar un worklog en:
DELETE /worklogs/{id}
