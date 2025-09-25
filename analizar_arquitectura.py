import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Servicio, TipoCita, Cita

def analizar_arquitectura():
    print("ANÁLISIS DE ARQUITECTURA: TIPOCITA vs SERVICIOS")
    print("=" * 55)

    print("\n1. SERVICIOS ACTUALES (con precios):")
    print("-" * 35)
    servicios = Servicio.objects.filter(estado='Activo').order_by('nombre')
    for s in servicios:
        print(f"  💰 {s.nombre} - ${s.precio}")

    print(f"\n   Total servicios: {servicios.count()}")

    print("\n2. TIPOS DE CITA ACTUALES (con duraciones):")
    print("-" * 45)
    tipos = TipoCita.objects.filter(estado='Activo').order_by('nombre')
    for t in tipos:
        print(f"  ⏰ {t.nombre} - {t.duracion_minutos} min")

    print(f"\n   Total tipos de cita: {tipos.count()}")

    print("\n3. CITAS EXISTENTES - ¿QUÉ USAN?")
    print("-" * 35)
    total_citas = Cita.objects.count()
    print(f"  📅 Total citas en DB: {total_citas}")

    if total_citas > 0:
        # Ver una cita de ejemplo
        cita_ejemplo = Cita.objects.first()
        print(f"\n   Ejemplo de cita:")
        print(f"   - Mascota: {cita_ejemplo.mascota.nombreMascota}")
        print(f"   - Servicio: {cita_ejemplo.servicio.nombre} (${cita_ejemplo.servicio.precio})")
        print(f"   - Veterinario: {cita_ejemplo.veterinario}")
        print(f"   - Fecha/Hora: {cita_ejemplo.fecha} {cita_ejemplo.hora}")

    print("\n4. PROBLEMA IDENTIFICADO:")
    print("-" * 30)
    print("  🤔 Las citas usan SERVICIOS (con precios)")
    print("  🤔 Pero creamos TIPOS DE CITA con duraciones")
    print("  🤔 ¿Son complementarios o duplicados?")

    print("\n5. OPCIONES DE ARQUITECTURA:")
    print("-" * 35)
    print("  A) SOLO SERVICIOS:")
    print("     - Agregar campo 'duracion_minutos' a Servicio")
    print("     - Eliminar TipoCita completamente")
    print("     - Más simple, todo en un lugar")

    print("\n  B) SERVICIOS + TIPOCITA (COMPLEMENTARIOS):")
    print("     - Servicio = Qué se hace + Precio")
    print("     - TipoCita = Cómo se agenda + Duración + Prioridad")
    print("     - Relación: Un servicio puede tener un tipo de cita asociado")

    print("\n  C) MIGRAR TODO A TIPOCITA:")
    print("     - Agregar precios a TipoCita")
    print("     - Migrar servicios existentes")
    print("     - Cambiar referencias en Cita")

if __name__ == '__main__':
    analizar_arquitectura()