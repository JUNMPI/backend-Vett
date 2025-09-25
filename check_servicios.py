import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Servicio, TipoCita

print("SERVICIOS ACTUALES:")
print("=" * 30)
for s in Servicio.objects.filter(estado='Activo'):
    print(f"  - {s.nombre} (${s.precio})")

print(f"\nTotal servicios: {Servicio.objects.filter(estado='Activo').count()}")

print("\nTIPOS DE CITA ACTUALES:")
print("=" * 30)
for t in TipoCita.objects.filter(estado='Activo'):
    print(f"  - {t.nombre} ({t.duracion_minutos} min)")

print(f"\nTotal tipos de cita: {TipoCita.objects.filter(estado='Activo').count()}")