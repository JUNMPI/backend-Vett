# 🔍 AUDITORÍA EXHAUSTIVA: Errores Encontrados y Corregidos

**Fecha:** 2025-10-10
**Tipo:** Testing y Corrección de Bugs
**Estado:** ✅ CORREGIDO

---

## 🐛 ERRORES CRÍTICOS ENCONTRADOS

### **Error #1: ValidationError lanza 500 en lugar de 400** 🔴 CRÍTICO

**Descripción:**
Al crear un Trabajador/Responsable con DNI inválido (ej: 7 dígitos), el sistema lanzaba error **500 Internal Server Error** en lugar de **400 Bad Request**.

**Causa Raíz:**
```python
# En api/models.py (ANTES - INCORRECTO):
class Trabajador(models.Model):
    def save(self, *args, **kwargs):
        self.full_clean()  # ← Lanza ValidationError NO capturado
        super().save(*args, **kwargs)
```

El método `full_clean()` lanza `django.core.exceptions.ValidationError` que NO es capturado por Django REST Framework, resultando en error 500.

**Impacto:**
- ❌ Mala experiencia de usuario (error 500 genérico)
- ❌ No se muestra el mensaje de validación específico
- ❌ Frontend no puede mostrar error útil

**Solución Implementada:**
```python
# En api/models.py (DESPUÉS - CORRECTO):
class Trabajador(models.Model):
    def save(self, *args, **kwargs):
        """
        Guardar modelo.
        NOTA: La validación se hace en el serializer con validate(), no aquí.
        Llamar full_clean() aquí causa errores 500 en lugar de 400.
        """
        super().save(*args, **kwargs)  # ← Sin full_clean()
```

**Validación movida al Serializer:**
```python
# En api/serializers.py:
class TrabajadorSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        documento = attrs.get('documento')
        tipodocumento = attrs.get('tipodocumento')

        if documento and tipodocumento:
            tipo = tipodocumento.nombre.upper()
            doc = documento.strip()

            # DNI: 8 dígitos exactos
            if tipo == 'DNI':
                if not re.match(r'^\d{8}$', doc):
                    raise serializers.ValidationError({
                        'documento': 'El DNI debe tener exactamente 8 dígitos.'
                    })
            # ... otros tipos

        return attrs
```

**Resultado:**
```bash
# ANTES:
POST /api/trabajadores/ con DNI inválido
→ 500 Internal Server Error (HTML de error)

# DESPUÉS:
POST /api/trabajadores/ con DNI inválido
→ 400 Bad Request
{
  "documento": ["El DNI debe tener exactamente 8 dígitos."]
}
```

---

### **Error #2: Validación de formato de documentos faltante en Responsable** ⚠️ MEDIO

**Descripción:**
`ResponsableSerializer` NO tenía validación de formato de documentos peruanos, solo validaba duplicados.

**Solución:**
Agregada la misma validación de formato que `TrabajadorSerializer`:

```python
class ResponsableSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        # ... validación de email único
        # ... validación de documento duplicado

        # ✅ AGREGADO: Validación de formato según tipo (Perú)
        tipo = tipodocumento.nombre.upper()
        doc = documento.strip()

        if tipo == 'DNI':
            if not re.match(r'^\d{8}$', doc):
                raise serializers.ValidationError({
                    'documento': 'El DNI debe tener exactamente 8 dígitos.'
                })
        # ... CE, Pasaporte, RUC
```

---

## ✅ VALIDACIONES FUNCIONANDO CORRECTAMENTE

### **Test 1: DNI válido (8 dígitos)**
```python
documento = "99999999"
tipo = "DNI"

Resultado: ✅ ACEPTADO
Status: 201 Created
```

### **Test 2: DNI inválido (7 dígitos)**
```python
documento = "1234567"  # Solo 7 dígitos
tipo = "DNI"

Resultado: ✅ RECHAZADO
Status: 400 Bad Request
Error: {"documento": ["El DNI debe tener exactamente 8 dígitos."]}
```

### **Test 3: Documento duplicado**
```python
# Crear dos trabajadores con mismo documento
documento = "99999999"

Resultado: ✅ RECHAZADO (segundo intento)
Status: 400 Bad Request
Error: {"non_field_errors": ["The fields tipodocumento, documento must make a unique set."]}
```

### **Test 4: Email duplicado**
```python
# Crear dos trabajadores con mismo email en usuario
usuario.email = "test@test.com"

Resultado: ✅ RECHAZADO (segundo intento)
Status: 400 Bad Request
Error: {"usuario": {"email": ["Este correo ya está en uso."]}}
```

---

## 🧪 TESTS EJECUTADOS

| Test # | Descripción | Estado | Resultado |
|--------|-------------|--------|-----------|
| 1 | Crear Trabajador con DNI válido (8 dígitos) | ✅ | 201 Created |
| 2 | Crear Trabajador con DNI inválido (7 dígitos) | ✅ | 400 Bad Request (correcto) |
| 3 | Crear Trabajador con documento duplicado | ✅ | 400 Bad Request (correcto) |
| 4 | Crear Trabajador con email duplicado | ✅ | 400 Bad Request (correcto) |
| 5 | Verificar que email en body es ignorado | ⚠️ | Pendiente (Unicode error) |
| 6 | Crear Responsable SIN usuario | ⏳ | Pendiente |
| 7 | Crear Responsable CON usuario (debe fallar) | ⏳ | Pendiente |
| 8 | Validación tipos de documento (CE, Pasaporte, RUC) | ⏳ | Pendiente |
| 9 | Editar Trabajador existente | ⏳ | Pendiente |
| 10 | Auditoría de datos migrados | ⏳ | Pendiente |

---

## 📊 CAMBIOS APLICADOS

### **Archivo: api/models.py**

**Cambio 1: Trabajador.save()**
```diff
  def save(self, *args, **kwargs):
-     """Ejecutar validaciones antes de guardar"""
-     self.full_clean()
+     """
+     Guardar modelo.
+     NOTA: La validación se hace en el serializer con validate(), no aquí.
+     Llamar full_clean() aquí causa errores 500 en lugar de 400.
+     """
      super().save(*args, **kwargs)
```

**Cambio 2: Responsable.save()**
```diff
  def save(self, *args, **kwargs):
-     """Ejecutar validaciones antes de guardar"""
-     self.full_clean()
+     """
+     Guardar modelo.
+     NOTA: La validación se hace en el serializer con validate(), no aquí.
+     """
      super().save(*args, **kwargs)
```

### **Archivo: api/serializers.py**

**Cambio 3: TrabajadorSerializer.validate()**
```diff
  def validate(self, attrs):
      """
-     Validación de documento duplicado
+     Validación completa: documento duplicado + formato según tipo (Perú)
      """
+     import re
      documento = attrs.get('documento')
      tipodocumento = attrs.get('tipodocumento')

      if documento and tipodocumento:
          # Verificar duplicados
          query = Trabajador.objects.filter(...)

+         # Validar formato según tipo de documento (Perú)
+         tipo = tipodocumento.nombre.upper()
+         doc = documento.strip()
+
+         # DNI: 8 dígitos exactos
+         if tipo == 'DNI':
+             if not re.match(r'^\d{8}$', doc):
+                 raise serializers.ValidationError({
+                     'documento': 'El DNI debe tener exactamente 8 dígitos.'
+                 })
+
+         # Carnet de Extranjería: 9 dígitos
+         elif tipo in ['CE', 'CARNET DE EXTRANJERIA', ...]:
+             if not re.match(r'^\d{9}$', doc):
+                 raise serializers.ValidationError({
+                     'documento': 'El Carnet de Extranjería debe tener 9 dígitos.'
+                 })
+         # ... Pasaporte, RUC

      return attrs
```

**Cambio 4: ResponsableSerializer.validate()**
```diff
  def validate(self, attrs):
      """
-     Validación de email y documento únicos
+     Validación completa: email único + documento duplicado + formato (Perú)
      """
+     import re

      # Validar email único
      email = attrs.get('email')
      if email:
          # ...

      # Validar documento duplicado
      documento = attrs.get('documento')
      tipodocumento = attrs.get('tipodocumento')

      if documento and tipodocumento:
          # Verificar duplicados
          query = Responsable.objects.filter(...)

+         # ✅ AGREGADO: Validar formato según tipo (Perú)
+         tipo = tipodocumento.nombre.upper()
+         doc = documento.strip()
+
+         # DNI: 8 dígitos exactos
+         if tipo == 'DNI':
+             if not re.match(r'^\d{8}$', doc):
+                 raise serializers.ValidationError({
+                     'documento': 'El DNI debe tener exactamente 8 dígitos.'
+                 })
+         # ... CE, Pasaporte, RUC

      return attrs
```

---

## 🎯 BENEFICIOS DE LOS CAMBIOS

### **1. Errores HTTP Correctos**
- ✅ Validaciones retornan **400 Bad Request** (no 500)
- ✅ Mensajes de error específicos y útiles
- ✅ Frontend puede mostrar errores al usuario

### **2. Validación Completa**
- ✅ DNI: 8 dígitos
- ✅ CE: 9 dígitos
- ✅ Pasaporte: 9-12 alfanumérico
- ✅ RUC: 11 dígitos
- ✅ Documentos duplicados: bloqueados
- ✅ Emails duplicados: bloqueados

### **3. Consistencia**
- ✅ Trabajador y Responsable usan la misma validación
- ✅ No hay diferencias en el comportamiento

---

## 🔄 PRÓXIMOS PASOS

### **Testing Pendiente:**
1. ⏳ Completar tests 5-10
2. ⏳ Test con Carnet de Extranjería
3. ⏳ Test con Pasaporte
4. ⏳ Test edición de Trabajador
5. ⏳ Test edición de Responsable

### **Mejoras Opcionales:**
1. 💡 Agregar validación de RUC (verificar dígito verificador)
2. 💡 Agregar validación de email real (verificar dominio exists)
3. 💡 Agregar rate limiting para prevenir spam
4. 💡 Agregar logs de auditoría para cambios críticos

---

## ✅ RESUMEN

| Aspecto | Antes | Después |
|---------|-------|---------|
| **DNI inválido** | 500 Error | 400 Bad Request ✅ |
| **Mensaje de error** | HTML genérico | JSON específico ✅ |
| **Validación formato** | Solo en modelo (no funciona) | En serializer ✅ |
| **Responsable** | Sin validación formato | Con validación ✅ |
| **Consistencia** | Desigual | Igual en ambos modelos ✅ |

---

**Errores encontrados:** 2
**Errores corregidos:** 2
**Tests pasando:** 4/10 (40%)
**Estado:** 🟡 EN PROGRESO

---

**Siguiente paso:** Completar tests restantes y documentar resultados completos.
