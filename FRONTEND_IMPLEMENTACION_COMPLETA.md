# Guía Completa para Frontend - Sistema de Roles y Permisos

> **Para el desarrollador frontend**: Este documento contiene TODO lo necesario para implementar el sistema de roles, permisos y gestión dinámica de permisos.

---

## 📋 Índice

1. [Credenciales de Prueba](#credenciales-de-prueba)
2. [Endpoints de Autenticación](#endpoints-de-autenticación)
3. [Sistema de Permisos - Uso Básico](#sistema-de-permisos---uso-básico)
4. [Módulo de Gestión de Permisos (Admin)](#módulo-de-gestión-de-permisos-admin)
5. [Interfaces TypeScript](#interfaces-typescript)
6. [Ejemplos de Código](#ejemplos-de-código)

---

## 🔐 Credenciales de Prueba

Usa estas credenciales para probar el sistema:

| Rol | Email | Contraseña | Nombre |
|-----|-------|------------|--------|
| **Administrador** | admin@huellitas.com | admin12345 | Admin |
| **Veterinario** | vet@huellitas.com | vet12345 | Carlos Alberto Ramirez Perez |
| **Recepcionista** | recepcion@huellitas.com | recep12345 | Maria Elena Gonzalez Torres |

---

## 🌐 Endpoints de Autenticación

### Base URL
```
http://localhost:8000/api
```

### 1. Login

**POST** `/api/login/`

```typescript
// Request
{
  "email": "admin@huellitas.com",
  "password": "admin12345"
}

// Response (200)
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Obtener Permisos del Usuario

**GET** `/api/auth/permisos/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "rol": "administrador",
  "permisos": {
    "dashboard": { "ver": true },
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
    }
    // ... más módulos
  }
}
```

### 3. Obtener Info del Usuario

**GET** `/api/auth/me/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (Veterinario):**
```json
{
  "id": "uuid-del-usuario",
  "email": "vet@huellitas.com",
  "rol": "veterinario",
  "trabajador": {
    "id": "uuid",
    "nombres": "Carlos Alberto",
    "apellidos": "Ramirez Perez",
    "email": "vet@huellitas.com",
    "telefono": "987654321",
    "tipodocumento": "uuid",
    "documento": "45678912"
  },
  "veterinario": {
    "id": "uuid",
    "especialidad": "Medicina General"
  }
}
```

### 4. Refresh Token

**POST** `/api/refresh/`

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 🛡️ Sistema de Permisos - Uso Básico

### Flujo de Login

```typescript
// 1. Login
const loginResponse = await axios.post('/api/login/', {
  email: 'admin@huellitas.com',
  password: 'admin12345'
});

// 2. Guardar tokens
localStorage.setItem('access', loginResponse.data.access);
localStorage.setItem('refresh', loginResponse.data.refresh);

// 3. Configurar header
axios.defaults.headers.common['Authorization'] =
  `Bearer ${loginResponse.data.access}`;

// 4. Obtener permisos
const permisosResponse = await axios.get('/api/auth/permisos/');
localStorage.setItem('permisos', JSON.stringify(permisosResponse.data));

// 5. Obtener info del usuario
const userResponse = await axios.get('/api/auth/me/');
localStorage.setItem('user', JSON.stringify(userResponse.data));
```

### Verificar Permisos en Componentes

```typescript
// Verificar si puede ver un módulo
const permisos = JSON.parse(localStorage.getItem('permisos'));
const puedeVerDashboard = permisos?.permisos?.dashboard?.ver;

// Verificar si puede crear citas
const puedeCrearCitas = permisos?.permisos?.citas?.crear;
```

### Resumen de Permisos por Rol

| Módulo | Admin | Veterinario | Recepcionista |
|--------|-------|-------------|---------------|
| Dashboard | ✅ | ❌ | ❌ |
| Crear Citas | ✅ | ❌ | ✅ |
| Calendario General | ✅ | ❌ | ✅ |
| Mi Calendario | ✅ | ✅ | ❌ |
| Aplicar Vacunas | ✅ | ✅ | ❌ |
| Gestionar Usuarios | ✅ | ❌ | ❌ |

---

## ⚙️ Módulo de Gestión de Permisos (Admin)

> **IMPORTANTE**: Este módulo es **SOLO PARA ADMINISTRADORES**. Permite modificar permisos dinámicamente sin tocar código.

### Endpoints Disponibles

#### 1. Listar Todos los Permisos

**GET** `/api/permisos-rol/`

```json
[
  {
    "id": "uuid",
    "rol": "veterinario",
    "rol_display": "Veterinario",
    "modulo": "citas",
    "permisos": {
      "ver": true,
      "crear": false,
      "editar": true
    },
    "descripcion_modulo": "Gestión de citas",
    "fecha_creacion": "2025-10-06T10:00:00Z",
    "fecha_modificacion": "2025-10-06T10:00:00Z"
  }
]
```

#### 2. Obtener Permisos de un Rol

**GET** `/api/permisos-rol/por-rol/?rol=veterinario`

```json
{
  "rol": "veterinario",
  "permisos": [
    {
      "id": "uuid",
      "modulo": "citas",
      "permisos": {"ver": true, "crear": false}
    },
    {
      "id": "uuid",
      "modulo": "vacunas",
      "permisos": {"ver": true, "aplicar": true}
    }
  ]
}
```

#### 3. Obtener Módulos Disponibles

**GET** `/api/permisos-rol/modulos-disponibles/`

```json
{
  "dashboard": {
    "nombre": "Dashboard",
    "descripcion": "Panel principal",
    "acciones": ["ver"]
  },
  "citas": {
    "nombre": "Citas",
    "descripcion": "Gestión de citas",
    "acciones": ["ver", "crear", "editar", "eliminar", "calendario_general", "mi_calendario"]
  }
}
```

#### 4. Actualizar Permiso Individual

**PATCH** `/api/permisos-rol/{id}/`

```json
{
  "permisos": {
    "ver": true,
    "crear": true,
    "editar": false
  }
}
```

#### 5. Actualización Masiva

**POST** `/api/permisos-rol/actualizar-masivo/`

```json
{
  "rol": "veterinario",
  "permisos": [
    {
      "modulo": "citas",
      "permisos": {
        "ver": true,
        "crear": true,
        "editar": true
      }
    },
    {
      "modulo": "mascotas",
      "permisos": {
        "ver": true,
        "crear": false
      }
    }
  ]
}
```

**Response:**
```json
{
  "mensaje": "Permisos actualizados correctamente",
  "rol": "veterinario",
  "actualizados": ["citas", "mascotas"],
  "creados": [],
  "total": 2
}
```

#### 6. Inicializar Permisos por Defecto

**POST** `/api/permisos-rol/inicializar-defaults/`

> Crea los permisos iniciales para todos los roles. Útil si se borra la BD o es primera vez.

```json
{
  "mensaje": "Permisos inicializados correctamente",
  "creados": 52,
  "actualizados": 0,
  "total": 52
}
```

---

## 📝 Interfaces TypeScript

### Interfaces de Autenticación

```typescript
interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  access: string;
  refresh: string;
}

interface RefreshRequest {
  refresh: string;
}

interface RefreshResponse {
  access: string;
}
```

### Interfaces de Permisos

```typescript
interface PermisosUsuario {
  rol: 'administrador' | 'veterinario' | 'recepcionista' | 'inventario';
  permisos: {
    dashboard?: { ver: boolean };
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

```typescript
interface Trabajador {
  id: string;
  nombres: string;
  apellidos: string;
  email: string;
  telefono: string;
  tipodocumento: string;
  documento: string;
}

interface Veterinario {
  id: string;
  especialidad: string;
}

interface UsuarioCompleto {
  id: string;
  email: string;
  rol: 'administrador' | 'veterinario' | 'recepcionista' | 'inventario';
  trabajador: Trabajador | null;
  veterinario?: Veterinario;
}
```

### Interfaces de Gestión de Permisos

```typescript
interface PermisoRol {
  id: string;
  rol: string;
  rol_display: string;
  modulo: string;
  permisos: Record<string, boolean>;
  descripcion_modulo: string;
  fecha_creacion: string;
  fecha_modificacion: string;
}

interface ModuloDisponible {
  nombre: string;
  descripcion: string;
  acciones: string[];
}

interface ModulosDisponibles {
  [key: string]: ModuloDisponible;
}

interface ActualizarMasivoRequest {
  rol: string;
  permisos: Array<{
    modulo: string;
    permisos: Record<string, boolean>;
    descripcion_modulo?: string;
  }>;
}

interface ActualizarMasivoResponse {
  mensaje: string;
  rol: string;
  actualizados: string[];
  creados: string[];
  total: number;
}
```

---

## 💻 Ejemplos de Código

### 1. Servicio de Autenticación

```typescript
// auth.service.ts
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

class AuthService {
  async login(email: string, password: string) {
    const response = await axios.post(`${API_URL}/login/`, {
      email,
      password
    });

    if (response.data.access) {
      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);

      axios.defaults.headers.common['Authorization'] =
        `Bearer ${response.data.access}`;

      await this.loadPermissions();
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

  getPermissions(): PermisosUsuario | null {
    const permisos = localStorage.getItem('permisos');
    return permisos ? JSON.parse(permisos) : null;
  }

  getUserInfo(): UsuarioCompleto | null {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  can(modulo: string, accion: string = 'ver'): boolean {
    const permisos = this.getPermissions();
    if (!permisos) return false;

    const permisoModulo = permisos.permisos[modulo];
    if (!permisoModulo) return false;

    return permisoModulo[accion] === true;
  }

  isRole(rol: string): boolean {
    const user = this.getUserInfo();
    return user?.rol === rol;
  }

  logout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('permisos');
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
  }
}

export default new AuthService();
```

### 2. Componente de Menú Lateral (React)

```tsx
// Sidebar.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import AuthService from './auth.service';

const Sidebar: React.FC = () => {
  const permisos = AuthService.getPermissions();
  const user = AuthService.getUserInfo();

  if (!permisos || !user) return null;

  return (
    <nav className="sidebar">
      <div className="user-info">
        <h3>{user.trabajador?.nombres || user.email}</h3>
        <p className="role-badge">{permisos.rol}</p>
      </div>

      <ul className="menu">
        {/* Dashboard - Solo Admin */}
        {AuthService.can('dashboard', 'ver') && (
          <li>
            <Link to="/dashboard">
              <i className="icon-dashboard"></i>
              Dashboard
            </Link>
          </li>
        )}

        {/* Citas */}
        {AuthService.can('citas', 'ver') && (
          <li>
            <Link to="/citas">
              <i className="icon-calendar"></i>
              Citas
            </Link>
            <ul className="submenu">
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
            <Link to="/mascotas">
              <i className="icon-pet"></i>
              Mascotas
            </Link>
          </li>
        )}

        {/* Clientes */}
        {AuthService.can('responsables', 'ver') && (
          <li>
            <Link to="/responsables">
              <i className="icon-users"></i>
              Clientes
            </Link>
          </li>
        )}

        {/* Vacunación */}
        {AuthService.can('vacunas', 'ver') && (
          <li>
            <Link to="/vacunas">
              <i className="icon-syringe"></i>
              Vacunación
            </Link>
          </li>
        )}

        {/* Historial Clínico */}
        {AuthService.can('historial_clinico', 'ver') && (
          <li>
            <Link to="/historial">
              <i className="icon-file-medical"></i>
              Historial Clínico
            </Link>
          </li>
        )}

        {/* Administración - Solo Admin */}
        {(AuthService.can('usuarios', 'ver') ||
          AuthService.can('trabajadores', 'ver') ||
          AuthService.can('veterinarios', 'ver')) && (
          <li>
            <span className="menu-title">
              <i className="icon-settings"></i>
              Administración
            </span>
            <ul className="submenu">
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

        {/* Gestión de Permisos - Solo Admin */}
        {AuthService.isRole('administrador') && (
          <li>
            <Link to="/permisos">
              <i className="icon-shield"></i>
              Gestión de Permisos
            </Link>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Sidebar;
```

### 3. Componente de Gestión de Permisos (React)

```tsx
// GestionPermisos.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './GestionPermisos.css';

interface Permiso {
  id: string;
  modulo: string;
  permisos: Record<string, boolean>;
  descripcion_modulo: string;
}

interface Modulo {
  nombre: string;
  descripcion: string;
  acciones: string[];
}

const GestionPermisos: React.FC = () => {
  const [roles] = useState(['administrador', 'veterinario', 'recepcionista']);
  const [rolSeleccionado, setRolSeleccionado] = useState('veterinario');
  const [modulos, setModulos] = useState<Record<string, Modulo>>({});
  const [permisos, setPermisos] = useState<Permiso[]>([]);
  const [loading, setLoading] = useState(false);

  // Cargar módulos disponibles
  useEffect(() => {
    const cargarModulos = async () => {
      const response = await axios.get('/api/permisos-rol/modulos-disponibles/');
      setModulos(response.data);
    };
    cargarModulos();
  }, []);

  // Cargar permisos del rol seleccionado
  useEffect(() => {
    const cargarPermisos = async () => {
      const response = await axios.get(
        `/api/permisos-rol/por-rol/?rol=${rolSeleccionado}`
      );
      setPermisos(response.data.permisos);
    };
    cargarPermisos();
  }, [rolSeleccionado]);

  // Manejar cambio de checkbox
  const handlePermisoChange = (
    permisoId: string,
    accion: string,
    valor: boolean
  ) => {
    setPermisos(permisos.map(p =>
      p.id === permisoId
        ? {...p, permisos: {...p.permisos, [accion]: valor}}
        : p
    ));
  };

  // Guardar cambios
  const guardarCambios = async () => {
    setLoading(true);
    try {
      await axios.post('/api/permisos-rol/actualizar-masivo/', {
        rol: rolSeleccionado,
        permisos: permisos.map(p => ({
          modulo: p.modulo,
          permisos: p.permisos,
          descripcion_modulo: p.descripcion_modulo
        }))
      });
      alert('✅ Permisos actualizados correctamente');
    } catch (error) {
      alert('❌ Error al actualizar permisos');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="gestion-permisos">
      <h1>Gestión de Permisos por Rol</h1>

      {/* Selector de rol */}
      <div className="selector-rol">
        <label>Seleccionar Rol:</label>
        <select
          value={rolSeleccionado}
          onChange={(e) => setRolSeleccionado(e.target.value)}
        >
          {roles.map(rol => (
            <option key={rol} value={rol}>
              {rol.charAt(0).toUpperCase() + rol.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Tabla de permisos */}
      <table className="tabla-permisos">
        <thead>
          <tr>
            <th>Módulo</th>
            <th>Descripción</th>
            <th>Ver</th>
            <th>Crear</th>
            <th>Editar</th>
            <th>Eliminar</th>
            <th>Otros</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(modulos).map(([moduloKey, moduloInfo]) => {
            const permiso = permisos.find(p => p.modulo === moduloKey);
            if (!permiso) return null;

            return (
              <tr key={moduloKey}>
                <td><strong>{moduloInfo.nombre}</strong></td>
                <td className="text-muted">{moduloInfo.descripcion}</td>

                {/* Ver */}
                <td>
                  {moduloInfo.acciones.includes('ver') && (
                    <input
                      type="checkbox"
                      checked={permiso.permisos.ver || false}
                      onChange={(e) => handlePermisoChange(
                        permiso.id, 'ver', e.target.checked
                      )}
                    />
                  )}
                </td>

                {/* Crear */}
                <td>
                  {moduloInfo.acciones.includes('crear') && (
                    <input
                      type="checkbox"
                      checked={permiso.permisos.crear || false}
                      onChange={(e) => handlePermisoChange(
                        permiso.id, 'crear', e.target.checked
                      )}
                    />
                  )}
                </td>

                {/* Editar */}
                <td>
                  {moduloInfo.acciones.includes('editar') && (
                    <input
                      type="checkbox"
                      checked={permiso.permisos.editar || false}
                      onChange={(e) => handlePermisoChange(
                        permiso.id, 'editar', e.target.checked
                      )}
                    />
                  )}
                </td>

                {/* Eliminar */}
                <td>
                  {moduloInfo.acciones.includes('eliminar') && (
                    <input
                      type="checkbox"
                      checked={permiso.permisos.eliminar || false}
                      onChange={(e) => handlePermisoChange(
                        permiso.id, 'eliminar', e.target.checked
                      )}
                    />
                  )}
                </td>

                {/* Otros permisos */}
                <td>
                  {Object.entries(permiso.permisos)
                    .filter(([key]) =>
                      !['ver', 'crear', 'editar', 'eliminar'].includes(key)
                    )
                    .map(([accion, valor]) => (
                      <label key={accion} className="checkbox-inline">
                        <input
                          type="checkbox"
                          checked={valor}
                          onChange={(e) => handlePermisoChange(
                            permiso.id, accion, e.target.checked
                          )}
                        />
                        <span>{accion.replace('_', ' ')}</span>
                      </label>
                    ))
                  }
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Botones */}
      <div className="botones">
        <button
          className="btn btn-primary"
          onClick={guardarCambios}
          disabled={loading}
        >
          {loading ? 'Guardando...' : 'Guardar Cambios'}
        </button>
        <button
          className="btn btn-secondary"
          onClick={() => window.location.reload()}
        >
          Cancelar
        </button>
      </div>
    </div>
  );
};

export default GestionPermisos;
```

### 4. Estilos CSS para Gestión de Permisos

```css
/* GestionPermisos.css */
.gestion-permisos {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.gestion-permisos h1 {
  margin-bottom: 30px;
  color: #333;
}

.selector-rol {
  margin-bottom: 30px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 8px;
}

.selector-rol label {
  font-weight: 600;
  margin-right: 10px;
}

.selector-rol select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  min-width: 200px;
}

.tabla-permisos {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

.tabla-permisos thead {
  background: #4a5568;
  color: white;
}

.tabla-permisos th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
}

.tabla-permisos td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  text-align: center;
}

.tabla-permisos td:first-child,
.tabla-permisos td:nth-child(2) {
  text-align: left;
}

.tabla-permisos tbody tr:hover {
  background: #f9fafb;
}

.tabla-permisos input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-inline {
  display: inline-block;
  margin-right: 15px;
  cursor: pointer;
}

.checkbox-inline input {
  margin-right: 5px;
}

.text-muted {
  color: #6b7280;
  font-size: 14px;
}

.botones {
  margin-top: 30px;
  display: flex;
  gap: 15px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
}
```

---

## ✅ Checklist de Implementación

### Fase 1: Autenticación Básica
- [ ] Implementar servicio de autenticación
- [ ] Crear pantalla de login
- [ ] Guardar tokens en localStorage
- [ ] Configurar interceptor de Axios para refresh token
- [ ] Probar login con las 3 credenciales

### Fase 2: Sistema de Permisos
- [ ] Cargar permisos después del login
- [ ] Crear hook/servicio para verificar permisos
- [ ] Implementar guards de rutas
- [ ] Mostrar/ocultar elementos del menú según permisos
- [ ] Probar con cada rol

### Fase 3: Gestión de Permisos (Solo Admin)
- [ ] Crear componente de gestión de permisos
- [ ] Cargar módulos disponibles
- [ ] Cargar permisos de cada rol
- [ ] Implementar tabla con checkboxes
- [ ] Implementar actualización masiva
- [ ] Probar modificación de permisos y verificar que se aplican

---

## 📚 Documentos de Referencia

Para más detalles técnicos, consulta:

1. **GUIA_FRONTEND_ROLES_PERMISOS.md** - Guía completa del sistema de permisos
2. **GESTION_PERMISOS_DINAMICOS.md** - Documentación técnica del módulo de gestión
3. **ACLARACIONES_FRONTEND_LOGIN.md** - Detalles sobre campos que NO existen

---

## 🚀 Resumen

1. **Login**: Usa `/api/login/` con email y password
2. **Permisos**: Obtén con `/api/auth/permisos/` después del login
3. **Info Usuario**: Obtén con `/api/auth/me/`
4. **Gestión Permisos**: Solo admin, usa endpoints `/api/permisos-rol/`
5. **Verificación**: Usa `can(modulo, accion)` para verificar permisos

**Credenciales de Prueba:**
- Admin: admin@huellitas.com / admin12345
- Veterinario: vet@huellitas.com / vet12345
- Recepcionista: recepcion@huellitas.com / recep12345
