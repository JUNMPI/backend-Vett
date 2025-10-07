# Aclaraciones para el Frontend - Sistema de Login y Permisos

## ✅ Estado Actual del Backend

Los endpoints de permisos **YA ESTÁN IMPLEMENTADOS** y funcionando:

```
✅ GET  /api/auth/permisos/  → Retorna permisos del usuario autenticado
✅ GET  /api/auth/me/        → Retorna información completa del usuario
✅ POST /api/login/          → Login con JWT
✅ POST /api/refresh/        → Refresh token
```

---

## 📋 Respuestas Reales de los Endpoints

### 1. POST /api/login/

**Request:**
```json
{
  "email": "admin@huellitas.com",
  "password": "admin123"
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. GET /api/auth/permisos/

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200) - Administrador:**
```json
{
  "rol": "administrador",
  "permisos": {
    "dashboard": {
      "ver": true
    },
    "citas": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true,
      "calendario_general": true,
      "mi_calendario": true
    },
    "mascotas": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true
    },
    "responsables": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true
    },
    "vacunas": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true,
      "aplicar": true,
      "historial": true
    },
    "historial_clinico": {
      "ver": true,
      "crear": true,
      "editar": true
    },
    "servicios": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true
    },
    "productos": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true
    },
    "usuarios": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true
    },
    "trabajadores": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true
    },
    "veterinarios": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true,
      "horarios": true,
      "slots": true
    },
    "reportes": {
      "ver": true,
      "generar": true
    },
    "configuracion": {
      "ver": true,
      "editar": true
    }
  }
}
```

**Response (200) - Veterinario:**
```json
{
  "rol": "veterinario",
  "permisos": {
    "dashboard": {
      "ver": false
    },
    "citas": {
      "ver": true,
      "crear": false,
      "editar": true,
      "eliminar": false,
      "calendario_general": false,
      "mi_calendario": true
    },
    "mascotas": {
      "ver": true,
      "crear": false,
      "editar": false,
      "eliminar": false
    },
    "responsables": {
      "ver": true,
      "crear": false,
      "editar": false,
      "eliminar": false
    },
    "vacunas": {
      "ver": true,
      "crear": false,
      "editar": false,
      "eliminar": false,
      "aplicar": true,
      "historial": true
    },
    "historial_clinico": {
      "ver": true,
      "crear": true,
      "editar": true
    },
    "servicios": {
      "ver": true,
      "crear": false,
      "editar": false,
      "eliminar": false
    },
    "productos": {
      "ver": true,
      "crear": false,
      "editar": false,
      "eliminar": false
    },
    "usuarios": {
      "ver": false
    },
    "trabajadores": {
      "ver": false
    },
    "veterinarios": {
      "ver": false
    },
    "reportes": {
      "ver": true,
      "generar": false
    },
    "configuracion": {
      "ver": false
    }
  }
}
```

**Response (200) - Recepcionista:**
```json
{
  "rol": "recepcionista",
  "permisos": {
    "dashboard": {
      "ver": false
    },
    "citas": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true,
      "calendario_general": true,
      "mi_calendario": false
    },
    "mascotas": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true
    },
    "responsables": {
      "ver": true,
      "crear": true,
      "editar": true,
      "eliminar": true
    },
    "vacunas": {
      "ver": true,
      "crear": false,
      "editar": false,
      "eliminar": false,
      "aplicar": false,
      "historial": true
    },
    "historial_clinico": {
      "ver": true,
      "crear": false,
      "editar": false
    },
    "servicios": {
      "ver": true,
      "crear": false,
      "editar": false,
      "eliminar": false
    },
    "productos": {
      "ver": true,
      "crear": false,
      "editar": false,
      "eliminar": false
    },
    "usuarios": {
      "ver": false
    },
    "trabajadores": {
      "ver": false
    },
    "veterinarios": {
      "ver": false
    },
    "reportes": {
      "ver": false
    },
    "configuracion": {
      "ver": false
    }
  }
}
```

### 3. GET /api/auth/me/

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200) - Administrador:**
```json
{
  "id": "074e2f8a-43fb-458e-8827-232c0453c1dc",
  "email": "admin@huellitas.com",
  "rol": "administrador",
  "trabajador": null
}
```

**Response (200) - Veterinario:**
```json
{
  "id": "uuid-del-usuario",
  "email": "veterinario@huellitas.com",
  "rol": "veterinario",
  "trabajador": {
    "id": "uuid-del-trabajador",
    "nombres": "Juan Carlos",
    "apellidos": "Pérez López",
    "tipo_documento": "DNI",
    "numero_documento": "12345678",
    "telefono": "987654321",
    "direccion": "Av. Principal 123"
  },
  "veterinario": {
    "id": "uuid-del-veterinario",
    "especialidad": "Cirugía",
    "anios_experiencia": 5
  }
}
```

**Response (200) - Recepcionista:**
```json
{
  "id": "uuid-del-usuario",
  "email": "recepcion@huellitas.com",
  "rol": "recepcionista",
  "trabajador": {
    "id": "uuid-del-trabajador",
    "nombres": "María",
    "apellidos": "González",
    "tipo_documento": "DNI",
    "numero_documento": "87654321",
    "telefono": "912345678",
    "direccion": "Jr. Comercio 456"
  }
}
```

---

## ⚠️ IMPORTANTES: Campos que NO Existen

### ❌ NO existe el campo `activo` en Usuario

El modelo `Usuario` **NO tiene** el campo `activo`. Si el usuario puede hacer login, está activo.

**❌ NO hacer esto:**
```typescript
if (user.activo) { // ← Este campo NO EXISTE
  // ...
}
```

**✅ Hacer esto:**
```typescript
// Si el usuario obtuvo token, está activo
if (user && user.id) {
  // Usuario válido
}
```

### ❌ NO existe el campo `es_superusuario`

**❌ NO hacer esto:**
```typescript
if (user.es_superusuario) { // ← Este campo NO EXISTE
  // ...
}
```

**✅ Hacer esto:**
```typescript
if (user.rol === 'administrador') {
  // Es admin
}
```

### ⚠️ Veterinario NO tiene algunos campos

El modelo `Veterinario` actual **NO tiene**:
- `registro_profesional`
- `anios_experiencia` (existe en la respuesta `/api/auth/me/` pero puede estar vacío)

---

## 🔄 Flujo Correcto de Login

### Paso 1: Login
```typescript
const response = await axios.post('/api/login/', {
  email: 'admin@huellitas.com',
  password: 'admin123'
});

// Guardar tokens
localStorage.setItem('access', response.data.access);
localStorage.setItem('refresh', response.data.refresh);

// Configurar header por defecto
axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
```

### Paso 2: Cargar Permisos
```typescript
try {
  const permisosResponse = await axios.get('/api/auth/permisos/');
  localStorage.setItem('permisos', JSON.stringify(permisosResponse.data));
} catch (error) {
  console.warn('No se pudieron cargar permisos, usando fallback');
  // ⚠️ Tu sistema de fallback está bien aquí
}
```

### Paso 3: Cargar Info del Usuario
```typescript
try {
  const userResponse = await axios.get('/api/auth/me/');
  localStorage.setItem('user', JSON.stringify(userResponse.data));
} catch (error) {
  console.warn('No se pudo cargar info del usuario, usando fallback');
  // ⚠️ Tu sistema de fallback está bien aquí
}
```

---

## 🛡️ Tu Sistema de Fallback está Correcto

Tu estrategia es **correcta**:

```typescript
// ✅ Si los endpoints existen → sistema completo
// ⚠️ Si los endpoints NO existen → login funciona, acceso temporal
// ❌ Si credenciales incorrectas → login falla
```

**PERO**: Como los endpoints **YA EXISTEN**, el fallback solo se activará si:
1. Hay un error de red
2. El servidor está caído
3. Hay un problema de CORS

En condiciones normales, siempre obtendrá permisos de la BD.

---

## 📝 Actualización de Tipos TypeScript

### Interfaz PermisosUsuario

```typescript
interface PermisosUsuario {
  rol: 'administrador' | 'veterinario' | 'recepcionista' | 'inventario' | 'veterinario_externo' | 'Responsable';
  permisos: {
    dashboard?: {
      ver: boolean;
    };
    citas?: {
      ver: boolean;
      crear: boolean;
      editar: boolean;
      eliminar: boolean;
      calendario_general: boolean;
      mi_calendario: boolean;
    };
    mascotas?: {
      ver: boolean;
      crear: boolean;
      editar: boolean;
      eliminar: boolean;
    };
    responsables?: {
      ver: boolean;
      crear: boolean;
      editar: boolean;
      eliminar: boolean;
    };
    vacunas?: {
      ver: boolean;
      crear: boolean;
      editar: boolean;
      eliminar: boolean;
      aplicar: boolean;
      historial: boolean;
    };
    historial_clinico?: {
      ver: boolean;
      crear: boolean;
      editar: boolean;
    };
    servicios?: {
      ver: boolean;
      crear: boolean;
      editar: boolean;
      eliminar: boolean;
    };
    productos?: {
      ver: boolean;
      crear: boolean;
      editar: boolean;
      eliminar: boolean;
    };
    usuarios?: {
      ver: boolean;
      crear?: boolean;
      editar?: boolean;
      eliminar?: boolean;
    };
    trabajadores?: {
      ver: boolean;
      crear?: boolean;
      editar?: boolean;
      eliminar?: boolean;
    };
    veterinarios?: {
      ver: boolean;
      crear?: boolean;
      editar?: boolean;
      eliminar?: boolean;
      horarios?: boolean;
      slots?: boolean;
    };
    reportes?: {
      ver: boolean;
      generar?: boolean;
    };
    configuracion?: {
      ver: boolean;
      editar?: boolean;
    };
  };
}
```

### Interfaz UsuarioCompleto

```typescript
interface Trabajador {
  id: string;
  nombres: string;
  apellidos: string;
  tipo_documento: string;
  numero_documento: string;
  telefono: string;
  direccion: string;
}

interface Veterinario {
  id: string;
  especialidad: string;
  anios_experiencia?: number; // Puede no estar presente
}

interface UsuarioCompleto {
  id: string;
  email: string;
  rol: 'administrador' | 'veterinario' | 'recepcionista' | 'inventario';
  trabajador: Trabajador | null; // null si es admin
  veterinario?: Veterinario; // Solo si es veterinario
  // ❌ NO INCLUIR: activo, es_superusuario
}
```

---

## 🧪 Cómo Probar

### 1. Login como Admin
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@huellitas.com", "password": "admin123"}'
```

### 2. Obtener Permisos
```bash
curl http://localhost:8000/api/auth/permisos/ \
  -H "Authorization: Bearer <tu_token>"
```

### 3. Obtener Info Usuario
```bash
curl http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer <tu_token>"
```

---

## 🎯 Resumen para el Frontend

| ✅ Correcto | ❌ Incorrecto |
|------------|--------------|
| `user.rol === 'administrador'` | `user.es_superusuario` |
| `if (user && user.id)` | `if (user.activo)` |
| `permisos.permisos.dashboard.ver` | `permisos.dashboard` (sin `.permisos`) |
| `user.trabajador?.nombres` | `user.trabajador.nombre` |
| `user.trabajador?.apellidos` | `user.trabajador.apellido` |

---

## 🔐 Credenciales de Prueba

```
Email: admin@huellitas.com
Contraseña: admin123
Rol: administrador
```

**⚠️ IMPORTANTE**: Cambiar esta contraseña en producción.

---

## 📞 Soporte

Si el frontend encuentra errores:

1. **401 Unauthorized**: Token inválido o expirado → usar `/api/refresh/`
2. **403 Forbidden**: Usuario sin permisos para esa acción
3. **404 Not Found**: Endpoint no existe (revisar URL)
4. **500 Internal Server Error**: Error del backend (revisar logs)

Los endpoints **YA ESTÁN FUNCIONANDO** - puedes verificarlo haciendo requests con curl o Postman.
