import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import TipoCita

def limpiar_tipos_bano():
    print("LIMPIANDO TIPOS DE CITA DE BAÑO")
    print("=" * 35)

    tipos_bano_eliminar = [
        'Baño Básico',
        'Baño + Corte',
        'Baño + Uñas',
        'Baño Completo'
    ]

    eliminados = 0
    for nombre in tipos_bano_eliminar:
        try:
            tipo = TipoCita.objects.get(nombre=nombre)
            print(f"  Eliminando: {tipo.nombre}")
            tipo.delete()
            eliminados += 1
        except TipoCita.DoesNotExist:
            print(f"  Ya no existe: {nombre}")

    print(f"\nEliminados: {eliminados} tipos de cita de baño")

    print("\nTIPOS DE CITA RESTANTES:")
    print("=" * 35)
    for tipo in TipoCita.objects.filter(estado='Activo').order_by('nombre'):
        print(f"  ✅ {tipo.nombre} ({tipo.duracion_minutos} min)")

    print(f"\nTotal tipos de cita: {TipoCita.objects.filter(estado='Activo').count()}")
    print("\n✅ LIMPIEZA COMPLETADA!")
    print("Ahora usa el módulo de SERVICIOS para baño (ya existe)")

if __name__ == '__main__':
    limpiar_tipos_bano()