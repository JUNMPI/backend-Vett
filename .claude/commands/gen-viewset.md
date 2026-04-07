# /gen-viewset

Genera un nuevo ViewSet Django REST Framework siguiendo los patrones exactos de este proyecto (Veterinaria Huellitas).

## Instrucciones

El usuario dará el nombre del modelo y el endpoint. Debes:

1. **Leer** `api/models.py` → verificar si el modelo ya existe o hay que crearlo
2. **Leer** `api/serializers.py` → seguir el patrón exacto de serializers existentes
3. **Leer** `api/views.py` → seguir el patrón de ViewSets existentes
4. **Leer** `api/urls.py` → ver cómo registrar la ruta

### Patrón obligatorio del modelo (si hay que crearlo)
```python
import uuid
from django.db import models
from .choices import Estado

class {Modelo}(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ... campos del modelo
    estado = models.CharField(max_length=10, choices=Estado.ESTADO_CHOICES, default='Activo')

    class Meta:
        db_table = '{tabla}'
        verbose_name = '{nombre}'
        verbose_name_plural = '{nombres}'

    def __str__(self):
        return f"{self.campo_principal}"
```

### Patrón obligatorio del serializer
```python
class {Modelo}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {Modelo}
        fields = '__all__'
```

### Patrón obligatorio del ViewSet
```python
class {Modelo}ViewSet(viewsets.ModelViewSet):
    queryset = {Modelo}.objects.all()
    serializer_class = {Modelo}Serializer
    permission_classes = [{PermisosAdecuados}]

    def get_queryset(self):
        return {Modelo}.objects.filter(estado='Activo')

    @action(detail=False, methods=['get'], url_path='activos')
    def activos(self, request):
        queryset = {Modelo}.objects.filter(estado='Activo')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        obj = self.get_object()
        obj.estado = 'Inactivo'
        obj.save()
        return Response({'status': 'desactivado'})

    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        obj = self.get_object()
        obj.estado = 'Activo'
        obj.save()
        return Response({'status': 'activado'})
```

### Registro en urls.py
```python
router.register(r'{endpoint}', {Modelo}ViewSet)
```

### Reglas
- Siempre usar UUID como primary key (`default=uuid.uuid4`)
- Siempre incluir soft delete (`estado` Activo/Inactivo) en lugar de hard delete
- Siempre agregar `permission_classes` — nunca dejar sin permisos
- Siempre crear migración después: `python manage.py makemigrations`
- Si el modelo tiene relaciones → especificar campos en serializer en lugar de `__all__`

## Argumento esperado
`/gen-viewset {NombreModelo} {endpoint-url}`
Ej: `/gen-viewset Consultorio consultorios`

## Pasos finales tras generar
1. Ejecutar `/check-build` para verificar que no hay errores
2. Crear la migración: `python manage.py makemigrations`
3. Revisar la migración generada antes de aplicarla
