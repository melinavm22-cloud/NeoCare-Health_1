# 🔐 Credenciales de Producción - NeoCare

## Credenciales Definidas para Presentación

**Para login:**

- **Email:** `neocare@neocare.com`
- **Contraseña:** `team_sigma`

---

## Crear Usuario en Producción

### Opción 1: Usando Swagger UI

1. Ir a: `[https://tu-dominio.com/docs](https://neocarehealth1.vercel.app/)` 
Usuario - admin@neocare.com
Contraseña - R7M2K9T4B8Q1

### Opción 2: Usando cURL

```bash
curl -X POST https://tu-dominio.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "Admin",
    "email": "admin@neocare.com",
    "password": "R7M2K9T4B8Q1"
  }'
```

---

---

**Proyecto:** NeoCare - Presentación de Prácticas Profesionales
