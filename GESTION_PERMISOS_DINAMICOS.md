# Gestión Dinámica de Permisos - Módulo de Administración

## 📋 Índice
1. [Descripción General](#descripción-general)
2. [¿Qué es este módulo?](#qué-es-este-módulo)
3. [Endpoints Disponibles](#endpoints-disponibles)
4. [Flujo de Trabajo](#flujo-de-trabajo)
5. [Ejemplos de Uso](#ejemplos-de-uso)
6. [Implementación Frontend](#implementación-frontend)
7. [Modelo de Datos](#modelo-de-datos)

---

## Descripción General

El **Sistema de Gestión Dinámica de Permisos** permite al administrador modificar desde el frontend qué puede ver y hacer cada rol del sistema, sin necesidad de tocar código backend.

### Características

✅ **Gestión visual de permisos** - Interfaz para activar/desactivar permisos por rol
✅ **Cambios en tiempo real** - Los permisos se aplican inmediatamente
✅ **Actualización masiva** - Modificar múltiples permisos a la vez
✅ **Persistencia en BD** - Los permisos se guardan en PostgreSQL
✅ **Fallback seguro** - Si falla la BD, usa permisos hardcodeados por defecto
✅ **Auditoría** - Registro de fecha de creación y modificación

---

## ¿Qué es este módulo?

Antes del módulo, los permisos estaban **hardcodeados** en el archivo `api/permissions.py`. Si querías cambiar qué puede ver un veterinario, tenías que:
1. Modificar el código
2. Hacer commit
3. Desplegar
4. Reiniciar el servidor

**Ahora con este módulo**, el admin puede desde el frontend:
1. Ir al módulo de "Gestión de Permisos"
2. Seleccionar un rol (ej: `veterinario`)
3. Activar/desactivar checkboxes para cada módulo
4. Guardar cambios
5. ✅ Los cambios se aplican inmediatamente

---

## Endpoints Disponibles

### Base URL
```
http://localhost:8000/api/permisos-rol/
```

### 1. Listar todos los permisos

**GET** `/api/permisos-rol/`

Lista todos los permisos configurados en el sistema.

**Respuesta:**
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
      "editar": true,
      "eliminar": false,
      "calendario_general": false,
      "mi_calendario": true
    },
    "descripcion_modulo": "Gestión de citas veterinarias",
    "fecha_creacion": "2025-10-06T10:00:00Z",
    "fecha_modificacion": "2025-10-06T10:00:00Z"
  }
]
```

### 2. Obtener permisos de un rol específico

**GET** `/api/permisos-rol/por-rol/?rol=veterinario`

Obtiene todos los permisos de un rol.

**Query Params:**
- `rol` (requerido): Rol a consultar (`administrador`, `veterinario`, `recepcionista`)

**Respuesta:**
```json
{
  "rol": "veterinario",
  "permisos": [
    {
      "id": "uuid",
      "rol": "veterinario",
      "modulo": "citas",
      "permisos": {"ver": true, "crear": false},
      "descripcion_modulo": "Gestión de citas"
    },
    {
      "id": "uuid",
      "rol": "veterinario",
      "modulo": "vacunas",
      "permisos": {"ver": true, "aplicar": true},
      "descripcion_modulo": "Sistema de vacunación"
    }
  ]
}
```

### 3. Obtener módulos disponibles

**GET** `/api/permisos-rol/modulos-disponibles/`

Lista todos los módulos del sistema con sus acciones posibles.

**Respuesta:**
```json
{
  "dashboard": {
    "nombre": "Dashboard",
    "descripcion": "Panel principal con estadísticas",
    "acciones": ["ver"]
  },
  "citas": {
    "nombre": "Citas",
    "descripcion": "Gestión de citas veterinarias",
    "acciones": ["ver", "crear", "editar", "eliminar", "calendario_general", "mi_calendario"]
  },
  "mascotas": {
    "nombre": "Mascotas",
    "descripcion": "Gestión de mascotas",
    "acciones": ["ver", "crear", "editar", "eliminar"]
  }
}
```

### 4. Actualizar un permiso individual

**PATCH** `/api/permisos-rol/{id}/`

Actualiza un permiso específico.

**Body:**
```json
{
  "permisos": {
    "ver": true,
    "crear": true,
    "editar": false
  }
}
```

### 5. Actualización masiva de permisos

**POST** `/api/permisos-rol/actualizar-masivo/`

Actualiza múltiples permisos de un rol en una sola petición.

**Body:**
```json
{
  "rol": "veterinario",
  "permisos": [
    {
      "modulo": "citas",
      "permisos": {
        "ver": true,
        "crear": false,
        "editar": true
      },
      "descripcion_modulo": "Gestión de citas"
    },
    {
      "modulo": "mascotas",
      "permisos": {
        "ver": true,
        "crear": false,
        "editar": false
      }
    }
  ]
}
```

**Respuesta:**
```json
{
  "mensaje": "Permisos actualizados correctamente",
  "rol": "veterinario",
  "actualizados": ["citas", "mascotas"],
  "creados": [],
  "total": 2
}
```

### 6. Inicializar permisos por defecto

**POST** `/api/permisos-rol/inicializar-defaults/`

Crea los permisos por defecto para todos los roles. Útil para:
- Primera vez que se usa el sistema
- Resetear permisos a valores predeterminados

**Respuesta:**
```json
{
  "mensaje": "Permisos inicializados correctamente",
  "creados": 52,
  "actualizados": 0,
  "total": 52
}
```

---

## Flujo de Trabajo

### 1. Inicialización del Sistema (Primera vez)

```bash
# Al instalar el sistema por primera vez
POST /api/permisos-rol/inicializar-defaults/
```

Esto crea los permisos por defecto para todos los roles en la base de datos.

### 2. Cargar Módulos Disponibles (Frontend)

```javascript
// Al abrir la pantalla de gestión de permisos
const modulos = await axios.get('/api/permisos-rol/modulos-disponibles/');
// Renderizar lista de módulos con checkboxes
```

### 3. Seleccionar Rol a Editar

```javascript
// Usuario selecciona "Veterinario" del dropdown
const permisos = await axios.get('/api/permisos-rol/por-rol/?rol=veterinario');
// Mostrar permisos actuales con checkboxes marcados/desmarcados
```

### 4. Modificar Permisos

```javascript
// Usuario marca/desmarca checkboxes en la UI
// Al hacer clic en "Guardar"
const response = await axios.post('/api/permisos-rol/actualizar-masivo/', {
  rol: 'veterinario',
  permisos: [
    {
      modulo: 'citas',
      permisos: {ver: true, crear: true, editar: false}
    }
  ]
});
```

### 5. Permisos Aplicados Automáticamente

Los cambios se aplican de inmediato. El próximo request de ese rol usará los nuevos permisos.

---

## Ejemplos de Uso

### Ejemplo 1: Dar acceso a Dashboard solo a Admin

```javascript
// Paso 1: Deshabilitar dashboard para veterinarios
await axios.patch('/api/permisos-rol/<id-permiso-veterinario-dashboard>/', {
  permisos: {
    ver: false
  }
});

// Paso 2: Deshabilitar dashboard para recepcionistas
await axios.patch('/api/permisos-rol/<id-permiso-recepcionista-dashboard>/', {
  permisos: {
    ver: false
  }
});

// Paso 3: Asegurar que admin tenga acceso
await axios.patch('/api/permisos-rol/<id-permiso-admin-dashboard>/', {
  permisos: {
    ver: true
  }
});
```

### Ejemplo 2: Permitir a Recepcionistas crear citas

```javascript
await axios.post('/api/permisos-rol/actualizar-masivo/', {
  rol: 'recepcionista',
  permisos: [
    {
      modulo: 'citas',
      permisos: {
        ver: true,
        crear: true,        // ✅ Activar
        editar: true,
        eliminar: true,
        calendario_general: true,
        mi_calendario: false
      }
    }
  ]
});
```

### Ejemplo 3: Restringir acceso a Productos para Veterinarios

```javascript
await axios.patch('/api/permisos-rol/<id-permiso-veterinario-productos>/', {
  permisos: {
    ver: false,      // ❌ Ocultar módulo completo
    crear: false,
    editar: false,
    eliminar: false
  }
});
```

---

## Implementación Frontend

### Interfaz Recomendada

```
┌─────────────────────────────────────────────────┐
│ Gestión de Permisos por Rol                     │
├─────────────────────────────────────────────────┤
│                                                  │
│ Seleccionar Rol:  [Veterinario ▼]               │
│                                                  │
├─────────────────────────────────────────────────┤
│ Módulo              │ Ver │ Crear │ Editar │... │
├─────────────────────┼─────┼───────┼────────┼────┤
│ ☐ Dashboard         │ ☐   │  -    │   -    │    │
│ ☑ Citas             │ ☑   │  ☐    │   ☑    │... │
│ ☑ Mascotas          │ ☑   │  ☐    │   ☐    │... │
│ ☑ Vacunación        │ ☑   │  ☐    │   ☐    │... │
│ ☐ Usuarios          │ ☐   │  ☐    │   ☐    │... │
│ ☐ Configuración     │ ☐   │  ☐    │   ☐    │... │
├─────────────────────────────────────────────────┤
│                [Guardar Cambios]  [Cancelar]    │
└─────────────────────────────────────────────────┘
```

### Componente React Ejemplo

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GestionPermisos = () => {
  const [roles] = useState(['administrador', 'veterinario', 'recepcionista']);
  const [rolSeleccionado, setRolSeleccionado] = useState('veterinario');
  const [modulos, setModulos] = useState({});
  const [permisos, setPermisos] = useState([]);
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
      const response = await axios.get(`/api/permisos-rol/por-rol/?rol=${rolSeleccionado}`);
      setPermisos(response.data.permisos);
    };
    cargarPermisos();
  }, [rolSeleccionado]);

  // Manejar cambio de checkbox
  const handlePermisoChange = (permisoId, modulo, accion, valor) => {
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
      alert('Permisos actualizados correctamente');
    } catch (error) {
      alert('Error al actualizar permisos');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="gestion-permisos">
      <h2>Gestión de Permisos por Rol</h2>

      {/* Selector de rol */}
      <div className="selector-rol">
        <label>Seleccionar Rol:</label>
        <select value={rolSeleccionado} onChange={(e) => setRolSeleccionado(e.target.value)}>
          {roles.map(rol => (
            <option key={rol} value={rol}>{rol}</option>
          ))}
        </select>
      </div>

      {/* Tabla de permisos */}
      <table className="tabla-permisos">
        <thead>
          <tr>
            <th>Módulo</th>
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

                {/* Checkbox Ver */}
                <td>
                  {moduloInfo.acciones.includes('ver') && (
                    <input
                      type="checkbox"
                      checked={permiso.permisos.ver || false}
                      onChange={(e) => handlePermisoChange(
                        permiso.id, moduloKey, 'ver', e.target.checked
                      )}
                    />
                  )}
                </td>

                {/* Checkbox Crear */}
                <td>
                  {moduloInfo.acciones.includes('crear') && (
                    <input
                      type="checkbox"
                      checked={permiso.permisos.crear || false}
                      onChange={(e) => handlePermisoChange(
                        permiso.id, moduloKey, 'crear', e.target.checked
                      )}
                    />
                  )}
                </td>

                {/* Checkbox Editar */}
                <td>
                  {moduloInfo.acciones.includes('editar') && (
                    <input
                      type="checkbox"
                      checked={permiso.permisos.editar || false}
                      onChange={(e) => handlePermisoChange(
                        permiso.id, moduloKey, 'editar', e.target.checked
                      )}
                    />
                  )}
                </td>

                {/* Checkbox Eliminar */}
                <td>
                  {moduloInfo.acciones.includes('eliminar') && (
                    <input
                      type="checkbox"
                      checked={permiso.permisos.eliminar || false}
                      onChange={(e) => handlePermisoChange(
                        permiso.id, moduloKey, 'eliminar', e.target.checked
                      )}
                    />
                  )}
                </td>

                {/* Otras acciones especiales */}
                <td>
                  {Object.entries(permiso.permisos)
                    .filter(([key]) => !['ver', 'crear', 'editar', 'eliminar'].includes(key))
                    .map(([accion, valor]) => (
                      <label key={accion}>
                        <input
                          type="checkbox"
                          checked={valor}
                          onChange={(e) => handlePermisoChange(
                            permiso.id, moduloKey, accion, e.target.checked
                          )}
                        />
                        {accion}
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
        <button onClick={guardarCambios} disabled={loading}>
          {loading ? 'Guardando...' : 'Guardar Cambios'}
        </button>
        <button onClick={() => window.location.reload()}>Cancelar</button>
      </div>
    </div>
  );
};

export default GestionPermisos;
```

---

## Modelo de Datos

### Tabla: `api_permisorol`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID | ID único del permiso |
| `rol` | VARCHAR(50) | Rol al que aplica (`administrador`, `veterinario`, etc.) |
| `modulo` | VARCHAR(50) | Módulo del sistema (`dashboard`, `citas`, etc.) |
| `permisos` | JSON | Objeto JSON con permisos: `{"ver": true, "crear": false}` |
| `descripcion_modulo` | VARCHAR(200) | Descripción del módulo (opcional) |
| `fecha_creacion` | TIMESTAMP | Fecha de creación |
| `fecha_modificacion` | TIMESTAMP | Última modificación |

**Restricciones:**
- `UNIQUE (rol, modulo)` - Un rol solo puede tener UNA configuración por módulo

### Estructura JSON del campo `permisos`

```json
{
  "ver": true,
  "crear": false,
  "editar": true,
  "eliminar": false,
  "aplicar": true,
  "historial": true,
  "calendario_general": false,
  "mi_calendario": true,
  "horarios": false,
  "slots": false,
  "generar": false
}
```

Las claves dependen del módulo. Ver endpoint `/modulos-disponibles/` para saber qué acciones tiene cada módulo.

---

## Seguridad

### ⚠️ Importante

1. **Solo Administradores**: Este módulo debe estar protegido para que solo admin pueda acceder
2. **Validación Backend**: El backend SIEMPRE valida permisos, el frontend solo oculta/muestra UI
3. **No usar para autenticación**: Los permisos son para autorización (qué puede hacer), no autenticación (quién es)

### Cómo proteger el módulo

```python
# En api/views.py - PermisoRolViewSet
class PermisoRolViewSet(viewsets.ModelViewSet):
    # Descomentar esta línea:
    permission_classes = [EsAdministrador]
```

---

## Troubleshooting

### Problema: Los permisos no se aplican

**Solución**: Verifica que el endpoint `/api/auth/permisos/` esté usando la BD y no el diccionario hardcodeado.

```python
# En api/permissions.py
def obtener_permisos(cls, rol):
    # Debe buscar primero en la BD
    permisos_db = PermisoRol.objects.filter(rol=rol)
    if permisos_db.exists():
        return permisos_dict
```

### Problema: Error "unique constraint violation"

**Solución**: Ya existe un permiso para ese `(rol, modulo)`. Usa `PATCH` en lugar de `POST`, o usa `/actualizar-masivo/` que hace `update_or_create`.

### Problema: Módulo no aparece en el frontend

**Solución**: El módulo debe estar en dos lugares:
1. Endpoint `/modulos-disponibles/` en `views.py`
2. Diccionario hardcodeado en `permissions.py` (como fallback)

---

## Próximos Pasos

1. **Implementar UI en frontend** usando el componente React de ejemplo
2. **Proteger el endpoint** con `permission_classes = [EsAdministrador]`
3. **Agregar logs** para auditoría de cambios de permisos
4. **Exportar/Importar** configuraciones de permisos (JSON)
5. **Templates de roles** (ej: "Veterinario Junior" vs "Veterinario Senior")

---

## Resumen de Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/permisos-rol/` | Listar todos los permisos |
| GET | `/api/permisos-rol/{id}/` | Ver un permiso específico |
| POST | `/api/permisos-rol/` | Crear nuevo permiso |
| PATCH | `/api/permisos-rol/{id}/` | Actualizar permiso |
| DELETE | `/api/permisos-rol/{id}/` | Eliminar permiso |
| GET | `/api/permisos-rol/por-rol/?rol=X` | Permisos de un rol |
| POST | `/api/permisos-rol/actualizar-masivo/` | Actualizar múltiples |
| GET | `/api/permisos-rol/modulos-disponibles/` | Lista de módulos |
| POST | `/api/permisos-rol/inicializar-defaults/` | Crear permisos default |

---

**Usuario Admin precargado:**
```
Email: admin@huellitas.com
Contraseña: admin123
```

**¡IMPORTANTE!** Cambiar la contraseña en producción.
