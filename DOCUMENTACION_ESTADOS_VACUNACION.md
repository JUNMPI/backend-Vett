# 📋 DOCUMENTACIÓN COMPLETA - ESTADOS DE VACUNACIÓN

## 🎯 **RESUMEN EJECUTIVO**
El sistema de vacunación maneja **6 estados diferentes** que se calculan dinámicamente según las fechas y la lógica de protocolos veterinarios.

---

## 🔍 **TODOS LOS ESTADOS DISPONIBLES**

### **1. VIGENTE**
- **Código**: `vigente`
- **Descripción**: Vacuna activa y efectiva
- **Condición**: Próxima fecha > 30 días en el futuro
- **Color sugerido**: 🟢 Verde
- **Ejemplo**: Vacuna aplicada hace 2 meses, próxima en 10 meses

### **2. PRÓXIMA**
- **Código**: `proxima`
- **Descripción**: Vacuna próxima a vencer (requiere atención)
- **Condición**: Próxima fecha entre 0 y 30 días
- **Color sugerido**: 🟡 Amarillo/Naranja
- **Ejemplo**: Vacuna vence en 15 días

### **3. VENCIDA**
- **Código**: `vencida`
- **Descripción**: Vacuna vencida (necesita renovación)
- **Condición**: Próxima fecha < fecha actual
- **Color sugerido**: 🔴 Rojo
- **Ejemplo**: Vacuna venció hace 2 meses

### **4. APLICADA**
- **Código**: `aplicada`
- **Descripción**: Vacuna recién aplicada (período de inmunización)
- **Condición**: Estado inicial al aplicar vacuna
- **Color sugerido**: 🔵 Azul
- **Ejemplo**: Vacuna aplicada hoy, desarrollando inmunidad

### **5. COMPLETADO**
- **Código**: `completado`
- **Descripción**: Protocolo finalizado/reemplazado por versión más reciente
- **Condición**: Vacuna antigua reemplazada por nueva aplicación
- **Color sugerido**: ⚫ Gris
- **Ejemplo**: Vacuna antigua sustituida por nueva

### **6. VENCIDA_REINICIO**
- **Código**: `vencida_reinicio`
- **Descripción**: Protocolo vencido que requiere reiniciar secuencia completa
- **Condición**: Vacuna multi-dosis vencida hace >60 días
- **Color sugerido**: 🟠 Naranja intenso
- **Ejemplo**: Segunda dosis de triple que debía aplicarse hace 6 meses

---

## 🧠 **LÓGICA DE CÁLCULO AUTOMÁTICO**

```python
def calcular_estado_dinamicamente(proxima_fecha, fecha_actual):
    dias_diferencia = (proxima_fecha - fecha_actual).days

    if dias_diferencia < 0:
        if abs(dias_diferencia) > 60 and es_multi_dosis:
            return 'vencida_reinicio'
        else:
            return 'vencida'
    elif 0 <= dias_diferencia <= 30:
        return 'proxima'
    else:
        return 'vigente'
```

---

## 📊 **DISTRIBUCIÓN TÍPICA EN EL SISTEMA**

Basado en datos reales del sistema (180 registros):
- **Vigente**: ~75 registros (42%)
- **Próxima**: ~64 registros (35%)
- **Completado**: ~36 registros (20%)
- **Vencida**: ~4 registros (2%)
- **Vencida_Reinicio**: ~1 registro (1%)
- **Aplicada**: Variable (nuevas aplicaciones)

---

## 🎨 **GUÍA VISUAL PARA FRONTEND**

### **Iconos Sugeridos**
- **Vigente**: ✅ o 🛡️
- **Próxima**: ⚠️ o 🔔
- **Vencida**: ❌ o ⏰
- **Aplicada**: 💉 o 🆕
- **Completado**: ✔️ o 📋
- **Vencida_Reinicio**: 🔄 o ⚠️⏰

### **Colores por Prioridad**
1. **🔴 CRÍTICO** - `vencida`, `vencida_reinicio`
2. **🟡 ATENCIÓN** - `proxima`
3. **🟢 NORMAL** - `vigente`, `aplicada`
4. **⚫ INACTIVO** - `completado`

---

## 🧪 **CASOS DE PRUEBA PARA FRONTEND**

### **Test 1: Estado VIGENTE**
```json
{
  "nombre_vacuna": "Antirrabica Canina",
  "fecha_aplicacion": "2025-01-18",
  "proxima_fecha": "2026-01-18",
  "estado": "vigente",
  "dias_restantes": 365
}
```

### **Test 2: Estado PRÓXIMA**
```json
{
  "nombre_vacuna": "Quintuple Canina",
  "fecha_aplicacion": "2024-09-18",
  "proxima_fecha": "2025-10-18",
  "estado": "proxima",
  "dias_restantes": 15
}
```

### **Test 3: Estado VENCIDA**
```json
{
  "nombre_vacuna": "Quintuple Canina",
  "fecha_aplicacion": "2024-07-18",
  "proxima_fecha": "2025-08-16",
  "estado": "vencida",
  "dias_vencida": 33
}
```

### **Test 4: Estado APLICADA**
```json
{
  "nombre_vacuna": "Antirrabica Felina",
  "fecha_aplicacion": "2025-09-18",
  "proxima_fecha": "2026-09-18",
  "estado": "aplicada",
  "recien_aplicada": true
}
```

### **Test 5: Estado VENCIDA_REINICIO**
```json
{
  "nombre_vacuna": "Triple Felina",
  "fecha_aplicacion": "2024-01-18",
  "proxima_fecha": "2024-03-18",
  "estado": "vencida_reinicio",
  "dias_vencida": 180,
  "requiere_reinicio": true
}
```

---

## 🔧 **IMPLEMENTACIÓN TÉCNICA**

### **Backend (Automático)**
- Los estados se calculan **dinámicamente** en cada consulta
- No se almacenan en base de datos (excepto como respaldo)
- Utiliza `SerializerMethodField` para cálculo en tiempo real

### **Frontend (Recomendado)**
- Mostrar estado calculado directamente del API
- Implementar colores y iconos según guía visual
- Añadir tooltips explicativos para cada estado
- Filtros por estado en listas de vacunas

### **Endpoints Relevantes**
- `GET /api/historial-vacunacion/` - Todos los registros con estados
- `GET /api/mascotas/{id}/historial-vacunacion/` - Historial por mascota
- `GET /api/dashboard/alertas-vacunacion/` - Vacunas críticas y próximas

---

## ⚡ **ESTADOS CRÍTICOS QUE REQUIEREN ACCIÓN**

### **ALTA PRIORIDAD**
- **`vencida_reinicio`**: Requiere reiniciar protocolo completo
- **`vencida`**: Necesita renovación inmediata

### **MEDIA PRIORIDAD**
- **`proxima`**: Programar cita próxima

### **MONITOREO**
- **`vigente`**: Sin acción requerida
- **`aplicada`**: Monitorear desarrollo de inmunidad
- **`completado`**: Solo para historial

---

## 🎯 **MENSAJES SUGERIDOS PARA USUARIO**

### **Por Estado**
- **Vigente**: "Protección activa ✅"
- **Próxima**: "Vence en X días - Programar cita ⚠️"
- **Vencida**: "Renovación requerida ❌"
- **Aplicada**: "Desarrollando inmunidad 💉"
- **Completado**: "Historial completado ✔️"
- **Vencida_Reinicio**: "Reiniciar protocolo 🔄"

---

## 📱 **CONSIDERACIONES UX/UI**

### **Dashboard Principal**
- Mostrar contadores por estado
- Alertas prominentes para vencidas/próximas
- Gráfico de distribución de estados

### **Lista de Vacunas**
- Estado como badge/chip colorido
- Ordenar por prioridad (críticos primero)
- Filtros rápidos por estado

### **Detalle de Mascota**
- Historial cronológico con estados
- Próximas fechas destacadas
- Alertas contextuales

---

**¡Sistema de estados 100% funcional y listo para implementación en frontend!** 🚀