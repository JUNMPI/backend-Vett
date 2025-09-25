#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import TipoCita

def agregar_servicios_bano():
    print("AGREGANDO SERVICIOS DE BAÑO AL SISTEMA")
    print("=" * 45)

    servicios_bano = [
        {
            'nombre': 'Baño Básico',
            'descripcion': 'Baño con shampoo, secado y cepillado básico',
            'duracion_minutos': 45,
            'prioridad': 2,
            'color': '#17a2b8',  # Celeste agua
            'tiempo_preparacion': 5,
            'tiempo_limpieza': 15
        },
        {
            'nombre': 'Baño + Corte',
            'descripcion': 'Baño completo con corte de pelo según raza',
            'duracion_minutos': 90,
            'prioridad': 2,
            'color': '#6610f2',  # Púrpura
            'tiempo_preparacion': 10,
            'tiempo_limpieza': 20
        },
        {
            'nombre': 'Baño + Uñas',
            'descripcion': 'Baño básico con corte de uñas profesional',
            'duracion_minutos': 60,
            'prioridad': 2,
            'color': '#fd7e14',  # Naranja
            'tiempo_preparacion': 5,
            'tiempo_limpieza': 15
        },
        {
            'nombre': 'Baño Completo',
            'descripcion': 'Servicio completo: baño, corte, uñas y limpieza de oídos',
            'duracion_minutos': 120,
            'prioridad': 2,
            'color': '#e83e8c',  # Rosa
            'tiempo_preparacion': 15,
            'tiempo_limpieza': 25
        }
    ]

    print("\nCreando tipos de cita para servicios de baño...")

    for servicio in servicios_bano:
        tipo_cita, created = TipoCita.objects.get_or_create(
            nombre=servicio['nombre'],
            defaults=servicio
        )

        if created:
            print(f"  Creado: {tipo_cita.nombre} ({tipo_cita.duracion_minutos} min)")
        else:
            print(f"  Ya existe: {tipo_cita.nombre}")

    # Mostrar resumen
    print(f"\n" + "=" * 45)
    print("RESUMEN:")
    print(f"Total tipos de cita: {TipoCita.objects.count()}")

    print("\nTipos disponibles:")
    for tipo in TipoCita.objects.filter(estado='Activo').order_by('nombre'):
        categoria = "MÉDICO" if tipo.nombre in ['Consulta General', 'Vacunacion', 'Cirugia Menor', 'Emergencia'] else "BAÑO"
        print(f"  [{categoria}] {tipo.nombre} - {tipo.duracion_minutos} min")

    print("\nSERVICIOS DE BAÑO AGREGADOS EXITOSAMENTE!")
    print("Los veterinarios ahora pueden agendar citas de baño en la misma agenda.")

if __name__ == '__main__':
    try:
        agregar_servicios_bano()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)