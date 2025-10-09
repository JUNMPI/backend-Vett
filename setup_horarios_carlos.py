#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para configurar horarios de trabajo del veterinario Carlos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Veterinario, HorarioTrabajo
from datetime import time

# Obtener veterinario Carlos
vet = Veterinario.objects.get(id='7daca2f6-b80f-4737-9e02-9c4669dcd101')

print('=' * 70)
print('CONFIGURACION DE HORARIOS DE TRABAJO')
print('=' * 70)
print(f'Veterinario: {vet.trabajador.nombres} {vet.trabajador.apellidos}')
print()

# Limpiar horarios anteriores
HorarioTrabajo.objects.filter(veterinario=vet).delete()

# Configurar horarios
horarios = [
    # Lunes a Viernes: 8:00 - 18:00 con descanso 13:00 - 14:00
    {
        'dia_semana': 0,  # Lunes
        'hora_inicio': time(8, 0),
        'hora_fin': time(18, 0),
        'tiene_descanso': True,
        'hora_inicio_descanso': time(13, 0),
        'hora_fin_descanso': time(14, 0),
    },
    {
        'dia_semana': 1,  # Martes
        'hora_inicio': time(8, 0),
        'hora_fin': time(18, 0),
        'tiene_descanso': True,
        'hora_inicio_descanso': time(13, 0),
        'hora_fin_descanso': time(14, 0),
    },
    {
        'dia_semana': 2,  # Miércoles
        'hora_inicio': time(8, 0),
        'hora_fin': time(18, 0),
        'tiene_descanso': True,
        'hora_inicio_descanso': time(13, 0),
        'hora_fin_descanso': time(14, 0),
    },
    {
        'dia_semana': 3,  # Jueves
        'hora_inicio': time(8, 0),
        'hora_fin': time(18, 0),
        'tiene_descanso': True,
        'hora_inicio_descanso': time(13, 0),
        'hora_fin_descanso': time(14, 0),
    },
    {
        'dia_semana': 4,  # Viernes
        'hora_inicio': time(8, 0),
        'hora_fin': time(18, 0),
        'tiene_descanso': True,
        'hora_inicio_descanso': time(13, 0),
        'hora_fin_descanso': time(14, 0),
    },
    # Sábado: 9:00 - 13:00 (sin descanso)
    {
        'dia_semana': 5,  # Sábado
        'hora_inicio': time(9, 0),
        'hora_fin': time(13, 0),
        'tiene_descanso': False,
    },
    # Domingo: No trabaja
]

print('Creando horarios de trabajo:')
print()

for config in horarios:
    horario = HorarioTrabajo.objects.create(
        veterinario=vet,
        activo=True,
        **config
    )
    dia = dict(HorarioTrabajo.DIAS_SEMANA)[config['dia_semana']]
    print(f'  {dia:12} {config["hora_inicio"]} - {config["hora_fin"]}', end='')
    if config.get('tiene_descanso'):
        print(f' (Descanso: {config["hora_inicio_descanso"]} - {config["hora_fin_descanso"]})')
    else:
        print()

print()
print('[OK] Horarios configurados exitosamente!')
print()

# Resumen
print('=' * 70)
print('RESUMEN')
print('=' * 70)
print()
print('HORARIO LABORAL:')
print('  Lunes - Viernes: 08:00 - 18:00 (con descanso 13:00 - 14:00)')
print('  Sabado:          09:00 - 13:00 (sin descanso)')
print('  Domingo:         NO TRABAJA')
print()
print('HORAS VALIDAS PARA CITAS:')
print('  Lunes - Viernes: 08:00 - 13:00 y 14:00 - 18:00')
print('  Sabado:          09:00 - 13:00')
print()
print('HORAS NO VALIDAS:')
print('  - Antes de 08:00 (L-V) o 09:00 (Sab)')
print('  - Despues de 18:00 (L-V) o 13:00 (Sab)')
print('  - Durante descanso: 13:00 - 14:00 (L-V)')
print('  - Todo el dia domingo')
print()
print('=' * 70)
