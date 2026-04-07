# /check-build

Verifica el estado del proyecto Django: imports, migraciones pendientes y errores de sintaxis.

## Instrucciones

1. Activar entorno virtual y ejecutar `python manage.py check 2>&1`
2. Si hay errores → leer el archivo indicado, corregir, volver a verificar
3. Ejecutar `python manage.py showmigrations 2>&1` → detectar migraciones no aplicadas
4. Ejecutar `python -m py_compile api/models.py api/serializers.py api/views.py api/permissions.py` → errores de sintaxis
5. Reportar resultado

### Formato de reporte

```
✅ BUILD DJANGO OK
─────────────────────────────
Sistema checks:       0 errores
Migraciones:          Todas aplicadas
Syntax check:         OK
Apps instaladas:      api ✅

[Si hay warnings del sistema Django, listarlos]
```

o si hay errores:

```
❌ BUILD DJANGO CON ERRORES
─────────────────────────────
Errores encontrados: X

1. api/models.py:línea — descripción
   → Fix aplicado: descripción del cambio

Migraciones pendientes:
  → api: 0021_xxx (ejecutar: python manage.py migrate)
```

### Reglas de fix automático
- **ImportError / ModuleNotFoundError**: verificar que el módulo esté en requirements.txt e instalado
- **FieldError**: verificar nombre de campo en el modelo correspondiente
- **MigrationError**: nunca modificar migraciones ya aplicadas — crear una nueva
- **Migraciones pendientes**: reportar, no aplicar automáticamente (puede afectar producción)

Ejecutar siempre antes de hacer commit al backend.
