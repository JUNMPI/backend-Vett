# Guía Frontend - Sistema de Roles y Permisos

## Índice
1. [Descripción General](#descripción-general)
2. [Roles del Sistema](#roles-del-sistema)
3. [Endpoints Disponibles](#endpoints-disponibles)
4. [Estructura de Permisos](#estructura-de-permisos)
5. [Implementación en Frontend](#implementación-en-frontend)
6. [Ejemplos de Uso](#ejemplos-de-uso)
7. [Casos Especiales](#casos-especiales)

---

## Descripción General

El sistema de roles y permisos controla qué puede ver y hacer cada usuario en el sistema. Cada usuario tiene asignado **un rol** que determina sus permisos.

### Flujo de Autenticación y Permisos

```
1. Usuario hace login → POST /api/login/
2. Backend retorna token JWT + datos básicos del usuario
3. Frontend guarda token en localStorage/sessionStorage
4. Frontend consulta permisos → GET /api/auth/permisos/
5. Frontend consulta datos completos → GET /api/auth/me/
6. Frontend renderiza UI según permisos del usuario
```

---

## Roles del Sistema

### 1. ADMINISTRADOR (`'administrador'`)
- **Acceso total** al sistema
- Puede gestionar usuarios, trabajadores, veterinarios
- Puede configurar el sistema
- Ve calendario de todos los veterinarios
- Genera reportes

### 2. VETERINARIO (`'veterinario'`)
- **Acceso médico** limitado
- Ve y completa sus propias citas
- Aplica vacunas y gestiona historial clínico
- **NO puede**: crear citas, ver otros veterinarios, gestionar usuarios
- Solo ve su propio calendario

### 3. RECEPCIONISTA (`'recepcionista'`)
- **Gestión de citas y clientes**
- Crea, edita y cancela citas
- Gestiona mascotas y responsables
- Ve calendario de **todos** los veterinarios
- **NO puede**: aplicar vacunas, gestionar usuarios, configurar sistema

### 4. RESPONSABLE (`'Responsable'`)
- **NO TIENE ACCESO AL SISTEMA**
- Es solo un registro interno para dueños de mascotas
- No pueden hacer login ni ver ningún módulo
- Se usa únicamente para asociar mascotas con sus dueños

### 5. VETERINARIO_EXTERNO (`'veterinario_externo'`)
- **Usuario especial del sistema**
- Usado para registro de vacunas aplicadas en otras clínicas
- Permite mantener historial completo de vacunación
- No es un rol para usuarios reales

### 6. INVENTARIO (`'inventario'`)
- **Pendiente de implementación**
- Futuro: gestión de productos y stock

---

## Endpoints Disponibles

### 1. Obtener Permisos del Usuario Autenticado

**GET** `/api/auth/permisos/`

**Headers requeridos:**
```http
Authorization: Bearer <token_jwt>
```

**Respuesta exitosa (200):**
```json
{
  "rol": "recepcionista",
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

### 2. Obtener Información del Usuario Autenticado

**GET** `/api/auth/me/`

**Headers requeridos:**
```http
Authorization: Bearer <token_jwt>
```

**Respuesta exitosa (200) - Veterinario:**
```json
{
  "id": "uuid-del-usuario",
  "email": "veterinario@huellitas.com",
  "rol": "veterinario",
  "activo": true,
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
    "especialidad": "Cirugía"
  }
}
```

**Respuesta exitosa (200) - Recepcionista:**
```json
{
  "id": "uuid-del-usuario",
  "email": "recepcion@huellitas.com",
  "rol": "recepcionista",
  "activo": true,
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

**Respuesta exitosa (200) - Administrador:**
```json
{
  "id": "uuid-del-usuario",
  "email": "admin@huellitas.com",
  "rol": "administrador",
  "activo": true,
  "trabajador": null,
  "es_superusuario": true
}
```

---

## Estructura de Permisos

### Módulos Disponibles

Cada módulo tiene un conjunto de acciones posibles:

| Módulo | Acciones Posibles |
|--------|-------------------|
| `dashboard` | `ver` |
| `citas` | `ver`, `crear`, `editar`, `eliminar`, `calendario_general`, `mi_calendario` |
| `mascotas` | `ver`, `crear`, `editar`, `eliminar` |
| `responsables` | `ver`, `crear`, `editar`, `eliminar` |
| `vacunas` | `ver`, `crear`, `editar`, `eliminar`, `aplicar`, `historial` |
| `historial_clinico` | `ver`, `crear`, `editar` |
| `servicios` | `ver`, `crear`, `editar`, `eliminar` |
| `productos` | `ver`, `crear`, `editar`, `eliminar` |
| `usuarios` | `ver`, `crear`, `editar`, `eliminar` |
| `trabajadores` | `ver`, `crear`, `editar`, `eliminar` |
| `veterinarios` | `ver`, `crear`, `editar`, `eliminar`, `horarios`, `slots` |
| `reportes` | `ver`, `generar` |
| `configuracion` | `ver`, `editar` |

### Permisos Especiales

#### `calendario_general` vs `mi_calendario`
- **`calendario_general: true`**: Usuario puede ver citas de **TODOS** los veterinarios (Admin, Recepcionista)
- **`mi_calendario: true`**: Usuario solo ve **SUS PROPIAS** citas (Veterinario)

#### `aplicar` en vacunas
- Solo Veterinarios y Admin pueden aplicar vacunas
- Recepcionistas solo pueden ver el historial

---

## Implementación en Frontend

### 1. Servicio de Autenticación (React/Vue/Angular)

```javascript
// auth.service.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

class AuthService {
  async login(email, password) {
    const response = await axios.post(`${API_URL}/login/`, {
      email,
      password
    });

    if (response.data.access) {
      // Guardar token
      localStorage.setItem('token', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);

      // Configurar header de axios
      axios.defaults.headers.common['Authorization'] =
        `Bearer ${response.data.access}`;

      // Obtener permisos
      await this.loadPermissions();

      // Obtener datos del usuario
      await this.loadUserInfo();
    }

    return response.data;
  }

  async loadPermissions() {
    const response = await axios.get(`${API_URL}/auth/permisos/`);
    localStorage.setItem('permisos', JSON.stringify(response.data));
    return response.data;
  }

  async loadUserInfo() {
    const response = await axios.get(`${API_URL}/auth/me/`);
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  }

  getPermissions() {
    const permisos = localStorage.getItem('permisos');
    return permisos ? JSON.parse(permisos) : null;
  }

  getUserInfo() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  can(modulo, accion = 'ver') {
    const permisos = this.getPermissions();
    if (!permisos) return false;

    const permisoModulo = permisos.permisos[modulo];
    if (!permisoModulo) return false;

    return permisoModulo[accion] === true;
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    localStorage.removeItem('permisos');
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
  }
}

export default new AuthService();
```

### 2. Componente de Menú Lateral (React)

```jsx
// Sidebar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import AuthService from './auth.service';

const Sidebar = () => {
  const permisos = AuthService.getPermissions();
  const user = AuthService.getUserInfo();

  if (!permisos || !user) return null;

  return (
    <nav className="sidebar">
      <div className="user-info">
        <h3>{user.trabajador?.nombres || user.email}</h3>
        <p>{permisos.rol}</p>
      </div>

      <ul>
        {/* Dashboard */}
        {AuthService.can('dashboard', 'ver') && (
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>
        )}

        {/* Citas */}
        {AuthService.can('citas', 'ver') && (
          <li>
            <Link to="/citas">Citas</Link>
            <ul>
              {AuthService.can('citas', 'calendario_general') && (
                <li><Link to="/citas/calendario">Calendario General</Link></li>
              )}
              {AuthService.can('citas', 'mi_calendario') && (
                <li><Link to="/citas/mi-calendario">Mi Calendario</Link></li>
              )}
            </ul>
          </li>
        )}

        {/* Mascotas */}
        {AuthService.can('mascotas', 'ver') && (
          <li>
            <Link to="/mascotas">Mascotas</Link>
          </li>
        )}

        {/* Responsables */}
        {AuthService.can('responsables', 'ver') && (
          <li>
            <Link to="/responsables">Clientes</Link>
          </li>
        )}

        {/* Vacunación */}
        {AuthService.can('vacunas', 'ver') && (
          <li>
            <Link to="/vacunas">Vacunación</Link>
          </li>
        )}

        {/* Historial Clínico */}
        {AuthService.can('historial_clinico', 'ver') && (
          <li>
            <Link to="/historial">Historial Clínico</Link>
          </li>
        )}

        {/* Productos */}
        {AuthService.can('productos', 'ver') && (
          <li>
            <Link to="/productos">Productos</Link>
          </li>
        )}

        {/* Administración */}
        {(AuthService.can('usuarios', 'ver') ||
          AuthService.can('trabajadores', 'ver') ||
          AuthService.can('veterinarios', 'ver')) && (
          <li>
            <span>Administración</span>
            <ul>
              {AuthService.can('usuarios', 'ver') && (
                <li><Link to="/usuarios">Usuarios</Link></li>
              )}
              {AuthService.can('trabajadores', 'ver') && (
                <li><Link to="/trabajadores">Trabajadores</Link></li>
              )}
              {AuthService.can('veterinarios', 'ver') && (
                <li><Link to="/veterinarios">Veterinarios</Link></li>
              )}
            </ul>
          </li>
        )}

        {/* Reportes */}
        {AuthService.can('reportes', 'ver') && (
          <li>
            <Link to="/reportes">Reportes</Link>
          </li>
        )}

        {/* Configuración */}
        {AuthService.can('configuracion', 'ver') && (
          <li>
            <Link to="/configuracion">Configuración</Link>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Sidebar;
```

### 3. Protección de Rutas (React Router)

```jsx
// ProtectedRoute.jsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import AuthService from './auth.service';

const ProtectedRoute = ({ children, modulo, accion = 'ver' }) => {
  const token = localStorage.getItem('token');

  if (!token) {
    return <Navigate to="/login" />;
  }

  if (modulo && !AuthService.can(modulo, accion)) {
    return <Navigate to="/unauthorized" />;
  }

  return children;
};

export default ProtectedRoute;
```

```jsx
// App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route path="/dashboard" element={
          <ProtectedRoute modulo="dashboard">
            <Dashboard />
          </ProtectedRoute>
        } />

        <Route path="/citas" element={
          <ProtectedRoute modulo="citas">
            <Citas />
          </ProtectedRoute>
        } />

        <Route path="/citas/crear" element={
          <ProtectedRoute modulo="citas" accion="crear">
            <CrearCita />
          </ProtectedRoute>
        } />

        <Route path="/veterinarios" element={
          <ProtectedRoute modulo="veterinarios">
            <Veterinarios />
          </ProtectedRoute>
        } />

        {/* ... más rutas ... */}
      </Routes>
    </BrowserRouter>
  );
}
```

### 4. Componentes Condicionales (Botones, Acciones)

```jsx
// ListaCitas.jsx
import React from 'react';
import AuthService from './auth.service';

const ListaCitas = ({ citas }) => {
  return (
    <div>
      <h2>Citas</h2>

      {/* Botón crear solo si tiene permiso */}
      {AuthService.can('citas', 'crear') && (
        <button onClick={() => navigate('/citas/crear')}>
          Nueva Cita
        </button>
      )}

      <table>
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Mascota</th>
            <th>Veterinario</th>
            <th>Estado</th>
            {(AuthService.can('citas', 'editar') ||
              AuthService.can('citas', 'eliminar')) && (
              <th>Acciones</th>
            )}
          </tr>
        </thead>
        <tbody>
          {citas.map(cita => (
            <tr key={cita.id}>
              <td>{cita.fecha_hora}</td>
              <td>{cita.mascota.nombre}</td>
              <td>{cita.veterinario.trabajador.nombres}</td>
              <td>{cita.estado}</td>
              {(AuthService.can('citas', 'editar') ||
                AuthService.can('citas', 'eliminar')) && (
                <td>
                  {AuthService.can('citas', 'editar') && (
                    <button onClick={() => handleEdit(cita.id)}>
                      Editar
                    </button>
                  )}
                  {AuthService.can('citas', 'eliminar') && (
                    <button onClick={() => handleDelete(cita.id)}>
                      Cancelar
                    </button>
                  )}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

### 5. Hook Personalizado (React)

```javascript
// usePermissions.js
import { useState, useEffect } from 'react';
import AuthService from './auth.service';

export const usePermissions = () => {
  const [permisos, setPermisos] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const permisosData = AuthService.getPermissions();
        const userData = AuthService.getUserInfo();

        setPermisos(permisosData);
        setUser(userData);
      } catch (error) {
        console.error('Error cargando permisos:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const can = (modulo, accion = 'ver') => {
    return AuthService.can(modulo, accion);
  };

  const isRole = (rol) => {
    return user?.rol === rol;
  };

  return {
    permisos,
    user,
    loading,
    can,
    isRole
  };
};

// Uso:
// const { can, isRole, user } = usePermissions();
// if (can('citas', 'crear')) { ... }
// if (isRole('administrador')) { ... }
```

---

## Ejemplos de Uso

### Ejemplo 1: Vista de Calendario según Rol

```jsx
// CalendarioCitas.jsx
import React, { useEffect, useState } from 'react';
import { usePermissions } from './usePermissions';
import axios from 'axios';

const CalendarioCitas = () => {
  const { can, isRole } = usePermissions();
  const [citas, setCitas] = useState([]);

  useEffect(() => {
    const fetchCitas = async () => {
      let endpoint;

      // Determinar qué endpoint usar según permisos
      if (can('citas', 'calendario_general')) {
        // Admin o Recepcionista: ve TODAS las citas
        endpoint = '/api/citas/calendario_recepcion/';
      } else if (can('citas', 'mi_calendario')) {
        // Veterinario: solo ve SUS citas
        endpoint = '/api/citas/mi_calendario/';
      } else {
        // No tiene permiso para ver calendario
        return;
      }

      const response = await axios.get(endpoint);
      setCitas(response.data);
    };

    fetchCitas();
  }, [can]);

  return (
    <div>
      <h2>
        {can('citas', 'calendario_general')
          ? 'Calendario General'
          : 'Mi Calendario'}
      </h2>

      {/* Renderizar calendario con citas */}
      <Calendar events={citas} />
    </div>
  );
};
```

### Ejemplo 2: Aplicar Vacuna (Solo Veterinarios)

```jsx
// AplicarVacuna.jsx
import React from 'react';
import { usePermissions } from './usePermissions';
import { Navigate } from 'react-router-dom';

const AplicarVacuna = () => {
  const { can, user } = usePermissions();

  // Redirigir si no tiene permiso
  if (!can('vacunas', 'aplicar')) {
    return <Navigate to="/unauthorized" />;
  }

  const handleSubmit = async (formData) => {
    try {
      const response = await axios.post(
        `/api/vacunas/${formData.vacuna_id}/aplicar/`,
        {
          mascota: formData.mascota_id,
          veterinario: user.veterinario.id, // ID del veterinario autenticado
          fecha_aplicacion: formData.fecha,
          protocolo_completo: formData.protocolo_completo,
          dosis_numero: formData.dosis_numero,
          dosis_aplicadas: formData.dosis_aplicadas
        }
      );

      alert('Vacuna aplicada correctamente');
    } catch (error) {
      alert('Error: ' + error.response.data.error);
    }
  };

  return (
    <div>
      <h2>Aplicar Vacuna</h2>
      {/* Formulario de aplicación */}
    </div>
  );
};
```

### Ejemplo 3: Gestión de Usuarios (Solo Admin)

```jsx
// Usuarios.jsx
import React from 'react';
import { usePermissions } from './usePermissions';

const Usuarios = () => {
  const { can, isRole } = usePermissions();

  // Solo admin puede ver esta página
  if (!isRole('administrador')) {
    return <div>No tienes acceso a esta sección</div>;
  }

  return (
    <div>
      <h2>Gestión de Usuarios</h2>

      {can('usuarios', 'crear') && (
        <button onClick={() => handleCreate()}>
          Crear Usuario
        </button>
      )}

      {/* Lista de usuarios con acciones de editar/eliminar */}
    </div>
  );
};
```

---

## Casos Especiales

### 1. Usuario Admin Precargado

En el sistema existe un usuario administrador creado automáticamente:

```
Email: admin@huellitas.com
Password: admin123
Rol: administrador
```

**IMPORTANTE**: Cambiar la contraseña en producción.

### 2. Veterinario Externo

Existe un veterinario especial con ID fijo para vacunas externas:

```
ID: e25ff4ab-9ffe-4ec7-9e42-0f7d0fac9f1a
Email: veterinario.externo@sistema.com
Uso: Registro de vacunas aplicadas en otras clínicas
```

Para obtenerlo desde el frontend:

```javascript
const response = await axios.get('/api/veterinarios/externo/');
const veterinarioExterno = response.data;
```

### 3. Responsables (Dueños de Mascotas)

- Los Responsables **NO tienen acceso al sistema**
- Son creados por Recepcionistas o Admin
- Se usan solo para asociar mascotas con sus dueños
- Cada Responsable tiene un Usuario asociado con rol 'Responsable', pero este usuario no puede hacer login

### 4. Refresh Token

El token JWT expira en 60 minutos. Implementar refresh automático:

```javascript
// axios.interceptor.js
axios.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refresh = localStorage.getItem('refresh');
        const response = await axios.post('/api/refresh/', { refresh });

        const newToken = response.data.access;
        localStorage.setItem('token', newToken);
        axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;

        return axios(originalRequest);
      } catch (err) {
        // Refresh token inválido, hacer logout
        AuthService.logout();
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);
```

### 5. Estado de Usuario Inactivo

Si un usuario es desactivado (`activo: false`), el backend rechazará sus tokens. Implementar manejo de errores:

```javascript
if (error.response.status === 403 && error.response.data.error === 'Usuario inactivo') {
  alert('Tu cuenta ha sido desactivada. Contacta al administrador.');
  AuthService.logout();
  window.location.href = '/login';
}
```

---

## Recomendaciones

### Seguridad
1. **Nunca confiar solo en el frontend**: Los permisos del frontend son para UX, el backend SIEMPRE valida
2. **Validar tokens**: Implementar refresh automático y manejo de expiración
3. **HTTPS en producción**: Nunca enviar tokens por HTTP sin cifrar

### UX
1. **Loading states**: Mostrar spinners mientras se cargan permisos
2. **Mensajes claros**: "No tienes permisos para esta acción" en lugar de ocultar sin explicar
3. **Deshabilitar vs Ocultar**: Deshabilitar botones que requieren permisos (mejor que ocultarlos)

### Performance
1. **Cachear permisos**: No hacer petición GET /api/auth/permisos/ en cada navegación
2. **Lazy loading**: Cargar rutas según permisos del usuario
3. **Optimistic UI**: Mostrar feedback inmediato en acciones

### Testing
1. Probar cada rol con diferentes combinaciones de permisos
2. Verificar que rutas protegidas redirijan correctamente
3. Simular tokens expirados y usuarios inactivos

---

## Endpoints Completos del Sistema

Para implementación completa, consultar:
- [README.md](README.md) - Lista completa de endpoints
- [VACUNACION_API_DOCS.md](VACUNACION_API_DOCS.md) - API de vacunación
- [SISTEMA_SLOTS_DOCUMENTACION.md](SISTEMA_SLOTS_DOCUMENTACION.md) - Sistema de citas

---

## Soporte

Para dudas o problemas con la implementación:
1. Revisar logs del backend: El sistema registra errores de permisos
2. Verificar token JWT en [jwt.io](https://jwt.io)
3. Consultar documentación técnica en archivos MD del repositorio
