#!/usr/bin/env python
import os
import sys
import django
from datetime import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import TipoCita, HorarioTrabajo, SlotTiempo, Veterinario

def crear_datos():
    print("INICIALIZANDO SISTEMA PROFESIONAL DE CITAS")
    print("=" * 50)

    # 1. Crear tipos de cita
    print("\n1. Creando tipos de cita...")
    tipos = [
        {'nombre': 'Consulta General', 'descripcion': 'Consulta veterinaria general', 'duracion_minutos': 30, 'prioridad': 2, 'color': '#3498db'},
        {'nombre': 'Vacunacion', 'descripcion': 'Aplicacion de vacunas', 'duracion_minutos': 15, 'prioridad': 2, 'color': '#2ecc71'},
        {'nombre': 'Cirugia Menor', 'descripcion': 'Procedimientos quirurgicos menores', 'duracion_minutos': 60, 'prioridad': 3, 'color': '#f39c12'},
        {'nombre': 'Emergencia', 'descripcion': 'Atencion de emergencias', 'duracion_minutos': 45, 'prioridad': 5, 'color': '#e74c3c'},
    ]

    for tipo_data in tipos:
        tipo, created = TipoCita.objects.get_or_create(
            nombre=tipo_data['nombre'],
            defaults=tipo_data
        )
        print(f"  {'Creado' if created else 'Ya existe'}: {tipo.nombre}")

    # 2. Crear horarios para los primeros 3 veterinarios
    print("\n2. Creando horarios de trabajo...")
    veterinarios = Veterinario.objects.all()[:3]

    for vet in veterinarios:
        print(f"  Veterinario: {vet}")
        # Días 0-4 = Lunes a Viernes
        dias_trabajo = [0, 1, 2, 3, 4]  # Lunes a Viernes
        nombres_dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']

        for i, dia in enumerate(dias_trabajo):
            horario, created = HorarioTrabajo.objects.get_or_create(
                veterinario=vet,
                dia_semana=dia,
                defaults={
                    'hora_inicio': time(8, 0),
                    'hora_fin': time(17, 0),
                    'hora_inicio_descanso': time(12, 0),
                    'hora_fin_descanso': time(13, 0),
                    'activo': True
                }
            )
            if created:
                print(f"    {nombres_dias[i]}: 08:00-17:00")

    # 3. Generar algunos slots de prueba
    print("\n3. Generando slots de tiempo...")
    from datetime import date, timedelta, datetime

    manana = date.today() + timedelta(days=1)
    veterinario_ejemplo = veterinarios[0] if veterinarios else None

    if veterinario_ejemplo:
        # Crear algunos slots de prueba para mañana
        horas = [time(9, 0), time(9, 30), time(10, 0), time(10, 30), time(11, 0), time(11, 30)]

        for hora in horas:
            hora_fin = datetime.combine(manana, hora)
            hora_fin = (hora_fin + timedelta(minutes=30)).time()

            duracion = 30  # 30 minutos
            slot, created = SlotTiempo.objects.get_or_create(
                veterinario=veterinario_ejemplo,
                fecha=manana,
                hora_inicio=hora,
                hora_fin=hora_fin,
                defaults={
                    'disponible': True,
                    'duracion_minutos': duracion
                }
            )
            if created:
                print(f"    Slot: {hora} - {hora_fin}")

    # 4. Mostrar resumen
    print("\n" + "=" * 50)
    print("RESUMEN:")
    print(f"Tipos de cita: {TipoCita.objects.count()}")
    print(f"Horarios de trabajo: {HorarioTrabajo.objects.count()}")
    print(f"Slots de tiempo: {SlotTiempo.objects.count()}")
    print("\nSISTEMA INICIALIZADO CORRECTAMENTE!")
    print("\nEndpoints disponibles:")
    print("  /api/tipos-cita/")
    print("  /api/horarios-trabajo/")
    print("  /api/slots-tiempo/")
    print("  /api/citas-profesional/")

if __name__ == '__main__':
    try:
        crear_datos()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)