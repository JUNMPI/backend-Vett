# 🏥 Veterinaria "Huellitas" - Backend API

Sistema de gestión veterinaria desarrollado con **Django REST Framework** que proporciona una API completa para la administración de una clínica veterinaria.

## 🚀 Características Principales

### 👥 **Gestión de Usuarios y Roles**
- **Autenticación JWT** con `djangorestframework-simplejwt`
- **Modelo de Usuario personalizado** usando email como identificador
- **Sistema de roles**: Administrador, Veterinario, Recepcionista, Inventario, Responsable
- **Gestión de trabajadores** con estados activo/inactivo

### 🐾 **Gestión Veterinaria**
- **Especialidades médicas** con sistema de estados
- **Veterinarios** con días de trabajo y especialidades
- **Mascotas** con historial clínico completo
- **Responsables** (dueños) con información de contacto
- **Citas médicas** con estados y seguimiento
- **Servicios veterinarios** con precios

### 📦 **Gestión de Inventario**
- **Productos** con categorización (medicamentos, vacunas, higiene, alimentos)
- **Control de stock** y fechas de vencimiento
- **Análisis de rentabilidad** con precio_compra y precio_venta
- **Proveedores** y tipos de documento

### 🏥 **Historiales Médicos**
- **Historial clínico único** por mascota
- **Atenciones médicas** con diagnósticos y tratamientos
- **Sistema de vacunación inteligente** con protocolos automatizados
- **Seguimiento avanzado de dosis** individual y protocolo completo
- **Generación automática** de números de historia

## 🛠️ Tecnologías Utilizadas

- **Python 3.13** + **Django 5.2.1**
- **Django REST Framework 3.16.0** para API REST
- **PostgreSQL** como base de datos
- **JWT Authentication** con Simple JWT
- **Django CORS Headers** para integración frontend
- **UUID** como claves primarias para mayor seguridad

## 📁 Estructura del Proyecto

```
veterinaria-backend/
├── api/                    # Aplicación principal
│   ├── models.py          # Modelos de base de datos
│   ├── serializers.py     # Serializadores DRF
│   ├── views.py           # ViewSets y lógica de negocio
│   ├── urls.py            # Rutas de la API
│   ├── choices.py         # Constantes y opciones
│   └── migrations/        # Migraciones de BD
├── huellitas/             # Configuración Django
│   ├── settings.py        # Configuraciones principales
│   ├── urls.py           # URLs del proyecto
│   └── wsgi.py           # WSGI config
├── create_productos.py    # Script para datos de prueba
├── requirements.txt       # Dependencias Python
└── manage.py             # CLI de Django
```

## ⚙️ Instalación y Configuración

### 1. **Clonar el repositorio**
```bash
git clone git@github.com:JUNMPI/backend-Vett.git
cd backend-Vett
```

### 2. **Crear y activar entorno virtual**
```bash
# Crear entorno virtual
python -m venv env_veterinaria

# Activar entorno (Windows)
env_veterinaria\Scripts\activate

# Activar entorno (Linux/macOS)
source env_veterinaria/bin/activate
```

### 3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 4. **Configurar base de datos**

Edita `huellitas/settings.py` con tus credenciales de PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tu_base_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

### 6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

### 7. **Cargar datos de prueba (Opcional)**
```bash
python create_productos.py
```

### 8. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/api/`

## 🔑 Autenticación

### Obtener Token JWT
```bash
POST /api/login/
Content-Type: application/json

{
    "email": "usuario@email.com",
    "password": "password"
}
```

### Usar Token en Requests
```bash
Authorization: Bearer <tu_access_token>
```

## 📚 Endpoints Principales

### 🏥 **Gestión General**
- `GET/POST /api/especialidades/` - Especialidades médicas
- `GET/POST /api/tipos-documento/` - Tipos de documento
- `GET/POST /api/consultorios/` - Consultorios
- `GET/POST /api/servicios/` - Servicios veterinarios

### 👥 **Gestión de Personal**
- `GET/POST /api/trabajadores/` - Trabajadores
- `GET/POST /api/veterinarios/` - Veterinarios
- `PATCH /api/trabajadores/{id}/activar/` - Activar trabajador
- `PATCH /api/trabajadores/{id}/desactivar/` - Desactivar trabajador

### 🐾 **Gestión de Mascotas**
- `GET/POST /api/responsables/` - Dueños de mascotas
- `GET/POST /api/mascotas/` - Mascotas
- `GET/POST /api/citas/` - Citas veterinarias

### 💉 **Sistema de Vacunación**
- `GET/POST /api/vacunas/` - Catálogo de vacunas
- `POST /api/vacunas/{id}/aplicar/` - **Aplicación unificada de vacunas**
- `GET /api/historial-vacunacion/` - Historial de vacunación
- **Soporte para dosis individuales y protocolos completos**
- 📖 **Ver**: [`VACUNACION_API_DOCS.md`](./VACUNACION_API_DOCS.md) para documentación detallada

### 📦 **Inventario**
- `GET/POST /api/productos/` - Productos e inventario
- `GET /api/productos/activos/` - Solo productos activos
- `PATCH /api/productos/{id}/activar/` - Activar producto
- `PATCH /api/productos/{id}/desactivar/` - Desactivar producto

### 🔍 **Filtros Especiales**
- `GET /api/especialidades/activos/` - Solo especialidades activas
- `GET /api/trabajadores/veterinarios/` - Solo veterinarios
- `GET /api/productos/count/` - Conteo de productos

## 💉 Sistema de Vacunación Inteligente

### 🎯 **Endpoint Unificado de Vacunación**

**URL**: `POST /api/vacunas/{id}/aplicar/`

El sistema soporta **dos modos de aplicación** en un solo endpoint:

#### **Modo 1: Dosis Individual**
```json
{
  "mascota_id": "uuid",
  "fecha_aplicacion": "2025-01-15",
  "veterinario_id": "uuid",
  "dosis_numero": 1,
  "observaciones": "Primera dosis",
  "protocolo_completo": false
}
```

#### **Modo 2: Protocolo Completo**
```json
{
  "mascota_id": "uuid",
  "fecha_aplicacion": "2025-01-15", 
  "veterinario_id": "uuid",
  "observaciones": "Protocolo completo",
  "protocolo_completo": true,
  "dosis_aplicadas": 3
}
```

### ✅ **Características del Sistema**
- **Cálculo automático** de próximas fechas según protocolo
- **Validación anti-duplicados** inteligente
- **Soporte para protocolos complejos** (JSON, cachorro, estándar)
- **Detección automática** de atrasos y reinicio de protocolos
- **Validación de fechas** (no permite fechas futuras)
- **Manejo de errores** con códigos específicos para frontend

### 🔄 **Flujo de Trabajo**
1. **Detección automática** del modo según parámetros
2. **Validación exhaustiva** de datos y fechas
3. **Cálculo inteligente** de dosis y próximas fechas
4. **Creación de registros** optimizada
5. **Respuesta estructurada** con información completa

## 💰 Análisis de Rentabilidad

El sistema incluye análisis de rentabilidad con los campos:
- `precio_compra`: Costo de adquisición
- `precio_venta`: Precio de venta al público
- **Margen**: `precio_venta - precio_compra`
- **% Rentabilidad**: `(margen / precio_compra) * 100`

## 🗄️ Modelos de Datos Principales

### **Usuario**
- Email único como identificador
- Roles: Administrador, Veterinario, Recepcionista, Inventario, Responsable
- Sistema de autenticación JWT

### **Mascota**
- Información completa (nombre, especie, raza, peso, etc.)
- Relación con responsable
- Historial clínico automático

### **Producto**
- Categorización por tipos (medicamento, vacuna, higiene, alimento, venta)
- Control de stock y vencimientos
- Análisis de costos y rentabilidad

### **Cita**
- Sistema completo de agendamiento
- Estados: Pendiente, Confirmada, Completada, Cancelada, Reprogramada
- Relación con veterinario, mascota y servicio

## 🔐 Consideraciones de Seguridad

⚠️ **Para producción, es necesario:**
- Cambiar `SECRET_KEY` y usar variables de entorno
- Establecer `DEBUG = False`
- Configurar `ALLOWED_HOSTS` apropiadamente
- Revisar configuración CORS
- Usar HTTPS para todas las comunicaciones

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso educativo y profesional.

## 👥 Autores

- **Desarrollo Backend**: Desarrollado con Django REST Framework
- **Asistencia Técnica**: Claude Code (Anthropic)

---

## 🚀 Estado del Proyecto

**Versión**: 1.0.0  
**Estado**: ✅ **LISTO PARA PRODUCCIÓN**  
**Última Actualización**: Enero 2025  
**Tests de Producción**: ✅ 100% Éxito  

### ✅ **Características Implementadas**
- [x] Autenticación JWT completa
- [x] CRUD completo para todos los modelos
- [x] Sistema de roles y permisos básicos
- [x] Soft delete con estados
- [x] Análisis de rentabilidad
- [x] Gestión de inventario
- [x] Historial clínico
- [x] **Sistema de vacunación inteligente**
- [x] **Aplicación unificada de dosis individuales y protocolos completos**
- [x] **Validaciones avanzadas anti-duplicados**
- [x] **Cálculo automático de próximas fechas de vacunación**

## 💉 **Sistema de Estados de Vacunación**

### **Estados Dinámicos Implementados**

El sistema calcula automáticamente el estado de cada vacuna en tiempo real:

- **`vigente`**: Vacuna activa con protección válida (>30 días para vencer)
- **`proxima`**: Vence en los próximos 30 días (requiere atención)
- **`vencida`**: Vencida hace menos de 60 días (requiere refuerzo)
- **`vencida_reinicio`**: Vencida hace más de 60 días (reiniciar protocolo)

### **Mascota de Prueba para Frontend**

**Luna (Golden Retriever)**
- **ID**: `e0469d55-9b2c-4ae5-9e0b-f191db1408f3`
- **Endpoint**: `GET /api/mascotas/e0469d55-9b2c-4ae5-9e0b-f191db1408f3/historial-vacunacion/`
- **Estados demostrados**: vigente, vencida
- **Protocolo aplicado**: Quintuple Canina (2 dosis)

### **Características del Sistema**
- ✅ **Cálculo dinámico**: Los estados se calculan en tiempo real
- ✅ **Transiciones automáticas**: Cambian automáticamente según fechas
- ✅ **Protocolos multi-dosis**: Soporte completo para vacunas de múltiples dosis
- ✅ **Validación de duplicados**: Previene aplicaciones incorrectas
- ✅ **Historial completo**: Seguimiento detallado por mascota

### 🔄 **Próximas Características**
- [ ] Dashboard de métricas
- [ ] Reportes en PDF
- [ ] Notificaciones automáticas
- [ ] Sistema de backup
- [ ] API de estadísticas avanzadas

---

**¿Preguntas o sugerencias?** Abre un issue en el repositorio.