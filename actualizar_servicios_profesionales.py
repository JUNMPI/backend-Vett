import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Servicio

def actualizar_servicios():
    print("ACTUALIZANDO SERVICIOS CON INFORMACIÓN PROFESIONAL")
    print("=" * 55)

    # Configuraciones por tipo de servicio
    configuraciones = {
        'Consulta': {
            'descripcion': 'Consulta veterinaria general, examen físico y diagnóstico',
            'duracion_minutos': 30,
            'tiempo_preparacion': 5,
            'tiempo_limpieza': 10,
            'prioridad': 2,
            'color': '#28a745',
            'requiere_consultorio_especial': False,
            'permite_overlap': False
        },
        'bañado simple': {
            'descripcion': 'Baño básico con shampoo, secado y cepillado',
            'duracion_minutos': 45,
            'tiempo_preparacion': 10,
            'tiempo_limpieza': 15,
            'prioridad': 1,
            'color': '#17a2b8',
            'requiere_consultorio_especial': False,
            'permite_overlap': False
        },
        'bañado mas corte simple': {
            'descripcion': 'Baño completo con corte de pelo básico según raza',
            'duracion_minutos': 75,
            'tiempo_preparacion': 10,
            'tiempo_limpieza': 20,
            'prioridad': 2,
            'color': '#fd7e14',
            'requiere_consultorio_especial': False,
            'permite_overlap': False
        },
        'bañado premium': {
            'descripcion': 'Servicio completo: baño, corte, uñas, limpieza de oídos y accesorios',
            'duracion_minutos': 120,
            'tiempo_preparacion': 15,
            'tiempo_limpieza': 25,
            'prioridad': 2,
            'color': '#e83e8c',
            'requiere_consultorio_especial': False,
            'permite_overlap': False
        }
    }

    servicios_actualizados = 0
    for servicio in Servicio.objects.filter(estado='Activo'):
        nombre = servicio.nombre

        if nombre in configuraciones:
            config = configuraciones[nombre]

            # Actualizar campos
            servicio.descripcion = config['descripcion']
            servicio.duracion_minutos = config['duracion_minutos']
            servicio.tiempo_preparacion = config['tiempo_preparacion']
            servicio.tiempo_limpieza = config['tiempo_limpieza']
            servicio.prioridad = config['prioridad']
            servicio.color = config['color']
            servicio.requiere_consultorio_especial = config['requiere_consultorio_especial']
            servicio.permite_overlap = config['permite_overlap']

            servicio.save()
            servicios_actualizados += 1

            print(f"  ✅ {nombre}")
            print(f"     - Duración: {config['duracion_minutos']} min")
            print(f"     - Prioridad: {config['prioridad']}")
            print(f"     - Color: {config['color']}")
            print()
        else:
            print(f"  ⚠️  {nombre} - No encontrado en configuraciones")

    print(f"Servicios actualizados: {servicios_actualizados}")

    # Mostrar resumen final
    print("\n" + "=" * 55)
    print("SERVICIOS PROFESIONALES CONFIGURADOS:")

    for servicio in Servicio.objects.filter(estado='Activo'):
        duracion_total = servicio.duracion_total_minutos()
        es_emergencia = "🚨" if servicio.es_emergencia() else ""

        print(f"  {es_emergencia}{servicio.nombre}")
        print(f"    💰 ${servicio.precio} | ⏱️ {servicio.duracion_minutos}min | 🎨 {servicio.color}")
        print(f"    📝 {servicio.descripcion[:50]}...")
        print()

    print("✅ SERVICIOS ACTUALIZADOS CON INFORMACIÓN PROFESIONAL")

if __name__ == '__main__':
    actualizar_servicios()