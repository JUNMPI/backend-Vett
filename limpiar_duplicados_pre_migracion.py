"""
Script para limpiar duplicados ANTES de aplicar constraints únicos
Ejecutar ANTES de hacer las migraciones
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Trabajador, Responsable, Usuario

print("=" * 70)
print("LIMPIEZA DE DUPLICADOS - PRE MIGRACION")
print("=" * 70)

# === PASO 1: LIMPIAR TRABAJADORES ===
print("\n[PASO 1/3] LIMPIEZA DE TRABAJADORES")
print("-" * 70)

# Caso: junior alvines y Ximena Alvines con documento 71448712
try:
    junior = Trabajador.objects.get(id='fe80d13b-8f49-4487-b793-124259541bd7')
    print(f"\n1. Trabajador: {junior.nombres} {junior.apellidos}")
    print(f"   Documento ACTUAL: {junior.documento}")
    print(f"   [CAMBIO] Nuevo documento: 71448713")

    junior.documento = '71448713'
    junior.save()
    print("   [OK] Documento actualizado exitosamente")

except Trabajador.DoesNotExist:
    print("\n1. [SKIP] junior alvines no encontrado (puede que ya fue corregido)")
except Exception as e:
    print(f"\n1. [ERROR] {str(e)}")

try:
    ximena = Trabajador.objects.get(id='4e84f660-c2d0-4779-b47c-54db4317486f')
    print(f"\n2. Trabajador: {ximena.nombres} {ximena.apellidos}")
    print(f"   Documento ACTUAL: {ximena.documento}")
    print(f"   [OK] Mantener documento: 71448712 (original)")

except Trabajador.DoesNotExist:
    print("\n2. [SKIP] Ximena Alvines no encontrada")

# Verificar otros duplicados de teléfono
print("\n3. Verificando telefonos duplicados...")
telefonos_dup = Trabajador.objects.filter(telefono='000000000')
if telefonos_dup.count() > 1:
    print(f"   [INFO] {telefonos_dup.count()} trabajadores con telefono 000000000 (placeholder)")
    print("   [ACCION] Se recomienda actualizar con telefonos reales")

# === PASO 2: LIMPIAR RESPONSABLES ===
print("\n[PASO 2/3] LIMPIEZA DE RESPONSABLES")
print("-" * 70)

# Caso: Maria Garcia Lopez y Juan Carlos Perez Lopez con documento 12345678
try:
    maria = Responsable.objects.get(id='c93ecbf0-90cc-4586-aa57-e87040354fed')
    print(f"\n1. Responsable: {maria.nombres} {maria.apellidos}")
    print(f"   Documento ACTUAL: {maria.documento}")
    print(f"   [CAMBIO] Nuevo documento: 87654321")

    maria.documento = '87654321'
    maria.save()
    print("   [OK] Documento actualizado exitosamente")

except Responsable.DoesNotExist:
    print("\n1. [SKIP] Maria Garcia Lopez no encontrada (puede que ya fue corregida)")
except Exception as e:
    print(f"\n1. [ERROR] {str(e)}")

try:
    juan = Responsable.objects.get(id='f0a9e302-03a9-4e54-804f-2a01b21c5188')
    print(f"\n2. Responsable: {juan.nombres} {juan.apellidos}")
    print(f"   Documento ACTUAL: {juan.documento}")
    print(f"   [OK] Mantener documento: 12345678 (original)")

except Responsable.DoesNotExist:
    print("\n2. [SKIP] Juan Carlos Perez Lopez no encontrado")

# === PASO 3: SINCRONIZAR EMAILS EN RESPONSABLES ===
print("\n[PASO 3/3] SINCRONIZACION DE EMAILS EN RESPONSABLES")
print("-" * 70)
print("\n[INFO] Preparando para eliminar campo Usuario en Responsable...")
print("[INFO] Sincronizando Responsable.email con Usuario.email\n")

responsables_sincronizados = 0
responsables_ya_sincronizados = 0

for responsable in Responsable.objects.all():
    try:
        if responsable.email != responsable.usuario.email:
            print(f"Responsable: {responsable.nombres} {responsable.apellidos}")
            print(f"  Email Responsable (viejo): {responsable.email}")
            print(f"  Email Usuario (usar este): {responsable.usuario.email}")

            # Usar el email del Usuario como fuente de verdad
            responsable.email = responsable.usuario.email
            responsable.save()

            print(f"  [OK] Email sincronizado")
            responsables_sincronizados += 1
        else:
            responsables_ya_sincronizados += 1

    except Exception as e:
        print(f"  [ERROR] {str(e)}")

print(f"\n[RESULTADO]")
print(f"  Responsables sincronizados: {responsables_sincronizados}")
print(f"  Responsables ya sincronizados: {responsables_ya_sincronizados}")

# === RESUMEN FINAL ===
print("\n" + "=" * 70)
print("RESUMEN DE LIMPIEZA")
print("=" * 70)

# Verificar que no queden duplicados
from django.db.models import Count

print("\n[VERIFICACION FINAL]")

# Trabajadores - Documentos duplicados
docs_trab_dup = Trabajador.objects.values('documento', 'tipodocumento').annotate(
    count=Count('id')
).filter(count__gt=1)

if docs_trab_dup.exists():
    print(f"  [ADVERTENCIA] Todavia hay {docs_trab_dup.count()} documentos duplicados en Trabajadores")
    for item in docs_trab_dup:
        print(f"    - Documento: {item['documento']} ({item['count']} registros)")
else:
    print("  [OK] No hay documentos duplicados en Trabajadores")

# Responsables - Documentos duplicados
docs_resp_dup = Responsable.objects.values('documento', 'tipodocumento').annotate(
    count=Count('id')
).filter(count__gt=1)

if docs_resp_dup.exists():
    print(f"  [ADVERTENCIA] Todavia hay {docs_resp_dup.count()} documentos duplicados en Responsables")
    for item in docs_resp_dup:
        print(f"    - Documento: {item['documento']} ({item['count']} registros)")
else:
    print("  [OK] No hay documentos duplicados en Responsables")

# Responsables - Emails desincronizados
emails_desinc = 0
for responsable in Responsable.objects.all():
    if responsable.email != responsable.usuario.email:
        emails_desinc += 1

if emails_desinc > 0:
    print(f"  [ADVERTENCIA] {emails_desinc} responsables con emails desincronizados")
else:
    print("  [OK] Todos los emails de Responsables estan sincronizados")

print("\n" + "=" * 70)
print("LIMPIEZA COMPLETADA")
print("=" * 70)
print("\n[SIGUIENTE PASO]")
print("1. Revisar que todo este correcto arriba")
print("2. Modificar los modelos (eliminar campos redundantes)")
print("3. Ejecutar: python manage.py makemigrations")
print("4. Ejecutar: python manage.py migrate")
print("=" * 70)
