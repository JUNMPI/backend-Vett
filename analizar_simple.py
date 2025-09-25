import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Servicio, TipoCita, Cita

print("ANALISIS DE ARQUITECTURA: TIPOCITA vs SERVICIOS")
print("=" * 50)

print("\n1. SERVICIOS ACTUALES:")
for s in Servicio.objects.filter(estado='Activo'):
    print(f"  - {s.nombre} (${s.precio})")

print(f"\nTotal servicios: {Servicio.objects.filter(estado='Activo').count()}")

print("\n2. TIPOS DE CITA ACTUALES:")
for t in TipoCita.objects.filter(estado='Activo'):
    print(f"  - {t.nombre} ({t.duracion_minutos} min)")

print(f"\nTotal tipos de cita: {TipoCita.objects.filter(estado='Activo').count()}")

print("\n3. CITAS EXISTENTES:")
citas = Cita.objects.all()
print(f"Total citas: {citas.count()}")

if citas.exists():
    cita = citas.first()
    print(f"\nEjemplo de cita:")
    print(f"  - Servicio usado: {cita.servicio.nombre}")
    print(f"  - Precio: ${cita.servicio.precio}")

print("\n" + "="*50)
print("PROBLEMA: Duplicacion conceptual")
print("- Citas referencian SERVICIOS (precios)")
print("- Pero creamos TIPOS DE CITA (duraciones)")
print("- Ambos describen lo mismo conceptualmente")

print("\nRECOMENDACION:")
print("Eliminar TipoCita y agregar duracion_minutos a Servicio")