#!/usr/bin/env python3
"""
🔧 FIX DEFINITIVO - ACTUALIZACIÓN CORRECTA DE ESTADOS DE VACUNACIÓN
"""
import os, sys, django
sys.path.append(r'C:\Users\ASUS\Downloads\Veterinaria-Backend-Django (2)\Veterinaria-Backend-Django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import HistorialVacunacion
from datetime import date, timedelta

print("FIX DEFINITIVO - CORRIGIENDO ESTADOS DE VACUNACION")
print("="*60)

today = date.today()
fecha_proxima = today + timedelta(days=30)

print(f"Fecha actual: {today}")
print(f"Límite próximas: {fecha_proxima}")

# 1. Mostrar estado actual problemático
print(f"\n1. ESTADO ACTUAL PROBLEMÁTICO:")
print("-" * 40)

problematicos = HistorialVacunacion.objects.filter(
    proxima_fecha__lt=today,
    estado__in=['vigente', 'aplicada']
).order_by('proxima_fecha')

print(f"Registros con fechas vencidas pero estado incorrecto: {problematicos.count()}")

for prob in problematicos[:10]:  # Mostrar primeros 10
    dias_vencida = (today - prob.proxima_fecha).days
    print(f"  {prob.mascota.nombreMascota}: {prob.vacuna.nombre}")
    print(f"    Estado actual: {prob.estado}")
    print(f"    Próxima fecha: {prob.proxima_fecha} (vencida hace {dias_vencida} días)")
    print(f"    Estado correcto: vencida")
    print()

# 2. CORREGIR ESTADOS - APLICAR LÓGICA CORRECTA
print(f"\n2. APLICANDO CORRECCIONES:")
print("-" * 40)

# Marcar como VENCIDAS las que tienen proxima_fecha < today
vencidas_actualizadas = HistorialVacunacion.objects.filter(
    proxima_fecha__lt=today,
    estado__in=['vigente', 'aplicada', 'proxima']
).update(estado='vencida')

print(f"OK Marcadas como VENCIDA: {vencidas_actualizadas}")

# Marcar como PRÓXIMAS las que están en rango de 30 días
proximas_actualizadas = HistorialVacunacion.objects.filter(
    proxima_fecha__gte=today,
    proxima_fecha__lte=fecha_proxima,
    estado__in=['vigente', 'aplicada']
).update(estado='proxima')

print(f"OK Marcadas como PRÓXIMA: {proximas_actualizadas}")

# Marcar como VIGENTES las que tienen > 30 días
vigentes_actualizadas = HistorialVacunacion.objects.filter(
    proxima_fecha__gt=fecha_proxima,
    estado__in=['aplicada', 'proxima']
).update(estado='vigente')

print(f"OK Marcadas como VIGENTE: {vigentes_actualizadas}")

# 3. VERIFICAR CORRECCIONES
print(f"\n3. VERIFICANDO CORRECCIONES:")
print("-" * 40)

# Contar estados finales
from collections import Counter

todos_registros = HistorialVacunacion.objects.all()
estados_finales = [reg.estado for reg in todos_registros]
conteo_estados = Counter(estados_finales)

print(f"Estados finales del sistema:")
for estado, count in conteo_estados.most_common():
    print(f"  {estado}: {count}")

# 4. VERIFICAR QUE NO HAY INCONSISTENCIAS
print(f"\n4. VERIFICANDO COHERENCIA:")
print("-" * 40)

inconsistencias = 0

# Buscar vigentes vencidos
vigentes_vencidos = HistorialVacunacion.objects.filter(
    estado='vigente',
    proxima_fecha__lt=today
).count()

# Buscar vencidas futuras
vencidas_futuras = HistorialVacunacion.objects.filter(
    estado='vencida',
    proxima_fecha__gt=today
).count()

# Buscar próximas muy lejanas
proximas_lejanas = HistorialVacunacion.objects.filter(
    estado='proxima',
    proxima_fecha__gt=fecha_proxima
).count()

inconsistencias = vigentes_vencidos + vencidas_futuras + proximas_lejanas

if inconsistencias == 0:
    print("OK SISTEMA 100% COHERENTE")
    print("OK TODOS LOS ESTADOS CORRECTOS")
    print("OK FECHAS Y LÓGICA CONSISTENTES")
else:
    print(f"ERROR {inconsistencias} INCONSISTENCIAS ENCONTRADAS:")
    if vigentes_vencidos:
        print(f"  - {vigentes_vencidos} vigentes vencidos")
    if vencidas_futuras:
        print(f"  - {vencidas_futuras} vencidas futuras")
    if proximas_lejanas:
        print(f"  - {proximas_lejanas} próximas muy lejanas")

# 5. MOSTRAR CASOS ESPECÍFICOS CORREGIDOS
print(f"\n5. CASOS ESPECÍFICOS CORREGIDOS:")
print("-" * 40)

# Verificar los casos que mencionó el usuario
casos_especificos = [
    "Quintuple Canina", "Sextuple Canina", "Leptospirosis Canina", "Hepatitis Canina"
]

for vacuna_nombre in casos_especificos:
    registros = HistorialVacunacion.objects.filter(
        vacuna__nombre__icontains=vacuna_nombre
    ).order_by('-fecha_aplicacion')[:3]  # Últimos 3

    if registros:
        print(f"\n{vacuna_nombre}:")
        for reg in registros:
            dias_diff = (reg.proxima_fecha - today).days if reg.proxima_fecha else 0
            status = f"En {dias_diff} días" if dias_diff > 0 else f"Hace {abs(dias_diff)} días"
            print(f"  Mascota: {reg.mascota.nombreMascota}")
            print(f"  Estado: {reg.estado}")
            print(f"  Próxima: {reg.proxima_fecha} ({status})")

            # Verificar coherencia
            coherente = True
            if reg.estado == 'vigente' and dias_diff <= 0:
                coherente = False
            elif reg.estado == 'vencida' and dias_diff > 0:
                coherente = False

            print(f"  Coherencia: {'OK OK' if coherente else 'ERROR ERROR'}")
            print()

print(f"\n" + "="*60)
print(f"FIX DEFINITIVO COMPLETADO")
print(f"TOTAL CORRECCIONES APLICADAS: {vencidas_actualizadas + proximas_actualizadas + vigentes_actualizadas}")
print(f"SISTEMA ESTADO: {'OK OPERATIVO' if inconsistencias == 0 else 'ERROR REQUIERE REVISIÓN'}")
print(f"="*60)