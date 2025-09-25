import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Servicio

configuraciones = {
    'Consulta': {
        'descripcion': 'Consulta veterinaria general, examen fisico y diagnostico',
        'duracion_minutos': 30,
        'tiempo_preparacion': 5,
        'tiempo_limpieza': 10,
        'prioridad': 2,
        'color': '#28a745',
    },
    'bañado simple': {
        'descripcion': 'Baño basico con shampoo, secado y cepillado',
        'duracion_minutos': 45,
        'tiempo_preparacion': 10,
        'tiempo_limpieza': 15,
        'prioridad': 1,
        'color': '#17a2b8',
    },
    'bañado mas corte simple': {
        'descripcion': 'Baño completo con corte de pelo basico segun raza',
        'duracion_minutos': 75,
        'tiempo_preparacion': 10,
        'tiempo_limpieza': 20,
        'prioridad': 2,
        'color': '#fd7e14',
    },
    'bañado premium': {
        'descripcion': 'Servicio completo: baño, corte, uñas, limpieza de oidos y accesorios',
        'duracion_minutos': 120,
        'tiempo_preparacion': 15,
        'tiempo_limpieza': 25,
        'prioridad': 2,
        'color': '#e83e8c',
    }
}

print("ACTUALIZANDO SERVICIOS...")

actualizados = 0
for servicio in Servicio.objects.filter(estado='Activo'):
    if servicio.nombre in configuraciones:
        config = configuraciones[servicio.nombre]

        servicio.descripcion = config['descripcion']
        servicio.duracion_minutos = config['duracion_minutos']
        servicio.tiempo_preparacion = config['tiempo_preparacion']
        servicio.tiempo_limpieza = config['tiempo_limpieza']
        servicio.prioridad = config['prioridad']
        servicio.color = config['color']
        servicio.requiere_consultorio_especial = False
        servicio.permite_overlap = False

        servicio.save()
        actualizados += 1
        print(f"- {servicio.nombre} ({config['duracion_minutos']} min)")

print(f"\nActualizados: {actualizados} servicios")

print("\nSERVICIOS FINALES:")
for s in Servicio.objects.filter(estado='Activo'):
    print(f"- {s.nombre}: ${s.precio}, {s.duracion_minutos}min, {s.color}")

print("\nCOMPLETADO!")