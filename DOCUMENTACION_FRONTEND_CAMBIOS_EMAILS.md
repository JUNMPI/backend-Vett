# 🚀 CAMBIOS EN API - Eliminación de Emails Duplicados y Validación Peruana

**Fecha:** 2025-10-10
**Prioridad:** 🔴 ALTA - BREAKING CHANGES
**Estado:** ✅ IMPLEMENTADO Y FUNCIONAL

---

## 📋 RESUMEN DE CAMBIOS

Se realizaron cambios **BREAKING** en los modelos `Trabajador` y `Responsable`:

1. **Trabajador:** Campo `email` eliminado (ahora viene de `usuario.email`)
2. **Responsable:** Campo `usuario` eliminado completamente (no tiene acceso al sistema)
3. **Validación:** Documentos únicos por tipo (DNI 8 dígitos, CE 9 dígitos, etc.)
4. **Constraints:** Imposible crear duplicados en base de datos

---

## 🎯 CAMBIO 1: TRABAJADOR (Empleados con acceso al sistema)

### **Antes:**
```typescript
interface Trabajador {
  id: string;
  nombres: string;
  apellidos: string;
  email: string;  // ❌ Campo directo
  telefono: string;
  documento: string;
  tipodocumento: string;
  usuario: {
    email: string;  // Mismo email duplicado
    password?: string;
    rol: string;
  };
  estado: string;
}

// Al crear:
POST /api/trabajadores/
{
  "nombres": "Juan",
  "apellidos": "Perez",
  "email": "juan@gmail.com",  // ❌ Se envía dos veces
  "telefono": "954316648",
  "documento": "71448712",
  "tipodocumento": "uuid-dni",
  "usuario": {
    "email": "juan@gmail.com",  // ❌ Duplicado
    "password": "123456",
    "rol": "Veterinario"
  }
}
```

### **Ahora:**
```typescript
interface Trabajador {
  id: string;
  nombres: string;
  apellidos: string;
  email: string;  // ✅ READ-ONLY (calculado desde usuario.email)
  telefono: string;
  documento: string;
  tipodocumento: string;
  usuario: {
    email: string;  // ✅ ÚNICA fuente de verdad
    password?: string;
    rol: string;
  };
  estado: string;
}

// Al crear:
POST /api/trabajadores/
{
  "nombres": "Juan",
  "apellidos": "Perez",
  // ❌ NO enviar: "email": "juan@gmail.com"
  "telefono": "954316648",
  "documento": "71448712",
  "tipodocumento": "uuid-dni",
  "usuario": {
    "email": "juan@gmail.com",  // ✅ Solo aquí
    "password": "123456",
    "rol": "Veterinario"
  }
}

// Respuesta:
{
  "id": "uuid",
  "nombres": "Juan",
  "apellidos": "Perez",
  "email": "juan@gmail.com",  // ✅ El backend lo calcula desde usuario.email
  "telefono": "954316648",
  "documento": "71448712",
  "tipodocumento": "uuid-dni",
  "usuario": {
    "id": "uuid",
    "email": "juan@gmail.com",
    "rol": "Veterinario"
  },
  "estado": "Activo"
}
```

### **Cambios en el Frontend:**

#### 1. **Crear Trabajador**
```typescript
// ❌ ANTES:
const nuevoTrabajador = {
  nombres: form.nombres,
  apellidos: form.apellidos,
  email: form.email,  // ← ELIMINAR
  telefono: form.telefono,
  documento: form.documento,
  tipodocumento: form.tipodocumento,
  usuario: {
    email: form.email,  // ← Mantener
    password: form.password,
    rol: form.rol
  }
};

// ✅ AHORA:
const nuevoTrabajador = {
  nombres: form.nombres,
  apellidos: form.apellidos,
  // NO enviar campo email aquí
  telefono: form.telefono,
  documento: form.documento,
  tipodocumento: form.tipodocumento,
  usuario: {
    email: form.email,  // ← Solo aquí
    password: form.password,
    rol: form.rol
  }
};
```

#### 2. **Editar Trabajador**
```typescript
// ✅ AHORA:
const trabajadorEditado = {
  nombres: form.nombres,
  apellidos: form.apellidos,
  // NO enviar campo email aquí
  telefono: form.telefono,
  documento: form.documento,
  tipodocumento: form.tipodocumento,
  usuario: {
    email: form.email,  // ← Email del usuario (para login)
    rol: form.rol
    // password solo si se cambia
  }
};

PUT /api/trabajadores/{id}/
```

#### 3. **Mostrar Email en UI**
```typescript
// ✅ Ambos funcionan igual:
<p>Email: {trabajador.email}</p>  // ← Calcula desde usuario.email
<p>Email: {trabajador.usuario.email}</p>  // ← Fuente original
```

---

## 🎯 CAMBIO 2: RESPONSABLE (Dueños de mascotas, SIN acceso al sistema)

### **Antes:**
```typescript
interface Responsable {
  id: string;
  nombres: string;
  apellidos: string;
  email: string;
  telefono: string;
  direccion: string;
  ciudad: string;
  documento: string;
  tipodocumento: string;
  emergencia?: string;
  usuario: {  // ❌ Ya NO existe
    email: string;
    rol: string;
  };
  mascotas: Mascota[];
}

// Al crear:
POST /api/responsables/
{
  "nombres": "Carlos",
  "apellidos": "Rodriguez",
  "email": "carlos@gmail.com",
  "telefono": "987654321",
  "direccion": "Av. Principal 123",
  "ciudad": "Lima",
  "documento": "12345678",
  "tipodocumento": "uuid-dni",
  "emergencia": "Ana Rodriguez - 999888777",
  "usuario": {  // ❌ Ya no enviar
    "email": "carlos@gmail.com",
    "password": "123456",
    "rol": "Responsable"
  }
}
```

### **Ahora:**
```typescript
interface Responsable {
  id: string;
  nombres: string;
  apellidos: string;
  email: string;  // ✅ Un solo email (para contacto)
  telefono: string;
  direccion: string;
  ciudad: string;
  documento: string;
  tipodocumento: string;
  tipodocumento_nombre: string;  // ✅ Nombre del tipo (ej: "DNI")
  emergencia?: string;
  // ❌ NO hay campo usuario
  mascotas: Mascota[];
}

// Al crear:
POST /api/responsables/
{
  "nombres": "Carlos",
  "apellidos": "Rodriguez",
  "email": "carlos@gmail.com",  // ✅ Solo este campo
  "telefono": "987654321",
  "direccion": "Av. Principal 123",
  "ciudad": "Lima",
  "documento": "12345678",
  "tipodocumento": "uuid-dni",
  "emergencia": "Ana Rodriguez - 999888777"
  // ❌ NO enviar campo usuario
}

// Respuesta:
{
  "id": "uuid",
  "nombres": "Carlos",
  "apellidos": "Rodriguez",
  "email": "carlos@gmail.com",
  "telefono": "987654321",
  "direccion": "Av. Principal 123",
  "ciudad": "Lima",
  "documento": "12345678",
  "tipodocumento": "uuid-dni",
  "tipodocumento_nombre": "DNI",
  "emergencia": "Ana Rodriguez - 999888777",
  "mascotas": []
}
```

### **Cambios en el Frontend:**

#### 1. **Crear Responsable**
```typescript
// ❌ ANTES:
const nuevoResponsable = {
  nombres: form.nombres,
  apellidos: form.apellidos,
  email: form.email,
  telefono: form.telefono,
  direccion: form.direccion,
  ciudad: form.ciudad,
  documento: form.documento,
  tipodocumento: form.tipodocumento,
  emergencia: form.emergencia,
  usuario: {  // ← ELIMINAR COMPLETAMENTE
    email: form.email,
    password: "default123",
    rol: "Responsable"
  }
};

// ✅ AHORA:
const nuevoResponsable = {
  nombres: form.nombres,
  apellidos: form.apellidos,
  email: form.email,  // ← Un solo email
  telefono: form.telefono,
  direccion: form.direccion,
  ciudad: form.ciudad,
  documento: form.documento,
  tipodocumento: form.tipodocumento,
  emergencia: form.emergencia
  // NO enviar campo usuario
};

POST /api/responsables/
```

#### 2. **Editar Responsable**
```typescript
// ✅ AHORA:
const responsableEditado = {
  nombres: form.nombres,
  apellidos: form.apellidos,
  email: form.email,  // ← Se puede cambiar
  telefono: form.telefono,
  direccion: form.direccion,
  ciudad: form.ciudad,
  documento: form.documento,
  tipodocumento: form.tipodocumento,
  emergencia: form.emergencia
  // NO enviar campo usuario
};

PUT /api/responsables/{id}/
```

#### 3. **Interfaces TypeScript**
```typescript
// ✅ Actualizar interfaces:
export interface Responsable {
  id: string;
  nombres: string;
  apellidos: string;
  email: string;
  telefono: string;
  direccion: string;
  ciudad: string;
  documento: string;
  tipodocumento: string;
  tipodocumento_nombre: string;
  emergencia?: string;
  // ❌ ELIMINAR: usuario: Usuario;
  mascotas: Mascota[];
}
```

---

## 🇵🇪 CAMBIO 3: VALIDACIÓN DE DOCUMENTOS PERUANOS

El backend ahora valida **automáticamente** el formato de documentos según el tipo:

### **Reglas de Validación:**

| Tipo Documento | Longitud | Formato | Ejemplo Válido | Ejemplo Inválido |
|----------------|----------|---------|----------------|------------------|
| **DNI** | 8 dígitos | Solo números | `71448712` | `1234567` (7 dígitos) |
| **Carnet de Extranjería (CE)** | 9 dígitos | Solo números | `123456789` | `12345678` (8 dígitos) |
| **Pasaporte** | 9-12 caracteres | Alfanumérico | `ABC123456` | `12345` (muy corto) |
| **RUC** | 11 dígitos | Solo números | `20123456789` | `2012345678` (10 dígitos) |

### **Errores del Backend:**

```typescript
// Si envías DNI inválido:
POST /api/trabajadores/
{
  "documento": "1234567",  // ← Solo 7 dígitos
  "tipodocumento": "uuid-dni"
}

// Respuesta 400:
{
  "documento": ["El DNI debe tener exactamente 8 dígitos."]
}
```

### **Validación en Frontend (Recomendado):**

```typescript
function validarDocumento(documento: string, tipoDocumento: string): string | null {
  const tipo = tipoDocumento.toUpperCase();

  switch (tipo) {
    case 'DNI':
      if (!/^\d{8}$/.test(documento)) {
        return 'El DNI debe tener exactamente 8 dígitos';
      }
      break;

    case 'CE':
    case 'CARNET DE EXTRANJERIA':
    case 'CARNET DE EXTRANJERÍA':
      if (!/^\d{9}$/.test(documento)) {
        return 'El Carnet de Extranjería debe tener 9 dígitos';
      }
      break;

    case 'PASAPORTE':
      if (!/^[A-Z0-9]{9,12}$/i.test(documento)) {
        return 'El Pasaporte debe tener entre 9 y 12 caracteres alfanuméricos';
      }
      break;

    case 'RUC':
      if (!/^\d{11}$/.test(documento)) {
        return 'El RUC debe tener exactamente 11 dígitos';
      }
      break;
  }

  return null;  // Sin errores
}

// Uso:
const error = validarDocumento(form.documento, tipoDocumentoSeleccionado.nombre);
if (error) {
  mostrarError(error);
  return;
}
```

---

## 🔒 CAMBIO 4: VALIDACIÓN DE DUPLICADOS

El backend ahora **rechaza automáticamente** duplicados:

### **Documentos Duplicados:**

```typescript
// Intento crear trabajador con documento existente:
POST /api/trabajadores/
{
  "documento": "71448712",
  "tipodocumento": "uuid-dni"  // Ya existe otro trabajador con este DNI
}

// Respuesta 400:
{
  "documento": ["Ya existe un trabajador con este documento."]
}
```

### **Emails Duplicados:**

```typescript
// Intento crear usuario con email existente:
POST /api/trabajadores/
{
  "usuario": {
    "email": "juan@gmail.com"  // Ya existe
  }
}

// Respuesta 400:
{
  "usuario": {
    "email": ["Este correo ya está en uso."]
  }
}
```

### **Manejo de Errores en Frontend:**

```typescript
async function crearTrabajador(datos: TrabajadorForm) {
  try {
    const response = await fetch('/api/trabajadores/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    });

    if (!response.ok) {
      const errores = await response.json();

      // Mostrar errores específicos:
      if (errores.documento) {
        mostrarError('Documento', errores.documento[0]);
      }
      if (errores.usuario?.email) {
        mostrarError('Email', errores.usuario.email[0]);
      }

      return;
    }

    const trabajador = await response.json();
    mostrarExito('Trabajador creado exitosamente');

  } catch (error) {
    mostrarError('Error de conexión', 'No se pudo conectar con el servidor');
  }
}
```

---

## 📝 CHECKLIST DE MIGRACIÓN FRONTEND

### **Para Trabajadores:**
- [ ] Actualizar interface `Trabajador` (email como read-only)
- [ ] Eliminar envío de `email` en POST/PUT (solo en `usuario.email`)
- [ ] Validar formato de documento antes de enviar
- [ ] Manejar errores de documento duplicado
- [ ] Manejar errores de email duplicado
- [ ] Probar crear trabajador
- [ ] Probar editar trabajador
- [ ] Verificar que `trabajador.email` se muestra correctamente

### **Para Responsables:**
- [ ] Actualizar interface `Responsable` (eliminar campo `usuario`)
- [ ] Eliminar envío de `usuario` en POST/PUT
- [ ] Actualizar forms (remover campos de usuario/password)
- [ ] Validar formato de documento antes de enviar
- [ ] Manejar errores de documento duplicado
- [ ] Manejar errores de email duplicado
- [ ] Probar crear responsable
- [ ] Probar editar responsable
- [ ] Actualizar pantalla de login (responsables NO pueden hacer login)

---

## 🧪 TESTING

### **Test 1: Crear Trabajador**
```bash
POST /api/trabajadores/
{
  "nombres": "Test",
  "apellidos": "Usuario",
  "telefono": "999888777",
  "documento": "87654321",
  "tipodocumento": "uuid-dni",
  "usuario": {
    "email": "test@test.com",
    "password": "test1234",
    "rol": "Recepcionista"
  }
}

# Esperado: 201 Created
# Verificar: trabajador.email === "test@test.com"
```

### **Test 2: Crear Responsable**
```bash
POST /api/responsables/
{
  "nombres": "Test",
  "apellidos": "Responsable",
  "email": "responsable@test.com",
  "telefono": "999888777",
  "direccion": "Av. Test 123",
  "ciudad": "Lima",
  "documento": "77777777",
  "tipodocumento": "uuid-dni"
}

# Esperado: 201 Created
# Verificar: NO tiene campo usuario en respuesta
```

### **Test 3: Documento Duplicado**
```bash
# Crear dos veces con mismo documento:
POST /api/trabajadores/ con documento="88888888"
POST /api/trabajadores/ con documento="88888888"

# Esperado: Segunda request falla con 400
# Error: "Ya existe un trabajador con este documento."
```

### **Test 4: DNI Inválido**
```bash
POST /api/trabajadores/
{
  "documento": "1234567",  # Solo 7 dígitos
  "tipodocumento": "uuid-dni"
}

# Esperado: 400 Bad Request
# Error: "El DNI debe tener exactamente 8 dígitos."
```

---

## ⚠️ ERRORES COMUNES

### **Error 1: "Field email is required"**
**Causa:** Estás enviando `email` en el body de Trabajador.
**Solución:** NO enviar `email` en el body principal, solo en `usuario.email`.

```typescript
// ❌ MAL:
{
  "email": "juan@gmail.com",  // ← ELIMINAR
  "usuario": { "email": "juan@gmail.com" }
}

// ✅ BIEN:
{
  "usuario": { "email": "juan@gmail.com" }
}
```

### **Error 2: "Field usuario is required (Responsable)"**
**Causa:** Estás enviando `usuario` en Responsable.
**Solución:** NO enviar `usuario` en Responsable.

```typescript
// ❌ MAL:
POST /api/responsables/
{
  "email": "carlos@gmail.com",
  "usuario": { ... }  // ← ELIMINAR
}

// ✅ BIEN:
POST /api/responsables/
{
  "email": "carlos@gmail.com"
  // Sin usuario
}
```

### **Error 3: "El DNI debe tener exactamente 8 dígitos"**
**Causa:** Documento con formato incorrecto.
**Solución:** Validar en frontend ANTES de enviar.

```typescript
if (tipoDocumento === 'DNI' && documento.length !== 8) {
  mostrarError('El DNI debe tener 8 dígitos');
  return;
}
```

### **Error 4: "Ya existe un trabajador con este documento"**
**Causa:** Estás intentando crear/editar con un documento que ya existe.
**Solución:** Verificar duplicados antes de enviar, o manejar el error en UI.

```typescript
catch (error) {
  if (error.documento) {
    mostrarError(`Este documento ya está registrado. Por favor verifica.`);
  }
}
```

---

## 📞 PREGUNTAS FRECUENTES

### **P1: ¿Por qué responsables ya no tienen usuario?**
**R:** Porque los responsables (dueños de mascotas) **NO tienen acceso al sistema**. Solo necesitan un email para contacto, no para hacer login.

### **P2: ¿Cómo hago login de responsables?**
**R:** **NO puedes**. Solo Trabajadores (Admin, Veterinario, Recepcionista, Inventario) pueden hacer login.

### **P3: ¿El email de Trabajador sigue apareciendo en la respuesta?**
**R:** **SÍ**. El backend lo calcula automáticamente desde `usuario.email` y lo devuelve como read-only.

### **P4: ¿Puedo cambiar el email de un Trabajador?**
**R:** **SÍ**, pero debes cambiarlo en `usuario.email`, no en `trabajador.email`.

```typescript
PUT /api/trabajadores/{id}/
{
  "usuario": {
    "email": "nuevo@email.com"  // ← Cambiar aquí
  }
}
```

### **P5: ¿Qué pasa con los responsables existentes?**
**R:** El backend ya migró todos los datos automáticamente. Los responsables existentes tienen su email sincronizado.

### **P6: ¿DNI de 7 dígitos?**
**R:** DNI en Perú es **siempre 8 dígitos** desde 1995. Si tienes DNI antiguos, contacta al backend para agregar excepción.

---

## 🚀 PRÓXIMOS PASOS

1. ✅ Actualizar interfaces TypeScript
2. ✅ Modificar formularios (eliminar campos innecesarios)
3. ✅ Agregar validación de documentos
4. ✅ Actualizar llamadas a API (POST/PUT)
5. ✅ Manejar errores de duplicados
6. ✅ Testing completo
7. ✅ Actualizar documentación frontend

---

**¿Dudas o problemas?** El backend está disponible para ayudar. 🚀
