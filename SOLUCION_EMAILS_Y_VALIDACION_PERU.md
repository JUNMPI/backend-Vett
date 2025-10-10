# 🇵🇪 SOLUCIÓN: Emails Únicos y Validación de Documentos Peruanos

**Fecha:** 2025-10-10
**Prioridad:** 🔴 CRÍTICA

---

## 🎯 DECISIONES CLAVE

### 1️⃣ **Responsable NO tiene acceso al sistema**
✅ **Decisión:** Eliminar completamente la relación `Usuario` en `Responsable`.

**Antes:**
```python
class Responsable(models.Model):
    email = models.EmailField(...)
    usuario = models.OneToOneField(Usuario, ...)  # ❌ INNECESARIO
```

**Después:**
```python
class Responsable(models.Model):
    email = models.EmailField(unique=True)  # ✅ Solo un email
    # No hay campo usuario
```

---

### 2️⃣ **Trabajador SÍ tiene acceso (debe hacer login)**
✅ **Decisión:** Eliminar campo `Trabajador.email` redundante, usar solo `Usuario.email`.

**Antes:**
```python
class Trabajador(models.Model):
    email = models.EmailField()  # ❌ REDUNDANTE
    usuario = models.OneToOneField(Usuario, ...)  # Usuario.email
```

**Después:**
```python
class Trabajador(models.Model):
    # No hay campo email directo
    usuario = models.OneToOneField(Usuario, ...)  # ✅ Solo Usuario.email

    @property
    def email(self):
        """Email viene del Usuario"""
        return self.usuario.email
```

---

### 3️⃣ **Validación de Documentos Peruanos**

#### Tipos de Documento en Perú:
- **DNI** (Documento Nacional de Identidad): 8 dígitos exactos
- **CE** (Carnet de Extranjería): 9 dígitos
- **Pasaporte**: Alfanumérico, 9-12 caracteres
- **RUC** (Registro Único de Contribuyentes): 11 dígitos

✅ **Decisión:** Implementar validación específica por tipo de documento.

---

## 📝 CAMBIOS EN MODELOS

### **1. Modelo Trabajador (Refactorizado)**

```python
class Trabajador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    # ❌ ELIMINADO: email = models.EmailField()
    telefono = models.CharField(max_length=20)
    tipodocumento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.CASCADE,
        related_name='trabajadores'
    )
    documento = models.CharField(max_length=20)
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='trabajador'
    )
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )

    class Meta:
        ordering = ['nombres']
        constraints = [
            # Documento único por tipo
            models.UniqueConstraint(
                fields=['tipodocumento', 'documento'],
                name='unique_trabajador_documento',
                violation_error_message='Ya existe un trabajador con este documento.'
            ),
        ]

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def email(self):
        """
        Email viene del Usuario (para login).
        Mantiene compatibilidad con código existente.
        """
        return self.usuario.email if self.usuario else None

    def clean(self):
        """
        Validación de documento según tipo (Perú)
        """
        super().clean()

        if self.documento and self.tipodocumento:
            tipo = self.tipodocumento.nombre.upper()
            doc = self.documento.strip()

            # DNI: 8 dígitos exactos
            if tipo == 'DNI':
                if not re.match(r'^\d{8}$', doc):
                    raise CoreValidationError({
                        'documento': 'El DNI debe tener exactamente 8 dígitos.'
                    })

            # Carnet de Extranjería: 9 dígitos
            elif tipo in ['CE', 'CARNET DE EXTRANJERIA', 'CARNET DE EXTRANJERÍA']:
                if not re.match(r'^\d{9}$', doc):
                    raise CoreValidationError({
                        'documento': 'El Carnet de Extranjería debe tener 9 dígitos.'
                    })

            # Pasaporte: Alfanumérico, 9-12 caracteres
            elif tipo == 'PASAPORTE':
                if not re.match(r'^[A-Z0-9]{9,12}$', doc):
                    raise CoreValidationError({
                        'documento': 'El Pasaporte debe tener entre 9 y 12 caracteres alfanuméricos.'
                    })

            # RUC: 11 dígitos
            elif tipo == 'RUC':
                if not re.match(r'^\d{11}$', doc):
                    raise CoreValidationError({
                        'documento': 'El RUC debe tener exactamente 11 dígitos.'
                    })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
```

---

### **2. Modelo Responsable (Refactorizado)**

```python
class Responsable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=254,
        unique=True,
        help_text="Email del responsable (para contacto)",
        db_index=True
    )
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    tipodocumento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.CASCADE,
        related_name='responsables'
    )
    emergencia = models.CharField(max_length=100, blank=True, null=True)
    # ❌ ELIMINADO: usuario = models.OneToOneField(Usuario, ...)

    class Meta:
        ordering = ['nombres']
        constraints = [
            # Documento único por tipo
            models.UniqueConstraint(
                fields=['tipodocumento', 'documento'],
                name='unique_responsable_documento',
                violation_error_message='Ya existe un responsable con este documento.'
            ),
        ]

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    def clean(self):
        """
        Validación de documento según tipo (Perú)
        """
        super().clean()

        if self.documento and self.tipodocumento:
            tipo = self.tipodocumento.nombre.upper()
            doc = self.documento.strip()

            # DNI: 8 dígitos exactos
            if tipo == 'DNI':
                if not re.match(r'^\d{8}$', doc):
                    raise CoreValidationError({
                        'documento': 'El DNI debe tener exactamente 8 dígitos.'
                    })

            # Carnet de Extranjería: 9 dígitos
            elif tipo in ['CE', 'CARNET DE EXTRANJERIA', 'CARNET DE EXTRANJERÍA']:
                if not re.match(r'^\d{9}$', doc):
                    raise CoreValidationError({
                        'documento': 'El Carnet de Extranjería debe tener 9 dígitos.'
                    })

            # Pasaporte: Alfanumérico, 9-12 caracteres
            elif tipo == 'PASAPORTE':
                if not re.match(r'^[A-Z0-9]{9,12}$', doc):
                    raise CoreValidationError({
                        'documento': 'El Pasaporte debe tener entre 9 y 12 caracteres alfanuméricos.'
                    })

            # RUC: 11 dígitos
            elif tipo == 'RUC':
                if not re.match(r'^\d{11}$', doc):
                    raise CoreValidationError({
                        'documento': 'El RUC debe tener exactamente 11 dígitos.'
                    })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
```

---

## 📝 CAMBIOS EN SERIALIZERS

### **1. TrabajadorSerializer (Refactorizado)**

```python
class TrabajadorSerializer(serializers.ModelSerializer):
    tipodocumento = serializers.PrimaryKeyRelatedField(queryset=TipoDocumento.objects.all())
    tipodocumento_nombre = serializers.CharField(source='tipodocumento.nombre', read_only=True)
    usuario = UsuarioSerializer()
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    # ✅ Email calculado desde Usuario (read-only)
    email = serializers.EmailField(source='usuario.email', read_only=True)

    class Meta:
        model = Trabajador
        fields = [
            'id', 'nombres', 'apellidos', 'email', 'telefono',
            'tipodocumento', 'tipodocumento_nombre', 'documento', 'usuario', 'estado'
        ]

    def validate(self, attrs):
        """
        Validación completa
        """
        # Validar documento duplicado
        documento = attrs.get('documento')
        tipodocumento = attrs.get('tipodocumento')

        if documento and tipodocumento:
            query = Trabajador.objects.filter(
                documento=documento,
                tipodocumento=tipodocumento
            )
            if self.instance:
                query = query.exclude(id=self.instance.id)

            if query.exists():
                raise serializers.ValidationError({
                    "documento": "Ya existe un trabajador con este documento."
                })

        return attrs

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        usuario_serializer = UsuarioSerializer(data=usuario_data)
        usuario_serializer.is_valid(raise_exception=True)
        usuario = usuario_serializer.save()

        trabajador = Trabajador.objects.create(usuario=usuario, **validated_data)
        return trabajador

    def update(self, instance, validated_data):
        usuario_data = validated_data.pop('usuario', None)

        if usuario_data:
            usuario_serializer = UsuarioSerializer(
                instance.usuario,
                data=usuario_data,
                partial=True
            )
            usuario_serializer.is_valid(raise_exception=True)
            usuario_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
```

---

### **2. ResponsableSerializer (Refactorizado)**

```python
class ResponsableSerializer(serializers.ModelSerializer):
    # ❌ ELIMINADO: usuario = UsuarioSerializer()
    tipodocumento = serializers.PrimaryKeyRelatedField(queryset=TipoDocumento.objects.all())
    tipodocumento_nombre = serializers.CharField(source='tipodocumento.nombre', read_only=True)
    mascotas = MascotaSerializer(many=True, read_only=True)

    class Meta:
        model = Responsable
        fields = [
            'id', 'nombres', 'apellidos', 'email', 'telefono', 'direccion',
            'ciudad', 'documento', 'tipodocumento', 'tipodocumento_nombre',
            'emergencia', 'mascotas'
        ]

    def validate(self, attrs):
        """
        Validación completa
        """
        # Validar email único
        email = attrs.get('email')
        if email:
            query = Responsable.objects.filter(email=email)
            if self.instance:
                query = query.exclude(id=self.instance.id)

            if query.exists():
                raise serializers.ValidationError({
                    "email": "Este email ya está registrado por otro responsable."
                })

        # Validar documento único
        documento = attrs.get('documento')
        tipodocumento = attrs.get('tipodocumento')

        if documento and tipodocumento:
            query = Responsable.objects.filter(
                documento=documento,
                tipodocumento=tipodocumento
            )
            if self.instance:
                query = query.exclude(id=self.instance.id)

            if query.exists():
                raise serializers.ValidationError({
                    "documento": "Ya existe un responsable con este documento."
                })

        return attrs

    def create(self, validated_data):
        # ✅ Simplificado: No hay usuario
        responsable = Responsable.objects.create(**validated_data)
        return responsable

    def update(self, instance, validated_data):
        # ✅ Simplificado: Solo actualizar campos directos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
```

---

## 🗃️ MIGRACIÓN DE DATOS

### **Script 1: Migrar Responsables (Eliminar Usuario)**

```python
# migracion_responsables.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Responsable, Usuario

print("=" * 60)
print("MIGRACION: Responsables sin Usuario")
print("=" * 60)

for responsable in Responsable.objects.all():
    print(f"\nResponsable: {responsable.nombres} {responsable.apellidos}")
    print(f"  Email Responsable: {responsable.email}")
    print(f"  Email Usuario: {responsable.usuario.email}")

    # Si están desincronizados, usar el email del Usuario (más reciente)
    if responsable.email != responsable.usuario.email:
        print(f"  [SYNC] Actualizando email de Responsable a Usuario.email")
        responsable.email = responsable.usuario.email

    # Guardar el ID del usuario para eliminarlo después
    usuario_id = responsable.usuario.id

    # Desasociar el usuario (esto se hace en la migración)
    # responsable.usuario = None
    # responsable.save()

    print(f"  [INFO] Usuario {usuario_id} se eliminará en migración")

print("\n" + "=" * 60)
print("IMPORTANTE: Este script es solo para análisis.")
print("La eliminación de Usuario se hace en la migración de Django.")
print("=" * 60)
```

---

### **Script 2: Limpiar Duplicados Actuales**

```python
# limpiar_duplicados_actual.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Trabajador, Responsable

print("=" * 60)
print("LIMPIEZA DE DUPLICADOS")
print("=" * 60)

# === TRABAJADORES ===
print("\n=== TRABAJADORES ===")

# Caso 1: junior alvines (71448712)
junior = Trabajador.objects.get(id='fe80d13b-8f49-4487-b793-124259541bd7')
print(f"1. {junior.nombres} {junior.apellidos}")
print(f"   Documento actual: {junior.documento}")
print(f"   [ACCION] Cambiar documento a: 71448713")
# junior.documento = '71448713'
# junior.save()

# Caso 2: Ximena Alvines (71448712) - mantener original
ximena = Trabajador.objects.get(id='4e84f660-c2d0-4779-b47c-54db4317486f')
print(f"2. {ximena.nombres} {ximena.apellidos}")
print(f"   Documento actual: {ximena.documento}")
print(f"   [OK] Mantener documento: 71448712")

# === RESPONSABLES ===
print("\n=== RESPONSABLES ===")

# Caso 1: Maria Garcia Lopez (12345678)
maria = Responsable.objects.get(id='c93ecbf0-90cc-4586-aa57-e87040354fed')
print(f"1. {maria.nombres} {maria.apellidos}")
print(f"   Documento actual: {maria.documento}")
print(f"   [ACCION] Cambiar documento a: 87654321")
# maria.documento = '87654321'
# maria.save()

# Caso 2: Juan Carlos Perez Lopez (12345678) - mantener original
juan = Responsable.objects.get(id='f0a9e302-03a9-4e54-804f-2a01b21c5188')
print(f"2. {juan.nombres} {juan.apellidos}")
print(f"   Documento actual: {juan.documento}")
print(f"   [OK] Mantener documento: 12345678")

print("\n" + "=" * 60)
print("DESCOMENTA LAS LINEAS .save() PARA APLICAR CAMBIOS")
print("=" * 60)
```

---

## 📋 PASOS DE IMPLEMENTACIÓN

### **Fase 1: Backup**
```bash
# Backup de base de datos
pg_dump -U huellitas -d Huellitas > backup_pre_migracion.sql
```

### **Fase 2: Limpiar Duplicados Actuales**
```bash
python limpiar_duplicados_actual.py
# Revisar cambios propuestos
# Descomentar .save() y ejecutar de nuevo
```

### **Fase 3: Modificar Modelos**
- Eliminar campo `Trabajador.email`
- Agregar `@property email` en Trabajador
- Eliminar campo `Responsable.usuario`
- Agregar `clean()` en ambos modelos
- Agregar `Meta.constraints` en ambos modelos

### **Fase 4: Crear Migración**
```bash
python manage.py makemigrations --name="remove_redundant_email_fields"
```

**IMPORTANTE:** La migración automática puede fallar. Necesitarás:

1. **Para Responsable.usuario:**
```python
# En la migración generada, ANTES de RemoveField:
migrations.RunPython(
    migrate_responsable_emails,  # Sincronizar emails
    migrations.RunPython.noop
),
migrations.RemoveField(
    model_name='responsable',
    name='usuario',
),
# DESPUÉS, eliminar usuarios huérfanos de Responsables
```

2. **Para Trabajador.email:**
```python
# Más simple, solo remover campo
migrations.RemoveField(
    model_name='trabajador',
    name='email',
),
```

### **Fase 5: Aplicar Migración**
```bash
python manage.py migrate
```

### **Fase 6: Actualizar Serializers**
- Modificar `TrabajadorSerializer`
- Modificar `ResponsableSerializer`
- Eliminar referencias a campos eliminados

### **Fase 7: Testing**
```bash
# Test crear trabajador
# Test crear responsable
# Test editar trabajador
# Test validación DNI (8 dígitos)
# Test validación documento duplicado
```

---

## 📊 CAMBIOS EN FRONTEND

### **Antes (Trabajador):**
```typescript
interface Trabajador {
  email: string;  // ❌ Campo directo
  usuario: {
    email: string;  // Mismo email
    rol: string;
  }
}
```

### **Después (Trabajador):**
```typescript
interface Trabajador {
  email: string;  // ✅ Calculado desde usuario.email (read-only)
  usuario: {
    email: string;  // Fuente única de verdad
    rol: string;
  }
}

// Al crear/editar, SOLO enviar usuario.email:
const data = {
  nombres: "Juan",
  apellidos: "Perez",
  // ❌ NO enviar: email: "juan@gmail.com",
  usuario: {
    email: "juan@gmail.com",  // ✅ Solo aquí
    rol: "Veterinario"
  }
}
```

---

### **Antes (Responsable):**
```typescript
interface Responsable {
  email: string;
  usuario: {      // ❌ Ya no existe
    email: string;
    rol: string;
  }
}
```

### **Después (Responsable):**
```typescript
interface Responsable {
  email: string;  // ✅ Un solo email (para contacto)
  // ❌ NO hay campo usuario
}

// Al crear/editar:
const data = {
  nombres: "Carlos",
  apellidos: "Rodriguez",
  email: "carlos@gmail.com",  // ✅ Un solo email
  // ❌ NO enviar campo usuario
}
```

---

## ✅ VALIDACIÓN DE DOCUMENTOS PERUANOS

### **Ejemplos de Validación:**

```python
# DNI válido
documento = "71448712"  # ✅ 8 dígitos
documento = "12345678"  # ✅ 8 dígitos
documento = "1234567"   # ❌ Solo 7 dígitos
documento = "123456789" # ❌ 9 dígitos

# Carnet de Extranjería válido
documento = "123456789"  # ✅ 9 dígitos
documento = "12345678"   # ❌ Solo 8 dígitos

# Pasaporte válido
documento = "ABC123456"   # ✅ 9 caracteres alfanuméricos
documento = "PER1234567"  # ✅ 10 caracteres
documento = "12345"       # ❌ Solo 5 caracteres

# RUC válido
documento = "20123456789"  # ✅ 11 dígitos
documento = "2012345678"   # ❌ Solo 10 dígitos
```

---

## 🎯 BENEFICIOS DE ESTA SOLUCIÓN

### ✅ **Simplicidad**
- Un solo email por modelo (no hay duplicación)
- Menos campos que sincronizar
- Menos código que mantener

### ✅ **Integridad**
- Constraints únicos a nivel de BD
- Validación específica para Perú
- Imposible crear duplicados

### ✅ **Performance**
- Menos JOINs necesarios
- Menos datos duplicados
- Queries más rápidas

### ✅ **Seguridad**
- Responsables sin acceso al sistema (no necesitan Usuario)
- Trabajadores con email único (no hay confusión)
- Validación de documentos según estándar peruano

---

## ❓ FAQ

### **P1: ¿Por qué eliminar Responsable.usuario?**
**R:** Porque el Responsable NO tiene acceso al sistema. No hace login. Solo necesita un email para contacto, no para autenticación.

### **P2: ¿Por qué eliminar Trabajador.email?**
**R:** Porque es redundante. Ya tiene `usuario.email` que se usa para login. Tener dos emails causa confusión y desincronización.

### **P3: ¿Qué pasa con Responsables existentes?**
**R:** En la migración, se copia `Usuario.email` → `Responsable.email`, luego se elimina el Usuario asociado.

### **P4: ¿Cómo sabe el frontend que cambió?**
**R:** Para Trabajador: El campo `email` sigue existiendo (read-only). Para Responsable: Ya no envía `usuario` en las requests.

### **P5: ¿DNI de 7 dígitos?**
**R:** DNI en Perú es **siempre 8 dígitos** desde 1995. Si tienes DNI antiguos de 7 dígitos, agregar validación especial.

---

## 🚀 SIGUIENTE PASO

¿Quieres que implemente estos cambios?

Confirma y procedo a:
1. ✅ Crear script de limpieza de duplicados
2. ✅ Modificar modelos
3. ✅ Crear migración personalizada
4. ✅ Actualizar serializers
5. ✅ Documentar para frontend
