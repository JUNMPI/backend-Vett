"""
Verificar especialidades de veterinarios
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Veterinario, Especialidad

print("=" * 80)
print("VERIFICACION DE ESPECIALIDADES DE VETERINARIOS")
print("=" * 80)

# Listar todas las especialidades disponibles
print("\nEspecialidades disponibles:")
print("-" * 80)
especialidades = Especialidad.objects.all()
for esp in especialidades:
    print(f"  - ID: {esp.id} | Nombre: {esp.nombre} | Estado: {esp.estado}")

print(f"\nTotal especialidades: {especialidades.count()}")

# Listar veterinarios y sus especialidades
print("\n" + "=" * 80)
print("VETERINARIOS Y SUS ESPECIALIDADES:")
print("=" * 80)

veterinarios = Veterinario.objects.all()
sin_especialidad = 0
con_especialidad = 0
con_no_aplica = 0

for vet in veterinarios:
    trabajador = vet.trabajador
    nombre = f"{trabajador.nombres} {trabajador.apellidos}"

    if vet.especialidad:
        if vet.especialidad.nombre.lower() == 'no aplica':
            print(f"[WARN] {nombre:<40} | Especialidad: {vet.especialidad.nombre} (ID: {vet.especialidad.id})")
            con_no_aplica += 1
        else:
            print(f"[OK]   {nombre:<40} | Especialidad: {vet.especialidad.nombre}")
            con_especialidad += 1
    else:
        print(f"[NULL] {nombre:<40} | Especialidad: NULL")
        sin_especialidad += 1

print("\n" + "=" * 80)
print("RESUMEN:")
print("=" * 80)
print(f"Total veterinarios: {veterinarios.count()}")
print(f"  - Con especialidad valida: {con_especialidad}")
print(f"  - Con 'No aplica': {con_no_aplica}")
print(f"  - Sin especialidad (NULL): {sin_especialidad}")

# Verificar si existe especialidad "No aplica"
print("\n" + "=" * 80)
print("VERIFICACION DE 'NO APLICA':")
print("=" * 80)

no_aplica = Especialidad.objects.filter(nombre__iexact='no aplica')
if no_aplica.exists():
    print(f"[ENCONTRADO] Existe especialidad 'No aplica':")
    for esp in no_aplica:
        print(f"  - ID: {esp.id} | Nombre: {esp.nombre} | Estado: {esp.estado}")

    # Contar cuantos veterinarios tienen esta especialidad
    vets_con_no_aplica = Veterinario.objects.filter(especialidad__in=no_aplica)
    print(f"\nVeterinarios con 'No aplica': {vets_con_no_aplica.count()}")
else:
    print("[OK] No existe especialidad 'No aplica'")

print("\n" + "=" * 80)
print("SCRIPT COMPLETADO")
print("=" * 80)
