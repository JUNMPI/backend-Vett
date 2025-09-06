# 🐍 DJANGO BACKEND - CONTEXTO PARA CLAUDE

## PROMPT BASE PARA DJANGO CLAUDE
```
Eres un experto Django desarrollando el backend de una clínica veterinaria.

**PROYECTO:** Sistema Veterinaria Huellitas
**TECH STACK:** Django 5.2.1 + PostgreSQL + JWT
**FRONTEND:** Angular 19 en localhost:56070
**BACKEND:** Django en localhost:8000

**CONFIGURACIÓN ACTUAL:**
- Base de datos: PostgreSQL "Huellitas"
- Usuario: huellitas / Password: 1234567
- AUTH_USER_MODEL: 'api.Usuario'
- JWT con rest_framework_simplejwt

**CORS CONFIGURADO:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:56070",
    "http://127.0.0.1:56070",
]
CORS_ALLOW_ALL_ORIGINS = True
```

**FORMATO LOGIN RESPONSE (NO CAMBIAR):**
```json
{
    "access": "jwt_token",
    "refresh": "jwt_token", 
    "usuario_id": "uuid",
    "email": "user@email.com",
    "rol": "Veterinario",
    "trabajador_id": "uuid",
    "nombres": "string",
    "apellidos": "string"
}
```

**MODELOS PRINCIPALES:**
- Usuario (customizado)
- Trabajador → Veterinario
- Mascota + Responsable
- Cita, Servicio, Especialidad
- Inventario

Mantén consistencia con esta estructura existente.
```

---

## USO EN FUTURAS SESIONES:

**Para Angular:** "Lee CLAUDE.md"
**Para Django:** "Lee DJANGO_CONTEXT.md y usa el prompt base"