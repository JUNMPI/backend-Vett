# 📋 PROMPT ACTUALIZADO PARA FRONTEND - Gestión de Trabajadores y Horarios

## 🎯 Contexto General

El **backend Django** del sistema **Veterinaria Huellitas** ha sido actualizado con **mejoras críticas** en la gestión de trabajadores, específicamente en el sistema de horarios de trabajo para veterinarios. Este documento detalla las **nuevas funcionalidades** que debes implementar en el frontend Angular para integrarse correctamente con el sistema de citas.

---

## 🆕 CAMBIOS IMPORTANTES DEL BACKEND

### **1. Sistema de Horarios de Trabajo Avanzado**

El backend ya **NO usa solo días de la semana simples**. Ahora utiliza el modelo **`HorarioTrabajo`** que incluye:

✅ **Horas específicas de trabajo** (hora_inicio, hora_fin)
✅ **Horarios de descanso/almuerzo** (hora_inicio_descanso, hora_fin_descanso)
✅ **Configuración por día de la semana** (0=Lunes, 6=Domingo)
✅ **Control de actividad** (horarios activos/inactivos)
✅ **Vigencia temporal** (fecha_inicio_vigencia, fecha_fin_vigencia)

### **2. Validación Automática de Citas**

El backend ahora **valida automáticamente** que:
- Las citas solo se creen en días laborables del veterinario
- Las citas estén dentro del horario de trabajo (hora_inicio - hora_fin)
- Las citas **NO se agenden en horario de descanso** (ej: almuerzo 13:00-14:00)
- No se permitan citas duplicadas (mismo vet, misma fecha/hora)

---

## 🏗️ Nueva Arquitectura de Modelos

### **Interface HorarioTrabajo (NUEVO)**

```typescript
export interface HorarioTrabajo {
  id?: string;                        // UUID
  veterinario: string;                // UUID del veterinario
  dia_semana: number;                 // 0=Lunes, 1=Martes, ..., 6=Domingo
  dia_semana_nombre?: string;         // "Lunes", "Martes", etc. (calculado)
  hora_inicio: string;                // "08:00:00"
  hora_fin: string;                   // "18:00:00"
  tiene_descanso: boolean;            // Si tiene descanso (ej: almuerzo)
  hora_inicio_descanso?: string;      // "13:00:00"
  hora_fin_descanso?: string;         // "14:00:00"
  activo: boolean;                    // Si está actualmente activo
  fecha_inicio_vigencia?: string;     // "2025-01-01" (opcional)
  fecha_fin_vigencia?: string;        // "2025-12-31" (opcional)
}
```

### **Interface Trabajador (ACTUALIZADA)**

```typescript
export interface Trabajador {
  id?: string;
  nombres: string;
  apellidos: string;
  email: string;
  telefono: string;
  tipodocumento: string | null;
  tipodocumento_nombre?: string;
  documento: string;
  usuario: Usuario;
  estado: string;                 // "Activo" | "Inactivo"
}
```

### **Interface Veterinario (ACTUALIZADA)**

```typescript
export interface Veterinario {
  id: string;
  trabajador: string;                   // UUID del trabajador
  especialidad: string;                 // UUID de la especialidad
  nombreEspecialidad?: string;          // Nombre de la especialidad (read-only)

  // ⚠️ DEPRECADO - Mantener por compatibilidad pero NO usar
  dias_trabajo?: DiaTrabajo[];

  // 🆕 NUEVO - Usar este campo (read-only, generado automáticamente por backend)
  horarios_trabajo?: HorarioTrabajo[];  // Array de horarios detallados

  // 🆕 NUEVOS - Detalles completos (read-only, generados automáticamente por backend)
  trabajador_detalle?: {
    id: string;
    nombres: string;
    apellidos: string;
    email: string;
    telefono: string;
    documento: string;
    estado: string;
  };

  especialidad_detalle?: {
    id: string;
    nombre: string;
    estado: string;
  };
}
```

---

## 🔌 Endpoints Actualizados

### **BASE URL**
`http://127.0.0.1:8000/api/`

---

### **1. HORARIOS DE TRABAJO - Nuevos Endpoints**

#### **Listar Horarios de un Veterinario**
```http
GET /api/horarios-trabajo/?veterinario={veterinario_id}
```

**Response:**
```json
[
  {
    "id": "uuid-horario-1",
    "veterinario": "uuid-veterinario",
    "dia_semana": 0,
    "dia_semana_nombre": "Lunes",
    "hora_inicio": "08:00:00",
    "hora_fin": "18:00:00",
    "tiene_descanso": true,
    "hora_inicio_descanso": "13:00:00",
    "hora_fin_descanso": "14:00:00",
    "activo": true,
    "fecha_inicio_vigencia": null,
    "fecha_fin_vigencia": null
  },
  {
    "id": "uuid-horario-2",
    "veterinario": "uuid-veterinario",
    "dia_semana": 1,
    "dia_semana_nombre": "Martes",
    "hora_inicio": "08:00:00",
    "hora_fin": "18:00:00",
    "tiene_descanso": true,
    "hora_inicio_descanso": "13:00:00",
    "hora_fin_descanso": "14:00:00",
    "activo": true,
    "fecha_inicio_vigencia": null,
    "fecha_fin_vigencia": null
  }
]
```

#### **Crear Horario de Trabajo**
```http
POST /api/horarios-trabajo/
```

**Body:**
```json
{
  "veterinario": "uuid-veterinario",
  "dia_semana": 0,
  "hora_inicio": "08:00:00",
  "hora_fin": "18:00:00",
  "tiene_descanso": true,
  "hora_inicio_descanso": "13:00:00",
  "hora_fin_descanso": "14:00:00",
  "activo": true
}
```

#### **Actualizar Horario de Trabajo**
```http
PUT /api/horarios-trabajo/{id}/
PATCH /api/horarios-trabajo/{id}/
```

#### **Eliminar Horario de Trabajo**
```http
DELETE /api/horarios-trabajo/{id}/
```

#### **Activar/Desactivar Horario**
```http
PATCH /api/horarios-trabajo/{id}/activar/
PATCH /api/horarios-trabajo/{id}/desactivar/
```

---

### **2. VETERINARIOS - Endpoints Actualizados**

#### **Obtener Veterinario con Horarios**
```http
GET /api/veterinarios/{id}/
```

**Response (ACTUALIZADO CON NUEVOS CAMPOS):**
```json
{
  "id": "uuid-veterinario",
  "trabajador": "uuid-trabajador",
  "especialidad": "uuid-especialidad",
  "nombreEspecialidad": "Medicina General",

  "trabajador_detalle": {
    "id": "uuid-trabajador",
    "nombres": "Carlos Alberto",
    "apellidos": "Ramirez Perez",
    "email": "vet@huellitas.com",
    "telefono": "987654321",
    "documento": "12345678",
    "estado": "Activo"
  },

  "especialidad_detalle": {
    "id": "uuid-especialidad",
    "nombre": "Medicina General",
    "estado": "Activo"
  },

  "dias_trabajo": [
    {"dia": "LUNES"},
    {"dia": "MARTES"}
  ],

  "horarios_trabajo": [
    {
      "id": "uuid-horario-1",
      "veterinario": "uuid-veterinario",
      "veterinario_nombre": "Carlos Alberto Ramirez Perez - Medicina General",
      "dia_semana": 0,
      "dia_display": "Lunes",
      "hora_inicio": "08:00:00",
      "hora_fin": "18:00:00",
      "hora_inicio_descanso": "13:00:00",
      "hora_fin_descanso": "14:00:00",
      "duracion_jornada": 9.0,
      "activo": true
    },
    {
      "id": "uuid-horario-2",
      "veterinario": "uuid-veterinario",
      "veterinario_nombre": "Carlos Alberto Ramirez Perez - Medicina General",
      "dia_semana": 1,
      "dia_display": "Martes",
      "hora_inicio": "08:00:00",
      "hora_fin": "18:00:00",
      "hora_inicio_descanso": "13:00:00",
      "hora_fin_descanso": "14:00:00",
      "duracion_jornada": 9.0,
      "activo": true
    }
  ]
}
```

**⚠️ IMPORTANTE:** El backend ahora retorna **AMBOS campos**:
- `dias_trabajo`: Sistema antiguo (solo días) - **DEPRECADO**
- `horarios_trabajo`: Sistema nuevo (días + horas + descansos) - **USAR ESTE**

---

### **3. TRABAJADORES - Endpoints sin cambios estructurales**

Los endpoints de trabajadores siguen funcionando igual, pero ahora:

- El campo `estado` ya existe en el backend
- Los endpoints `/desactivar/` y `/activar/` ya están implementados
- La validación de email y documento único funciona correctamente

---

## 🎨 Nuevas Funcionalidades a Implementar en el Frontend

### **1. Gestión de Horarios de Trabajo en Formulario de Veterinario**

#### **Componente: crear-trabajador.component.ts / editar-trabajador.component.ts**

**Reemplazar el actual selector de días simples por:**

```typescript
// ANTIGUO (YA NO USAR)
<div *ngFor="let dia of diasSemana">
  <input type="checkbox" [(ngModel)]="dia.seleccionado">
  {{ dia.nombre }}
</div>

// NUEVO (IMPLEMENTAR)
<div class="horarios-trabajo-section">
  <h3>Configuración de Horarios de Trabajo</h3>

  <div *ngFor="let dia of diasSemana; let i = index" class="dia-horario">
    <div class="dia-header">
      <input
        type="checkbox"
        [(ngModel)]="dia.trabaja"
        (change)="toggleDia(i)">
      <label>{{ dia.nombre }}</label>
    </div>

    <!-- Mostrar solo si el día está seleccionado -->
    <div *ngIf="dia.trabaja" class="horario-config">
      <div class="row">
        <div class="col-md-6">
          <label>Hora Inicio</label>
          <input
            type="time"
            [(ngModel)]="dia.hora_inicio"
            required>
        </div>
        <div class="col-md-6">
          <label>Hora Fin</label>
          <input
            type="time"
            [(ngModel)]="dia.hora_fin"
            required>
        </div>
      </div>

      <div class="descanso-section">
        <input
          type="checkbox"
          [(ngModel)]="dia.tiene_descanso">
        <label>Tiene descanso/almuerzo</label>

        <div *ngIf="dia.tiene_descanso" class="row">
          <div class="col-md-6">
            <label>Inicio Descanso</label>
            <input
              type="time"
              [(ngModel)]="dia.hora_inicio_descanso">
          </div>
          <div class="col-md-6">
            <label>Fin Descanso</label>
            <input
              type="time"
              [(ngModel)]="dia.hora_fin_descanso">
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

**Modelo de datos en el componente:**

```typescript
diasSemana = [
  {
    numero: 0,
    nombre: 'Lunes',
    trabaja: false,
    hora_inicio: '08:00',
    hora_fin: '18:00',
    tiene_descanso: false,
    hora_inicio_descanso: '13:00',
    hora_fin_descanso: '14:00'
  },
  {
    numero: 1,
    nombre: 'Martes',
    trabaja: false,
    hora_inicio: '08:00',
    hora_fin: '18:00',
    tiene_descanso: false,
    hora_inicio_descanso: '13:00',
    hora_fin_descanso: '14:00'
  },
  // ... resto de días
];
```

---

### **2. Servicio Actualizado: trabajadores.service.ts**

```typescript
// NUEVO MÉTODO - Crear horarios de trabajo
crearHorariosTrabajo(veterinarioId: string, horarios: HorarioTrabajo[]): Observable<HorarioTrabajo[]> {
  const requests = horarios.map(horario =>
    this.http.post<HorarioTrabajo>(`${this.apiUrl}/horarios-trabajo/`, {
      veterinario: veterinarioId,
      dia_semana: horario.dia_semana,
      hora_inicio: horario.hora_inicio,
      hora_fin: horario.hora_fin,
      tiene_descanso: horario.tiene_descanso,
      hora_inicio_descanso: horario.hora_inicio_descanso,
      hora_fin_descanso: horario.hora_fin_descanso,
      activo: true
    })
  );

  return forkJoin(requests);
}

// NUEVO MÉTODO - Actualizar horarios de trabajo
actualizarHorariosTrabajo(
  veterinarioId: string,
  horariosNuevos: HorarioTrabajo[]
): Observable<any> {
  // 1. Obtener horarios actuales
  return this.http.get<HorarioTrabajo[]>(
    `${this.apiUrl}/horarios-trabajo/?veterinario=${veterinarioId}`
  ).pipe(
    switchMap(horariosActuales => {
      // 2. Eliminar horarios antiguos
      const deleteRequests = horariosActuales.map(h =>
        this.http.delete(`${this.apiUrl}/horarios-trabajo/${h.id}/`)
      );

      // 3. Crear nuevos horarios
      return forkJoin(deleteRequests).pipe(
        switchMap(() => this.crearHorariosTrabajo(veterinarioId, horariosNuevos))
      );
    })
  );
}

// ACTUALIZAR MÉTODO createTrabajador
createTrabajador(
  trabajador: Trabajador,
  esVeterinario: boolean,
  especialidad?: string,
  horariosTrabajoConfig?: any[]  // Nuevo parámetro
): Observable<any> {
  return this.http.post<Trabajador>(`${this.apiUrl}/trabajadores/`, trabajador).pipe(
    switchMap(trabajadorCreado => {
      if (!esVeterinario) {
        return of(trabajadorCreado);
      }

      // Crear registro de veterinario
      return this.http.post<Veterinario>(`${this.apiUrl}/veterinarios/`, {
        trabajador: trabajadorCreado.id,
        especialidad: especialidad
      }).pipe(
        switchMap(veterinarioCreado => {
          // Crear horarios de trabajo
          const horarios: HorarioTrabajo[] = horariosTrabajoConfig!
            .filter(dia => dia.trabaja)
            .map(dia => ({
              veterinario: veterinarioCreado.id!,
              dia_semana: dia.numero,
              hora_inicio: dia.hora_inicio + ':00',
              hora_fin: dia.hora_fin + ':00',
              tiene_descanso: dia.tiene_descanso,
              hora_inicio_descanso: dia.tiene_descanso ? dia.hora_inicio_descanso + ':00' : undefined,
              hora_fin_descanso: dia.tiene_descanso ? dia.hora_fin_descanso + ':00' : undefined,
              activo: true
            }));

          return this.crearHorariosTrabajo(veterinarioCreado.id!, horarios).pipe(
            map(() => trabajadorCreado)
          );
        })
      );
    })
  );
}
```

---

### **3. Visualización de Horarios en el Listado**

#### **Componente: trabajadores.component.html**

**Agregar en el modal de detalle del trabajador:**

```html
<div *ngIf="trabajadorSeleccionado.usuario?.rol === 'Veterinario'" class="horarios-section">
  <h5>📅 Horarios de Trabajo</h5>

  <div *ngIf="horariosVeterinario && horariosVeterinario.length > 0; else sinHorarios">
    <div *ngFor="let horario of horariosVeterinario" class="horario-item">
      <div class="dia-nombre">
        <strong>{{ horario.dia_semana_nombre }}</strong>
        <span class="badge" [class.bg-success]="horario.activo" [class.bg-secondary]="!horario.activo">
          {{ horario.activo ? 'Activo' : 'Inactivo' }}
        </span>
      </div>

      <div class="horario-detalle">
        <span class="horario-rango">
          🕐 {{ horario.hora_inicio | slice:0:5 }} - {{ horario.hora_fin | slice:0:5 }}
        </span>

        <span *ngIf="horario.tiene_descanso" class="descanso">
          ☕ Descanso: {{ horario.hora_inicio_descanso | slice:0:5 }} - {{ horario.hora_fin_descanso | slice:0:5 }}
        </span>
      </div>
    </div>
  </div>

  <ng-template #sinHorarios>
    <p class="text-muted">⚠️ Este veterinario no tiene horarios configurados</p>
  </ng-template>
</div>
```

**Cargar horarios en el componente:**

```typescript
verDetalle(trabajador: Trabajador): void {
  this.trabajadorSeleccionado = trabajador;

  // Si es veterinario, cargar horarios
  if (trabajador.usuario?.rol === 'Veterinario') {
    this.veterinariosService.obtenerPorTrabajador(trabajador.id!).subscribe({
      next: (veterinario) => {
        this.horariosVeterinario = veterinario.horarios_trabajo || [];
      }
    });
  }

  // Mostrar modal
}
```

---

## ⚠️ VALIDACIONES IMPORTANTES

### **Validaciones del Backend (Ya implementadas)**

✅ **No permitir citas fuera del horario de trabajo**
✅ **No permitir citas en horario de descanso**
✅ **No permitir citas en días no laborables**
✅ **No permitir citas duplicadas (mismo vet, fecha, hora)**
✅ **Validar formato de horas (HH:MM:SS)**

### **Validaciones a implementar en el Frontend**

1. **Hora fin > Hora inicio**
   ```typescript
   if (dia.hora_fin <= dia.hora_inicio) {
     alert('La hora de fin debe ser mayor a la hora de inicio');
     return false;
   }
   ```

2. **Descanso dentro del horario laboral**
   ```typescript
   if (dia.tiene_descanso) {
     if (dia.hora_inicio_descanso < dia.hora_inicio ||
         dia.hora_fin_descanso > dia.hora_fin) {
       alert('El descanso debe estar dentro del horario de trabajo');
       return false;
     }
   }
   ```

3. **Al menos un día laborable**
   ```typescript
   const diasTrabajo = this.diasSemana.filter(d => d.trabaja);
   if (diasTrabajo.length === 0) {
     alert('Debe seleccionar al menos un día de trabajo');
     return false;
   }
   ```

4. **Horarios configurados al crear veterinario**
   ```typescript
   if (esVeterinario && !this.tieneHorariosConfigurados()) {
     alert('Debe configurar los horarios de trabajo del veterinario');
     return false;
   }
   ```

---

## 🎯 Flujo Completo: Crear Veterinario

### **Paso 1: Usuario llena el formulario**
- Nombres, apellidos, email, documento, etc.
- Selecciona rol: **Veterinario**
- Selecciona especialidad

### **Paso 2: Configurar horarios de trabajo**
- Marca los días que trabaja (ej: Lunes a Viernes)
- Para cada día:
  - Define hora inicio (ej: 08:00)
  - Define hora fin (ej: 18:00)
  - Opcionalmente marca "Tiene descanso"
  - Si tiene descanso: define horario de descanso (ej: 13:00 - 14:00)

### **Paso 3: Frontend envía peticiones al backend**
```typescript
guardar() {
  // 1. Crear trabajador
  this.trabajadoresService.createTrabajador(
    trabajadorData,
    true,  // esVeterinario
    especialidadId,
    this.diasSemana  // Configuración de horarios
  ).subscribe({
    next: () => {
      this.router.navigate(['/trabajadores'], {
        state: { mensaje: '✅ Veterinario creado con horarios configurados' }
      });
    },
    error: (error) => {
      console.error('Error:', error);
      if (error.error?.hora) {
        alert(`Error de validación: ${error.error.hora}`);
      }
    }
  });
}
```

---

## 🔄 Migración de Datos Existentes

### **Para Veterinarios Ya Creados**

Si ya tienes veterinarios en el sistema creados con el antiguo sistema de `DiaTrabajo`, necesitas:

1. **Crear horarios por defecto**:
   - Lunes a Viernes: 08:00 - 18:00 (descanso 13:00 - 14:00)
   - Sábado: 09:00 - 13:00 (sin descanso)
   - Domingo: No trabaja

2. **Script de migración** (ejecutar en backend):
   ```python
   # crear_horarios_desde_dias.py
   from api.models import Veterinario, DiaTrabajo, HorarioTrabajo

   MAPEO_DIAS = {
       'LUNES': 0, 'MARTES': 1, 'MIERCOLES': 2,
       'JUEVES': 3, 'VIERNES': 4, 'SABADO': 5, 'DOMINGO': 6
   }

   for vet in Veterinario.objects.all():
       for dia_trabajo in vet.dias_trabajo.all():
           dia_num = MAPEO_DIAS[dia_trabajo.dia]

           # Horario por defecto
           hora_inicio = '08:00' if dia_num < 5 else '09:00'
           hora_fin = '18:00' if dia_num < 5 else '13:00'
           tiene_descanso = dia_num < 5

           HorarioTrabajo.objects.get_or_create(
               veterinario=vet,
               dia_semana=dia_num,
               defaults={
                   'hora_inicio': hora_inicio,
                   'hora_fin': hora_fin,
                   'tiene_descanso': tiene_descanso,
                   'hora_inicio_descanso': '13:00' if tiene_descanso else None,
                   'hora_fin_descanso': '14:00' if tiene_descanso else None,
                   'activo': True
               }
           )
   ```

---

## 📊 Resumen de Cambios Críticos

| Componente | Antes | Ahora |
|------------|-------|-------|
| **Días de trabajo** | Solo nombre del día (LUNES, MARTES) | Horarios completos con horas específicas |
| **Modelo veterinario** | `dias_trabajo: DiaTrabajo[]` | `horarios_trabajo: HorarioTrabajo[]` |
| **Formulario** | Checkboxes simples de días | Configuración completa de horarios por día |
| **Validación citas** | Solo validaba día laborable | Valida día + hora + descanso |
| **Endpoint principal** | `POST /api/veterinarios/{id}/asignar-dias/` | `POST /api/horarios-trabajo/` |

---

## 🐛 Problemas Comunes a Evitar

### **1. Formato de Horas**
❌ **Incorrecto**: `"8:00"`, `"08:00"`, `"8:0:0"`
✅ **Correcto**: `"08:00:00"`

**Solución en frontend:**
```typescript
formatearHora(hora: string): string {
  // Si viene "08:00", convertir a "08:00:00"
  if (hora.split(':').length === 2) {
    return hora + ':00';
  }
  return hora;
}
```

### **2. Día de la Semana**
❌ **Incorrecto**: Enviar `"LUNES"`, `"Lunes"`, `1`
✅ **Correcto**: Enviar número `0` (Lunes) a `6` (Domingo)

### **3. Validación de Citas**
El backend ahora devuelve errores específicos:

```json
{
  "hora": "La hora 13:30:00 está en el horario de descanso (13:00:00 - 14:00:00).",
  "error_code": "FUERA_DE_HORARIO"
}
```

**Manejar en el frontend:**
```typescript
crearCita(cita: Cita): void {
  this.citasService.create(cita).subscribe({
    next: () => { /* éxito */ },
    error: (error) => {
      if (error.error?.error_code === 'FUERA_DE_HORARIO') {
        alert(`⚠️ ${error.error.hora}`);
      } else {
        alert('Error al crear la cita');
      }
    }
  });
}
```

---

## 📞 Endpoints Completos de Referencia

### **Trabajadores**
- `GET /api/trabajadores/` - Listar todos
- `GET /api/trabajadores/activos/` - Solo activos
- `GET /api/trabajadores/{id}/` - Obtener por ID
- `POST /api/trabajadores/` - Crear
- `PUT /api/trabajadores/{id}/` - Actualizar
- `PATCH /api/trabajadores/{id}/desactivar/` - Desactivar
- `PATCH /api/trabajadores/{id}/activar/` - Activar
- `PUT /api/trabajadores/{id}/reset-password/` - Resetear contraseña

### **Veterinarios**
- `GET /api/veterinarios/` - Listar todos
- `GET /api/veterinarios/{id}/` - Obtener por ID (incluye horarios_trabajo)
- `GET /api/veterinarios/por-trabajador/{trabajador_id}/` - Por trabajador
- `POST /api/veterinarios/` - Crear
- `PATCH /api/veterinarios/{id}/` - Actualizar

### **Horarios de Trabajo (NUEVO)**
- `GET /api/horarios-trabajo/` - Listar todos
- `GET /api/horarios-trabajo/?veterinario={id}` - Por veterinario
- `GET /api/horarios-trabajo/{id}/` - Obtener por ID
- `POST /api/horarios-trabajo/` - Crear
- `PUT /api/horarios-trabajo/{id}/` - Actualizar completo
- `PATCH /api/horarios-trabajo/{id}/` - Actualizar parcial
- `DELETE /api/horarios-trabajo/{id}/` - Eliminar
- `PATCH /api/horarios-trabajo/{id}/activar/` - Activar
- `PATCH /api/horarios-trabajo/{id}/desactivar/` - Desactivar

---

## ✅ Checklist de Implementación

### **Backend (Ya completado ✅)**
- [x] Modelo `HorarioTrabajo` creado
- [x] Validación de horarios en modelo `Cita`
- [x] Endpoints CRUD de horarios-trabajo
- [x] Validación de citas duplicadas (UniqueConstraint)
- [x] Campo `estado` en modelo Trabajador
- [x] Endpoints activar/desactivar trabajador

### **Frontend (Pendiente - Tu tarea 🎯)**
- [ ] Crear interface `HorarioTrabajo`
- [ ] Actualizar interface `Veterinario` (agregar `horarios_trabajo`)
- [ ] Actualizar servicio `trabajadores.service.ts` (métodos horarios)
- [ ] Modificar formulario crear-trabajador (configuración horarios)
- [ ] Modificar formulario editar-trabajador (editar horarios)
- [ ] Actualizar modal de detalle (mostrar horarios)
- [ ] Implementar validaciones de horarios en frontend
- [ ] Manejar errores de validación del backend
- [ ] Migrar datos existentes (script o manual)
- [ ] Actualizar filtros (opcional: filtrar por disponibilidad)

---

## 🎓 Ejemplo Completo de Integración

```typescript
// crear-trabajador.component.ts
export class CrearTrabajadorComponent {
  diasSemana = [
    { numero: 0, nombre: 'Lunes', trabaja: true, hora_inicio: '08:00', hora_fin: '18:00', tiene_descanso: true, hora_inicio_descanso: '13:00', hora_fin_descanso: '14:00' },
    { numero: 1, nombre: 'Martes', trabaja: true, hora_inicio: '08:00', hora_fin: '18:00', tiene_descanso: true, hora_inicio_descanso: '13:00', hora_fin_descanso: '14:00' },
    { numero: 2, nombre: 'Miércoles', trabaja: true, hora_inicio: '08:00', hora_fin: '18:00', tiene_descanso: true, hora_inicio_descanso: '13:00', hora_fin_descanso: '14:00' },
    { numero: 3, nombre: 'Jueves', trabaja: true, hora_inicio: '08:00', hora_fin: '18:00', tiene_descanso: true, hora_inicio_descanso: '13:00', hora_fin_descanso: '14:00' },
    { numero: 4, nombre: 'Viernes', trabaja: true, hora_inicio: '08:00', hora_fin: '18:00', tiene_descanso: true, hora_inicio_descanso: '13:00', hora_fin_descanso: '14:00' },
    { numero: 5, nombre: 'Sábado', trabaja: true, hora_inicio: '09:00', hora_fin: '13:00', tiene_descanso: false, hora_inicio_descanso: '', hora_fin_descanso: '' },
    { numero: 6, nombre: 'Domingo', trabaja: false, hora_inicio: '08:00', hora_fin: '18:00', tiene_descanso: false, hora_inicio_descanso: '', hora_fin_descanso: '' }
  ];

  guardar() {
    const trabajador = {
      nombres: this.formulario.value.nombres,
      apellidos: this.formulario.value.apellidos,
      email: this.formulario.value.email,
      telefono: this.formulario.value.telefono,
      tipodocumento: this.formulario.value.tipodocumento,
      documento: this.formulario.value.documento,
      usuario: {
        email: this.formulario.value.email,
        rol: this.formulario.value.rol,
        password: this.formulario.value.password
      }
    };

    const esVeterinario = this.formulario.value.rol === 'Veterinario';

    this.trabajadoresService.createTrabajador(
      trabajador,
      esVeterinario,
      this.formulario.value.especialidad,
      this.diasSemana  // Enviar configuración completa de horarios
    ).subscribe({
      next: () => {
        this.router.navigate(['/trabajadores'], {
          state: { mensaje: '✅ Trabajador creado exitosamente con horarios configurados' }
        });
      },
      error: (error) => {
        console.error('Error:', error);
        if (error.error?.hora) {
          this.mostrarError(`Validación de horario: ${error.error.hora}`);
        } else {
          this.mostrarError('Error al crear el trabajador');
        }
      }
    });
  }
}
```

---

---

## 🚨 CAMBIOS CRÍTICOS DEL BACKEND (Actualizaciones Recientes)

### **1. VeterinarioSerializer Actualizado**

El backend **ahora incluye automáticamente** los siguientes campos en todas las respuestas de veterinarios:

```python
# api/serializers.py - VeterinarioSerializer
fields = ['id', 'trabajador', 'trabajador_detalle', 'especialidad',
          'especialidad_detalle', 'nombreEspecialidad', 'dias_trabajo',
          'horarios_trabajo']
```

**Campos nuevos generados automáticamente (read-only):**
- `trabajador_detalle`: Objeto completo con datos del trabajador
- `especialidad_detalle`: Objeto completo con datos de la especialidad
- `horarios_trabajo`: Array con configuración completa de horarios

### **2. Endpoints de Horarios ya Implementados**

Todos estos endpoints **YA ESTÁN FUNCIONANDO** en el backend:

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/horarios-trabajo/` | Listar todos los horarios |
| `GET` | `/api/horarios-trabajo/?veterinario={id}` | Filtrar por veterinario |
| `GET` | `/api/horarios-trabajo/{id}/` | Obtener un horario |
| `POST` | `/api/horarios-trabajo/` | Crear horario |
| `PUT` | `/api/horarios-trabajo/{id}/` | Actualizar completo |
| `PATCH` | `/api/horarios-trabajo/{id}/` | Actualizar parcial |
| `DELETE` | `/api/horarios-trabajo/{id}/` | Eliminar |
| `PATCH` | `/api/horarios-trabajo/{id}/activar/` | Activar |
| `PATCH` | `/api/horarios-trabajo/{id}/desactivar/` | Desactivar |
| `GET` | `/api/horarios-trabajo/veterinario/{vet_id}/` | Horarios de veterinario específico |
| `GET` | `/api/horarios-trabajo/disponibilidad_semana/` | Disponibilidad semanal |

### **3. Validaciones de Citas ya Implementadas**

El modelo `Cita` **YA VALIDA AUTOMÁTICAMENTE**:

```python
# api/models.py - Cita.clean()
✅ Valida que la cita esté en un día laborable
✅ Valida que la hora esté dentro del horario de trabajo
✅ Valida que NO esté en horario de descanso
✅ Previene citas duplicadas (UniqueConstraint)
```

**Errores que el backend retorna:**
```json
{
  "hora": "El veterinario no trabaja los Domingos.",
  "error_code": "FUERA_DE_HORARIO"
}
```
```json
{
  "hora": "La hora 13:30:00 está en el horario de descanso (13:00:00 - 14:00:00).",
  "error_code": "FUERA_DE_HORARIO"
}
```
```json
{
  "non_field_errors": [
    "El veterinario ya tiene una cita agendada en esta fecha y hora."
  ]
}
```

### **4. Campos del HorarioTrabajoSerializer**

```python
# api/serializers.py
{
  "id": "uuid",
  "veterinario": "uuid",
  "veterinario_nombre": "Nombre completo - Especialidad",  # Calculado
  "dia_semana": 0-6,  # 0=Lunes, 6=Domingo
  "dia_display": "Lunes",  # Calculado desde choices
  "hora_inicio": "08:00:00",
  "hora_fin": "18:00:00",
  "hora_inicio_descanso": "13:00:00" | null,
  "hora_fin_descanso": "14:00:00" | null,
  "duracion_jornada": 9.0,  # Calculado (horas trabajadas netas)
  "activo": true
}
```

---

## 📋 RESUMEN: Lo que YA FUNCIONA vs Lo que FALTA

### ✅ **YA IMPLEMENTADO EN EL BACKEND:**

1. ✅ Modelo `HorarioTrabajo` con todos sus campos
2. ✅ Modelo `Cita` con validación de horarios (`clean()` method)
3. ✅ `HorarioTrabajoSerializer` completo con campos calculados
4. ✅ `VeterinarioSerializer` actualizado con `horarios_trabajo`, `trabajador_detalle`, `especialidad_detalle`
5. ✅ `HorarioTrabajoViewSet` con todos los endpoints CRUD
6. ✅ Endpoints de activar/desactivar horarios
7. ✅ Endpoint de disponibilidad semanal
8. ✅ UniqueConstraint en Cita (no duplicados)
9. ✅ Campo `estado` en Trabajador
10. ✅ Endpoints `activar/desactivar` en TrabajadorViewSet
11. ✅ Endpoint `reset-password` en TrabajadorViewSet
12. ✅ Endpoint `/api/veterinarios/por-trabajador/{trabajador_id}/`
13. ✅ Campo `tipodocumento_nombre` en TrabajadorSerializer

### ❌ **FALTA IMPLEMENTAR EN EL FRONTEND:**

1. ❌ Interface `HorarioTrabajo` en TypeScript
2. ❌ Actualizar interface `Veterinario` para incluir nuevos campos
3. ❌ Formulario de horarios en crear-trabajador.component
4. ❌ Formulario de horarios en editar-trabajador.component
5. ❌ Servicio `trabajadores.service.ts` con métodos para horarios
6. ❌ Visualización de horarios en modal de detalle
7. ❌ Validaciones de horarios en el formulario
8. ❌ Manejo de errores de validación de citas
9. ❌ Migración de datos existentes (opcional)
10. ❌ Actualizar filtros para usar horarios (opcional)

---

## 🎯 ACCIÓN INMEDIATA REQUERIDA

**El frontend debe actualizar URGENTEMENTE:**

1. **Interface Veterinario** - Agregar campos: `trabajador_detalle`, `especialidad_detalle`, `horarios_trabajo`
2. **Formularios** - Reemplazar checkboxes simples de días por configuración completa de horarios
3. **Servicio** - Agregar métodos para CRUD de horarios de trabajo
4. **Validación** - Manejar errores `FUERA_DE_HORARIO` del backend

**Sin estas actualizaciones:**
- ❌ Las citas seguirán fallando sin mensaje claro para el usuario
- ❌ No se podrán configurar horarios de veterinarios
- ❌ El sistema antiguo de `dias_trabajo` quedará obsoleto
- ❌ La integración backend-frontend estará rota

---

## 🎉 Conclusión

Con esta actualización, el sistema de gestión de trabajadores y veterinarios estará completamente integrado con el sistema de citas, permitiendo:

✅ **Validación automática** de disponibilidad de veterinarios
✅ **Configuración flexible** de horarios de trabajo
✅ **Prevención de conflictos** de agenda
✅ **Mejor experiencia** de usuario al agendar citas

**Sistema**: Veterinaria Huellitas
**Frontend**: Angular 19.2.10
**Backend**: Django 5.2.1 + PostgreSQL + DRF 3.16.0
**Fecha Actualización Backend**: 2025-10-09
**Última Actualización Documento**: 2025-10-09
