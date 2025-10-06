# SISTEMA DE ROLES Y PERMISOS - Veterinaria Huellitas

## RESUMEN

Sistema completo de roles y permisos que define qué puede ver y hacer cada tipo de usuario en el sistema.

**Archivos clave:**
- `api/permissions.py` - Definición de permisos por rol
- `api/choices.py` - Definición de roles disponibles
- `api/migrations/0018_datos_iniciales_sistema.py` - Precarga de datos

---

## ROLES DEL SISTEMA

### 1. **Administrador** (`administrador`)
**Control total del sistema**

✅ **Puede hacer TODO**:
- Gestionar usuarios y trabajadores
- Crear veterinarios y asignar horarios
- Ver calendario completo (todos los veterinarios)
- Gestionar citas, servicios, productos
- Aplicar vacunas y ver historial médico
- Generar reportes
- Configurar el sistema

### 2. **Veterinario** (`veterinario`)
**Atiende mascotas y maneja su agenda**

✅ **Puede**:
- Ver SU calendario de citas (solo las propias)
- Completar sus citas
- Aplicar vacunas
- Agregar registros al historial clínico
- Ver información de mascotas y responsables

❌ **NO puede**:
- Crear citas (las crea la recepcionista)
- Ver calendario de otros veterinarios
- Gestionar usuarios, trabajadores
- Modificar servicios o productos
- Cancelar citas

### 3. **Recepcionista** (`recepcionista`)
**Gestiona agendamiento y atención al cliente**

✅ **Puede**:
- Ver calendario completo (TODOS los veterinarios)
- Crear, editar y cancelar citas
- Gestionar mascotas y responsables
- Ver historial de vacunación
- Consultar servicios y productos

❌ **NO puede**:
- Aplicar vacunas
- Modificar historial clínico
- Gestionar usuarios o trabajadores
- Modificar servicios o productos
- Ver reportes o configuración

### 4. **Veterinario Externo** (`veterinario_externo`)
**Solo para referencia histórica**

🔒 **Usuario inactivo** - No puede hacer login

✅ **Uso**:
- Se usa como referencia al registrar mascotas que vienen de otra veterinaria
- Permite registrar vacunas aplicadas externamente
- Mantiene trazabilidad del historial de la mascota

---

## DATOS PRECARGADOS

Al ejecutar `python manage.py migrate`, se crean automáticamente:

### 1. Usuario Administrador
```
Email:    admin@huellitas.com
Password: admin123
Rol:      administrador
```

⚠️ **IMPORTANTE**: Cambiar password después del primer login

### 2. Veterinario Externo
```
Email:    veterinario.externo@sistema.com
Rol:      veterinario_externo
Estado:   Inactivo (no puede hacer login)
```

ID del veterinario se muestra en la consola al migrar.
Usar este ID al registrar vacunas externas.

---

## ENDPOINTS DE AUTENTICACIÓN

### **Login**
```http
POST /api/login/
Content-Type: application/json

{
  "email": "admin@huellitas.com",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLC...",
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

### **Obtener Permisos del Usuario**
```http
GET /api/auth/permisos/
Authorization: Bearer {access_token}
```

**Respuesta:**
```json
{
  "usuario": {
    "id": "uuid",
    "email": "veterinario@example.com",
    "rol": "veterinario",
    "rol_display": "Veterinario",
    "is_staff": false,
    "is_superuser": false
  },
  "permisos": {
    "dashboard": {
      "ver": true
    },
    "citas": {
      "ver": true,
      "crear": false,
      "editar": true,
      "eliminar": false,
      "calendario_general": false,
      "mi_calendario": true
    },
    "vacunas": {
      "ver": true,
      "crear": false,
      "editar": false,
      "eliminar": false,
      "aplicar": true,
      "historial": true
    },
    ...
  },
  "status": "success"
}
```

### **Obtener Información del Usuario**
```http
GET /api/auth/me/
Authorization: Bearer {access_token}
```

**Respuesta:**
```json
{
  "id": "uuid",
  "email": "veterinario@example.com",
  "rol": "veterinario",
  "rol_display": "Veterinario",
  "is_staff": false,
  "trabajador": {
    "id": "uuid",
    "nombres": "Juan",
    "apellidos": "Pérez",
    "email": "veterinario@example.com",
    "telefono": "987654321",
    "documento": "12345678",
    "estado": "Activo"
  },
  "veterinario": {
    "id": "uuid",
    "especialidad": "Medicina General"
  }
}
```

---

## INTEGRACIÓN CON FRONTEND

### **1. Al hacer login:**

```typescript
// Login
const response = await axios.post('/api/login/', {
  email: 'admin@huellitas.com',
  password: 'admin123'
});

// Guardar token
localStorage.setItem('access_token', response.data.access);
localStorage.setItem('refresh_token', response.data.refresh);

// Obtener permisos
const permisosResponse = await axios.get('/api/auth/permisos/', {
  headers: { 'Authorization': `Bearer ${response.data.access}` }
});

// Guardar permisos en estado/contexto
setUsuario(permisosResponse.data.usuario);
setPermisos(permisosResponse.data.permisos);
```

### **2. Controlar visibilidad del menú:**

```typescript
// En el componente del menú
const MenuLateral = () => {
  const { permisos } = useAuth();

  return (
    <nav>
      {permisos.dashboard?.ver && (
        <Link to="/dashboard">Dashboard</Link>
      )}

      {permisos.citas?.ver && (
        <Link to="/citas">Citas</Link>
      )}

      {/* Calendario GENERAL (solo admin y recepcionista) */}
      {permisos.citas?.calendario_general && (
        <Link to="/calendario-recepcion">Calendario General</Link>
      )}

      {/* MI calendario (solo veterinarios) */}
      {permisos.citas?.mi_calendario && (
        <Link to="/mi-calendario">Mi Calendario</Link>
      )}

      {permisos.vacunas?.ver && (
        <Link to="/vacunas">Vacunas</Link>
      )}

      {permisos.usuarios?.ver && (
        <Link to="/usuarios">Usuarios</Link>
      )}
    </nav>
  );
};
```

### **3. Controlar botones de acción:**

```typescript
// En componente de citas
const CitasComponent = () => {
  const { permisos } = useAuth();

  return (
    <div>
      <h1>Citas</h1>

      {/* Botón crear solo para recepcionista y admin */}
      {permisos.citas?.crear && (
        <button onClick={crearNuevaCita}>
          Nueva Cita
        </button>
      )}

      {/* Botón aplicar vacuna solo para veterinario y admin */}
      {permisos.vacunas?.aplicar && (
        <button onClick={aplicarVacuna}>
          Aplicar Vacuna
        </button>
      )}
    </div>
  );
};
```

---

## TABLA DE PERMISOS COMPLETA

| Módulo | Admin | Veterinario | Recepcionista |
|--------|-------|-------------|---------------|
| **Dashboard** | ✅ Ver | ✅ Ver | ✅ Ver |
| **Citas - Ver** | ✅ | ✅ | ✅ |
| **Citas - Crear** | ✅ | ❌ | ✅ |
| **Citas - Editar** | ✅ | ✅ (solo completar) | ✅ |
| **Citas - Cancelar** | ✅ | ❌ | ✅ |
| **Calendario General** | ✅ | ❌ | ✅ |
| **Mi Calendario** | ✅ | ✅ | ❌ |
| **Mascotas - Ver** | ✅ | ✅ | ✅ |
| **Mascotas - Crear** | ✅ | ❌ | ✅ |
| **Mascotas - Editar** | ✅ | ❌ | ✅ |
| **Responsables - Ver** | ✅ | ✅ | ✅ |
| **Responsables - Crear** | ✅ | ❌ | ✅ |
| **Vacunas - Ver** | ✅ | ✅ | ✅ |
| **Vacunas - Aplicar** | ✅ | ✅ | ❌ |
| **Historial Clínico - Ver** | ✅ | ✅ | ✅ |
| **Historial Clínico - Crear** | ✅ | ✅ | ❌ |
| **Servicios - Ver** | ✅ | ✅ | ✅ |
| **Servicios - Gestionar** | ✅ | ❌ | ❌ |
| **Productos - Ver** | ✅ | ✅ | ✅ |
| **Productos - Gestionar** | ✅ | ❌ | ❌ |
| **Usuarios - Ver** | ✅ | ❌ | ❌ |
| **Usuarios - Gestionar** | ✅ | ❌ | ❌ |
| **Reportes** | ✅ | ❌ | ❌ |
| **Configuración** | ✅ | ❌ | ❌ |

---

## TESTING

### **Ejecutar test del sistema:**
```bash
python test_sistema_roles.py
```

Verifica:
- ✅ Usuario admin creado correctamente
- ✅ Veterinario externo configurado
- ✅ Permisos asignados correctamente
- ✅ Métodos de verificación de permisos funcionan

---

## CREAR NUEVOS USUARIOS

El admin debe crear los usuarios desde el sistema:

### **1. Crear Trabajador y Usuario:**
```http
POST /api/trabajadores/registro/
Authorization: Bearer {admin_token}

{
  "nombres": "María",
  "apellidos": "López",
  "email": "maria.lopez@huellitas.com",
  "telefono": "987654321",
  "tipodocumento": "uuid-dni",
  "documento": "87654321",
  "rol": "recepcionista",
  "password": "temporal123"
}
```

### **2. Si es veterinario, crear registro adicional:**
```http
POST /api/veterinarios/
Authorization: Bearer {admin_token}

{
  "trabajador": "uuid-del-trabajador",
  "especialidad": "uuid-especialidad"
}
```

---

## MODIFICAR PERMISOS

Para modificar permisos, editar `api/permissions.py`:

```python
PERMISOS = {
    Rol.VETERINARIO: {
        'citas': {
            'ver': True,
            'crear': True,  # Cambiar de False a True
            ...
        }
    }
}
```

No requiere migración, los cambios aplican inmediatamente.

---

## SEGURIDAD

### **Buenas prácticas:**

1. ✅ Cambiar password del admin después del primer login
2. ✅ Usar HTTPS en producción
3. ✅ Configurar `ALLOWED_HOSTS` en settings.py
4. ✅ Cambiar `SECRET_KEY` en producción
5. ✅ Configurar `DEBUG = False` en producción
6. ✅ Restringir `CORS_ALLOWED_ORIGINS`

### **Tokens JWT:**
- Access token: 60 minutos
- Refresh token: 1 día
- Configurar en `settings.py` > `SIMPLE_JWT`

---

## TROUBLESHOOTING

### **"Usuario no puede hacer login"**
- Verificar que `is_active = True`
- Veterinario externo tiene `is_active = False` (no debe hacer login)

### **"No tengo permisos para X acción"**
- Verificar rol del usuario: `GET /api/auth/me/`
- Verificar permisos del rol: `GET /api/auth/permisos/`
- Revisar `api/permissions.py`

### **"No aparece el veterinario externo"**
- ID se muestra al ejecutar `python manage.py migrate`
- También en: `GET /api/veterinario-externo/`

---

**Sistema implementado y listo para producción** ✅
