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

# 🐍 DJANGO BACKEND - CONTEXTO PARA IMPLEMENTACIÓN DE VACUNAS

## 🎯 **OBJETIVO**
Implementar los endpoints backend en Django para sincronizar con el **módulo de vacunas frontend que ya está 100% funcional**.

---

## 📊 **MÓDULO DE VACUNAS - FRONTEND COMPLETADO**

### ✅ **LO QUE YA ESTÁ HECHO (Frontend Angular)**
- **Interfaz completa:** CRUD, filtros, búsqueda, estadísticas, modales
- **Integración con inventario:** Selecciona productos tipo "vacuna" automáticamente
- **Anti-duplicación:** Filtra vacunas ya registradas para evitar duplicados
- **Actualizaciones locales:** Sin recarga de página, UX fluida
- **Validaciones:** Formularios reactivos con TypeScript
- **Estilos consistentes:** Tarjetas estadísticas como otros módulos

### 🔧 **LO QUE NECESITA EL BACKEND (Django)**
1. **Modelo Vacuna** - Estructura de datos específica
2. **Endpoints REST** - CRUD + cambio de estado
3. **Filtrado de inventario** - Solo productos tipo "vacuna"
4. **Respuestas consistentes** - Formato JSON estándar

---

## 📋 **ENDPOINTS REQUERIDOS**

### 🔗 **URLs a implementar en Django:**
```python
# vacunas/urls.py (CREAR ESTE ARCHIVO)
from django.urls import path
from . import views

urlpatterns = [
    # GESTIÓN DE VACUNAS
    path('vacunas/', views.VacunaListCreateView.as_view(), name='vacuna-list-create'),
    path('vacunas/<int:pk>/', views.VacunaRetrieveUpdateDestroyView.as_view(), name='vacuna-detail'),
    path('vacunas/<int:pk>/cambiar-estado/', views.cambiar_estado_vacuna, name='vacuna-cambiar-estado'),
    
    # INVENTARIO (si no existe, modificar existing)
    path('productos/', views.ProductoListView.as_view(), name='producto-list'),  # Con filtro ?tipo=vacuna
]
```

---

## 🗄️ **MODELO DJANGO A IMPLEMENTAR**

### 📊 **Vacuna Model (CREAR):**
```python
# vacunas/models.py
from django.db import models
import json

class Vacuna(models.Model):
    # Campos básicos (heredados del inventario)
    nombre = models.CharField(max_length=200, help_text="Tomado del inventario - readonly en frontend")
    enfermedad_previene = models.CharField(max_length=300, help_text="Tomado del inventario - readonly en frontend")
    
    # Campos específicos de protocolo de vacunación
    especies_aplicables = models.JSONField(
        default=list, 
        help_text="Array de especies: ['Perro', 'Gato', 'Ambos']"
    )
    frecuencia_meses = models.PositiveIntegerField(
        help_text="Cada cuántos meses se debe aplicar (ej: 12 = anual)"
    )
    edad_minima_semanas = models.PositiveIntegerField(
        help_text="Edad mínima en semanas para primera aplicación"
    )
    edad_maxima_semanas = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Edad máxima recomendada (null = sin límite)"
    )
    dosis_total = models.PositiveIntegerField(
        default=1,
        help_text="Número total de dosis en el protocolo completo"
    )
    intervalo_dosis_semanas = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Semanas entre dosis (solo si dosis_total > 1)"
    )
    es_obligatoria = models.BooleanField(
        default=False,
        help_text="True = Obligatoria, False = Opcional"
    )
    
    # Control y metadatos
    estado = models.CharField(
        max_length=20,
        choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')],
        default='Activo'
    )
    producto_inventario_id = models.PositiveIntegerField(
        help_text="FK al producto del inventario (sin foreign key directa)"
    )
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'vacunas'
        verbose_name = 'Vacuna'
        verbose_name_plural = 'Vacunas'
        ordering = ['-fecha_modificacion']
    
    def __str__(self):
        return f"{self.nombre} - {self.enfermedad_previene}"
    
    @property
    def especies_str(self):
        """Convierte array de especies a string para display"""
        if isinstance(self.especies_aplicables, list):
            return ", ".join(self.especies_aplicables)
        return str(self.especies_aplicables)
```

---

## 🔧 **VIEWS A IMPLEMENTAR**

### 📝 **views.py (CREAR O ACTUALIZAR):**
```python
# vacunas/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Vacuna
from .serializers import VacunaSerializer
# Importar también ProductoSerializer si existe

class VacunaListCreateView(generics.ListCreateAPIView):
    queryset = Vacuna.objects.all()
    serializer_class = VacunaSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por estado
        estado = self.request.query_params.get('estado')
        if estado and estado != 'todas':
            queryset = queryset.filter(estado__iexact=estado)
        
        # Filtro de búsqueda
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(enfermedad_previene__icontains=search) |
                Q(especies_aplicables__icontains=search)
            )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Estadísticas para el frontend
        total = queryset.count()
        activas = queryset.filter(estado='Activo').count()
        inactivas = queryset.filter(estado='Inactivo').count()
        obligatorias = queryset.filter(es_obligatoria=True).count()
        
        return Response({
            'data': serializer.data,
            'estadisticas': {
                'total': total,
                'activas': activas, 
                'inactivas': inactivas,
                'obligatorias': obligatorias
            },
            'message': 'Vacunas obtenidas exitosamente',
            'status': 'success'
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'Vacuna creada exitosamente',
                'status': 'success'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'data': None,
            'message': 'Error al crear vacuna',
            'errors': serializer.errors,
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)

class VacunaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacuna.objects.all()
    serializer_class = VacunaSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'Vacuna actualizada exitosamente',
                'status': 'success'
            })
        
        return Response({
            'data': None,
            'message': 'Error al actualizar vacuna',
            'errors': serializer.errors,
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'data': None,
            'message': 'Vacuna eliminada exitosamente',
            'status': 'success'
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
def cambiar_estado_vacuna(request, pk):
    try:
        vacuna = Vacuna.objects.get(pk=pk)
        nuevo_estado = 'Inactivo' if vacuna.estado == 'Activo' else 'Activo'
        vacuna.estado = nuevo_estado
        vacuna.save()
        
        serializer = VacunaSerializer(vacuna)
        return Response({
            'data': serializer.data,
            'message': f'Estado cambiado a {nuevo_estado}',
            'status': 'success'
        })
    
    except Vacuna.DoesNotExist:
        return Response({
            'data': None,
            'message': 'Vacuna no encontrada',
            'status': 'error'
        }, status=status.HTTP_404_NOT_FOUND)

# MODIFICAR ProductoListView EXISTENTE para agregar filtro tipo=vacuna
class ProductoListView(generics.ListAPIView):
    # ... código existente ...
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # AGREGAR ESTE FILTRO para vacunas
        tipo = self.request.query_params.get('tipo')
        if tipo == 'vacuna':
            queryset = queryset.filter(
                Q(tipo__icontains='vacuna') |
                Q(subtipo__icontains='vacuna') |
                Q(nombre__icontains='vacuna') |
                Q(descripcion__icontains='vacuna')
            ).filter(estado='Activo')  # Solo productos activos
        
        return queryset
```

---

## 📄 **SERIALIZER A IMPLEMENTAR**

### 🔧 **serializers.py (CREAR):**
```python
# vacunas/serializers.py
from rest_framework import serializers
from .models import Vacuna

class VacunaSerializer(serializers.ModelSerializer):
    especies_str = serializers.ReadOnlyField()  # Para display en frontend
    
    class Meta:
        model = Vacuna
        fields = [
            'id',
            'nombre', 
            'enfermedad_previene',
            'especies_aplicables',
            'especies_str',
            'frecuencia_meses',
            'edad_minima_semanas', 
            'edad_maxima_semanas',
            'dosis_total',
            'intervalo_dosis_semanas',
            'es_obligatoria',
            'estado',
            'producto_inventario_id',
            'fecha_creacion',
            'fecha_modificacion'
        ]
        extra_kwargs = {
            'fecha_creacion': {'read_only': True},
            'fecha_modificacion': {'read_only': True}
        }
    
    def validate(self, data):
        """Validaciones personalizadas"""
        if data.get('dosis_total', 1) > 1 and not data.get('intervalo_dosis_semanas'):
            raise serializers.ValidationError({
                'intervalo_dosis_semanas': 'Requerido cuando dosis_total > 1'
            })
        
        if data.get('edad_maxima_semanas') and data.get('edad_minima_semanas'):
            if data['edad_maxima_semanas'] <= data['edad_minima_semanas']:
                raise serializers.ValidationError({
                    'edad_maxima_semanas': 'Debe ser mayor que la edad mínima'
                })
        
        return data
```

---

## ⚙️ **CONFIGURACIÓN DE DJANGO**

### 📦 **settings.py (AGREGAR):**
```python
INSTALLED_APPS = [
    # ... apps existentes ...
    'vacunas',  # AGREGAR ESTA APP
]
```

### 🔗 **main urls.py (AGREGAR):**
```python
urlpatterns = [
    # ... URLs existentes ...
    path('api/', include('vacunas.urls')),  # AGREGAR ESTA LÍNEA
]
```

---

## 💾 **MIGRACIÓN**

### 🗄️ **Comandos a ejecutar:**
```bash
# 1. Crear la app (si no existe)
python manage.py startapp vacunas

# 2. Crear migración
python manage.py makemigrations vacunas

# 3. Aplicar migración  
python manage.py migrate

# 4. Crear superusuario (si necesitas acceso admin)
python manage.py createsuperuser
```

---

## 🔍 **TESTING**

### ✅ **Endpoints a probar:**
1. **GET /api/vacunas/** - Lista con estadísticas
2. **POST /api/vacunas/** - Crear nueva vacuna
3. **PUT/PATCH /api/vacunas/1/** - Editar vacuna
4. **DELETE /api/vacunas/1/** - Eliminar vacuna
5. **POST /api/vacunas/1/cambiar-estado/** - Cambiar estado
6. **GET /api/productos/?tipo=vacuna** - Inventario de vacunas

### 📊 **Formato de respuesta esperado:**
```json
{
    "data": [...],
    "message": "Operación exitosa",
    "status": "success",
    "estadisticas": {  // Solo en GET lista
        "total": 10,
        "activas": 8,
        "inactivas": 2, 
        "obligatorias": 5
    }
}
```

---

## 🎯 **RESULTADO ESPERADO**
Una vez implementado este backend, el **módulo de vacunas frontend funcionará completamente**:
- ✅ Lista y crea vacunas desde inventario
- ✅ Filtra vacunas duplicadas automáticamente  
- ✅ CRUD completo sin recarga de página
- ✅ Estadísticas en tiempo real
- ✅ Búsqueda y filtros avanzados
- ✅ UX consistente con otros módulos

**🚀 El frontend YA ESTÁ LISTO, solo necesita estos endpoints para funcionar al 100%.**