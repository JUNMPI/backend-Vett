# Filtrado Automático de Citas por Rol

## 🎯 Cambios Implementados

El sistema ahora **filtra automáticamente** las citas según el rol del usuario autenticado:

### Comportamiento por Rol

| Rol | Endpoint GET /api/citas/ | ¿Qué Ve? |
|-----|-------------------------|----------|
| **Veterinario** | `/api/citas/` | ✅ Solo **SUS** citas (automático) |
| **Recepcionista** | `/api/citas/` | ✅ **TODAS** las citas |
| **Administrador** | `/api/citas/` | ✅ **TODAS** las citas |

---

## 🔧 Cambios Técnicos

### 1. Endpoint Principal: GET /api/citas/

**Antes:**
```typescript
// Mostraba TODAS las citas sin importar el rol
const response = await axios.get('/api/citas/');
// Veterinario veía citas de TODOS los veterinarios ❌
```

**Ahora:**
```typescript
// Filtra automáticamente según el rol del usuario autenticado
const response = await axios.get('/api/citas/');

// Si es VETERINARIO → Solo ve SUS citas ✅
// Si es RECEPCIONISTA/ADMIN → Ve TODAS las citas ✅
```

### 2. Endpoint Mi Calendario: GET /api/citas/mi-calendario/

**Antes:**
```typescript
// Requería pasar veterinario_id manualmente
const response = await axios.get('/api/citas/mi-calendario/?veterinario_id=uuid');
```

**Ahora:**
```typescript
// Detecta automáticamente el veterinario del usuario autenticado
const response = await axios.get('/api/citas/mi-calendario/?fecha=2025-10-06');
// Ya NO necesita veterinario_id ✅
```

**Query Params:**
- `fecha` (opcional): YYYY-MM-DD. Si no se especifica, usa el día actual.

**Response:**
```json
{
  "fecha": "2025-10-06",
  "veterinario": {
    "id": "uuid",
    "nombre": "Carlos Alberto Ramirez Perez"
  },
  "total_citas": 3,
  "citas": [
    {
      "id": "uuid",
      "hora": "09:00:00",
      "estado": "confirmada",
      "mascota": {
        "id": "uuid",
        "nombre": "Rocky",
        "especie": "Perro",
        "raza": "Labrador"
      },
      "responsable": {
        "id": "uuid",
        "nombre": "Juan Pérez",
        "telefono": "987654321"
      },
      "servicio": {
        "id": "uuid",
        "nombre": "Consulta General",
        "categoria": "CONSULTA",
        "duracion_minutos": 30,
        "precio": "50.00"
      },
      "notas": "Primera consulta"
    }
  ]
}
```

---

## 💻 Implementación en el Frontend

### Escenario 1: Veterinario - Solo ve sus citas

```typescript
// auth.service.ts
const user = AuthService.getUserInfo();

if (user.rol === 'veterinario') {
  // Obtener SUS citas (filtrado automático)
  const response = await axios.get('/api/citas/');
  // Solo retorna citas donde veterinario.id === user.veterinario.id

  // O usar el endpoint específico para calendario
  const calendario = await axios.get('/api/citas/mi-calendario/');
  // Detecta automáticamente su ID de veterinario
}
```

### Escenario 2: Recepcionista - Ve todas las citas

```typescript
if (user.rol === 'recepcionista') {
  // Ver TODAS las citas
  const response = await axios.get('/api/citas/');

  // Opcionalmente filtrar por veterinario específico
  const citasDeUnVet = await axios.get('/api/citas/?veterinario_id=uuid');
}
```

### Escenario 3: Admin - Ve todas, puede filtrar

```typescript
if (user.rol === 'administrador') {
  // Ver TODAS las citas
  const response = await axios.get('/api/citas/');

  // Filtrar por veterinario específico
  const citasDeUnVet = await axios.get('/api/citas/?veterinario_id=uuid');

  // Usar calendario de recepción (todas las citas)
  const calendario = await axios.get('/api/citas/calendario_recepcion/');
}
```

---

## 🎨 Componente de Gestión de Citas (React)

### Ejemplo Completo

```tsx
// GestionCitas.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import AuthService from './auth.service';

interface Cita {
  id: string;
  fecha: string;
  hora: string;
  estado: string;
  mascota: {
    nombre: string;
    especie: string;
  };
  responsable: {
    nombre: string;
    telefono: string;
  };
  veterinario: {
    nombre: string;
  };
  servicio: {
    nombre: string;
    precio: string;
  };
}

const GestionCitas: React.FC = () => {
  const [citas, setCitas] = useState<Cita[]>([]);
  const [loading, setLoading] = useState(true);
  const user = AuthService.getUserInfo();

  useEffect(() => {
    const cargarCitas = async () => {
      try {
        // El backend filtra automáticamente según el rol
        const response = await axios.get('/api/citas/');
        setCitas(response.data);
      } catch (error) {
        console.error('Error cargando citas:', error);
      } finally {
        setLoading(false);
      }
    };

    cargarCitas();
  }, []);

  if (loading) return <div>Cargando...</div>;

  return (
    <div className="gestion-citas">
      <h1>
        {user?.rol === 'veterinario'
          ? 'Mis Citas'
          : 'Gestión de Citas'}
      </h1>

      {/* Mostrar info según el rol */}
      {user?.rol === 'veterinario' && (
        <div className="info-veterinario">
          <p>
            Mostrando solo tus citas asignadas.
            Total: {citas.length}
          </p>
        </div>
      )}

      {user?.rol !== 'veterinario' && (
        <div className="info-admin">
          <p>
            Mostrando todas las citas del sistema.
            Total: {citas.length}
          </p>
        </div>
      )}

      {/* Tabla de citas */}
      <table className="tabla-citas">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Hora</th>
            <th>Mascota</th>
            <th>Dueño</th>
            {/* Veterinario solo se muestra para admin/recepcionista */}
            {user?.rol !== 'veterinario' && <th>Veterinario</th>}
            <th>Servicio</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {citas.map(cita => (
            <tr key={cita.id}>
              <td>{cita.fecha}</td>
              <td>{cita.hora}</td>
              <td>
                {cita.mascota.nombre}
                <br />
                <small>{cita.mascota.especie}</small>
              </td>
              <td>
                {cita.responsable.nombre}
                <br />
                <small>{cita.responsable.telefono}</small>
              </td>
              {user?.rol !== 'veterinario' && (
                <td>{cita.veterinario.nombre}</td>
              )}
              <td>
                {cita.servicio.nombre}
                <br />
                <small>S/ {cita.servicio.precio}</small>
              </td>
              <td>
                <span className={`badge badge-${cita.estado}`}>
                  {cita.estado}
                </span>
              </td>
              <td>
                {/* Botones según permisos */}
                {AuthService.can('citas', 'editar') && (
                  <button onClick={() => handleEdit(cita.id)}>
                    Editar
                  </button>
                )}
                {AuthService.can('citas', 'eliminar') && (
                  <button onClick={() => handleCancel(cita.id)}>
                    Cancelar
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Botón crear solo para recepcionista/admin */}
      {AuthService.can('citas', 'crear') && (
        <button
          className="btn-crear"
          onClick={() => navigate('/citas/crear')}
        >
          Nueva Cita
        </button>
      )}
    </div>
  );
};

export default GestionCitas;
```

---

## 🔍 Verificación del Filtrado

### Probar con Veterinario

```bash
# 1. Login como veterinario
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "vet@huellitas.com", "password": "vet12345"}'

# 2. Obtener citas (solo verá las suyas)
curl http://localhost:8000/api/citas/ \
  -H "Authorization: Bearer <token>"

# 3. Mi calendario (sin necesidad de veterinario_id)
curl http://localhost:8000/api/citas/mi-calendario/ \
  -H "Authorization: Bearer <token>"
```

### Probar con Recepcionista

```bash
# 1. Login como recepcionista
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "recepcion@huellitas.com", "password": "recep12345"}'

# 2. Obtener todas las citas
curl http://localhost:8000/api/citas/ \
  -H "Authorization: Bearer <token>"

# Verá citas de TODOS los veterinarios
```

---

## ⚠️ IMPORTANTE para el Frontend

### ❌ NO hacer esto (Ya no es necesario)

```typescript
// ANTES: Filtrar manualmente en el frontend
const user = getUserInfo();
const todasLasCitas = await axios.get('/api/citas/');

// Filtrar manualmente si es veterinario ❌
const citasFiltradas = user.rol === 'veterinario'
  ? todasLasCitas.filter(c => c.veterinario.id === user.veterinario.id)
  : todasLasCitas;
```

### ✅ Hacer esto (Backend filtra automáticamente)

```typescript
// AHORA: Backend filtra automáticamente
const citas = await axios.get('/api/citas/');
// Ya vienen filtradas según el rol ✅

// Simplemente mostrar las citas
setCitas(citas);
```

---

## 🎯 Resumen de Cambios para el Frontend

| Acción | Antes | Ahora |
|--------|-------|-------|
| **GET /api/citas/** (veterinario) | Veía todas las citas | ✅ Solo ve sus citas |
| **GET /api/citas/** (recepcionista) | Veía todas las citas | ✅ Sigue viendo todas |
| **GET /api/citas/mi-calendario/** | Requería `veterinario_id` | ✅ Lo detecta automáticamente |
| **Filtrado en frontend** | Necesario para veterinarios | ✅ Ya no es necesario |

---

## 🚀 Ventajas

1. ✅ **Seguridad**: El veterinario no puede acceder a citas de otros veterinarios
2. ✅ **Simplicidad**: Frontend no necesita lógica de filtrado
3. ✅ **Performance**: Se filtran en la BD, no en el frontend
4. ✅ **Consistencia**: Mismo comportamiento en todos los endpoints
5. ✅ **Automático**: Se basa en el token JWT del usuario

---

## 📞 Endpoints Relacionados

- `GET /api/citas/` - Lista de citas (filtrado automático)
- `GET /api/citas/{id}/` - Detalle de una cita
- `GET /api/citas/mi-calendario/` - Calendario del veterinario (automático)
- `GET /api/citas/calendario_recepcion/` - Calendario completo (admin/recepcionista)
- `POST /api/citas/` - Crear cita (recepcionista/admin)
- `PATCH /api/citas/{id}/` - Editar cita

---

**Usuario de prueba veterinario:**
```
Email: vet@huellitas.com
Contraseña: vet12345
```

Ahora el sistema funciona correctamente: el veterinario solo ve sus citas, y recepcionista/admin ven todas! 🎉
