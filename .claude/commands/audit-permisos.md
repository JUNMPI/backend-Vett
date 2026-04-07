# /audit-permisos

Audita la consistencia del sistema de permisos en todo el backend Django.

## Instrucciones

Leer y cruzar estos archivos:
1. `api/permissions.py` → clases DRF y diccionario de permisos por rol
2. `api/views.py` → `permission_classes` en cada ViewSet y `@action`
3. `api/urls.py` → rutas registradas
4. `api/models.py` → modelo `PermisoRol` (permisos dinámicos en BD)

### Verificaciones a realizar

**1. ViewSets sin permission_classes**
Detectar ViewSets sin `permission_classes` definido (heredan `IsAuthenticated` por defecto de settings — verificar).

**2. Acciones sin protección**
Detectar `@action` decorators que no verifican permisos internamente para operaciones sensibles (eliminar, modificar roles, etc).

**3. Módulos del diccionario vs uso real**
Cruzar los módulos definidos en `PermisosPorRol` (`api/permissions.py`) con los módulos usados en `PermisoRol` de la BD. Detectar módulos referenciados pero no definidos.

**4. Consistencia frontend ↔ backend**
Los módulos de permisos del backend deben coincidir con los que el frontend consulta en `GET /api/auth/permisos/`. Listar cualquier discrepancia.

**5. Endpoint /api/auth/permisos/**
Verificar que retorna la estructura completa esperada por el frontend:
```json
{
  "permisos": {
    "dashboard": {"ver": true},
    "citas": {"ver": true, "crear": true, ...},
    ...
  },
  "rol": "administrador"
}
```

**6. Roles definidos vs usados**
Verificar que todos los roles en `choices.py` (Administrador, Veterinario, Recepcionista, etc.) tienen permisos definidos en `api/permissions.py`.

### Formato de reporte

```
🔍 AUDITORÍA DE PERMISOS — Backend Veterinaria Huellitas
══════════════════════════════════════════════════════════

✅ ViewSets protegidos:        XX/XX
❌ ViewSets sin permisos:      X
⚠️  Acciones sin verificación: X
❌ Módulos sin definir:        X
⚠️  Discrepancias frontend:    X

DETALLE DE PROBLEMAS:
─────────────────────
[Lista de cada problema con archivo:línea y fix sugerido]

MÓDULOS DEFINIDOS EN BACKEND:
  dashboard, citas, mascotas, responsables, vacunas,
  historial_clinico, productos, trabajadores, veterinarios,
  reportes, configuracion

MÓDULOS ESPERADOS POR EL FRONTEND:
  [lista extraída de GUIA_FRONTEND_ROLES_PERMISOS.md]

DISCREPANCIAS: X módulos

RESUMEN:
Críticos (❌): X — requieren fix inmediato
Advertencias (⚠️): X — revisar antes de producción
```

Después del reporte, preguntar si el usuario quiere que se apliquen los fixes automáticamente.
