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
- **Vacunaciones** con seguimiento de dosis
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

### 📦 **Inventario**
- `GET/POST /api/productos/` - Productos e inventario
- `GET /api/productos/activos/` - Solo productos activos
- `PATCH /api/productos/{id}/activar/` - Activar producto
- `PATCH /api/productos/{id}/desactivar/` - Desactivar producto

### 🔍 **Filtros Especiales**
- `GET /api/especialidades/activos/` - Solo especialidades activas
- `GET /api/trabajadores/veterinarios/` - Solo veterinarios
- `GET /api/productos/count/` - Conteo de productos

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
**Estado**: Desarrollo Activo  
**Última Actualización**: Enero 2025  

### ✅ **Características Implementadas**
- [x] Autenticación JWT completa
- [x] CRUD completo para todos los modelos
- [x] Sistema de roles y permisos básicos
- [x] Soft delete con estados
- [x] Análisis de rentabilidad
- [x] Gestión de inventario
- [x] Historial clínico

### 🔄 **Próximas Características**
- [ ] Dashboard de métricas
- [ ] Reportes en PDF
- [ ] Notificaciones automáticas
- [ ] Sistema de backup
- [ ] API de estadísticas avanzadas

---

**¿Preguntas o sugerencias?** Abre un issue en el repositorio.