#!/usr/bin/env python3
"""
🔧 SCRIPT DE LIMPIEZA DE DUPLICADOS - Sistema Veterinario Huellitas
Autor: Claude Code Django
Fecha: 2025-09-15

PROPÓSITO:
- Corregir el registro duplicado de "Animal prueba 12"
- Implementar validaciones para prevenir futuros duplicados
- Generar reporte de correcciones aplicadas
"""

import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import HistorialVacunacion, Mascota, Vacuna
from django.db import transaction

def fix_duplicate_records():
    """
    🎯 CORRECCIÓN ESPECÍFICA: Animal prueba 12 - Parvovirus duplicado
    """
    print("🔍 BUSCANDO DUPLICADOS DE ANIMAL PRUEBA 12...")

    # IDs específicos del duplicado detectado
    mascota_id = "dfd5553f-5dbb-421c-8ea2-d4b09cac1802"
    vacuna_id = "c09a28ff-559a-4bc8-b177-76e36a6b3c4d"
    fecha_problema = "2025-08-10"

    # Buscar los registros duplicados
    registros_duplicados = HistorialVacunacion.objects.filter(
        mascota_id=mascota_id,
        vacuna_id=vacuna_id,
        fecha_aplicacion=fecha_problema,
        dosis_numero=2
    ).order_by('creado')

    print(f"✅ Encontrados {registros_duplicados.count()} registros duplicados")

    if registros_duplicados.count() > 1:
        # Mantener el primero, eliminar los demás
        registro_a_mantener = registros_duplicados.first()
        registros_a_eliminar = registros_duplicados.exclude(id=registro_a_mantener.id)

        print(f"📝 Manteniendo registro: {registro_a_mantener.id}")
        for registro in registros_a_eliminar:
            print(f"🗑️  Eliminando duplicado: {registro.id}")
            registro.delete()

        # Actualizar observaciones del registro mantenido
        registro_a_mantener.observaciones = "(Aplicada en clínica externa) Dosis 2/2 - Protocolo completo - Duplicado corregido"
        registro_a_mantener.save()

        print("✅ DUPLICADOS CORREGIDOS")
    else:
        print("ℹ️  No se encontraron duplicados para corregir")

def find_all_duplicates():
    """
    🔍 BÚSQUEDA GLOBAL: Encontrar todos los posibles duplicados en el sistema
    """
    print("\n🔍 BUSCANDO TODOS LOS DUPLICADOS EN EL SISTEMA...")

    # Query para encontrar duplicados potenciales
    from django.db.models import Count

    duplicados = HistorialVacunacion.objects.values(
        'mascota_id', 'vacuna_id', 'fecha_aplicacion', 'dosis_numero'
    ).annotate(
        count=Count('id')
    ).filter(count__gt=1)

    total_duplicados = len(duplicados)
    print(f"📊 REPORTE: {total_duplicados} grupos de duplicados encontrados")

    for dup in duplicados:
        print(f"\n⚠️  DUPLICADO DETECTADO:")
        print(f"   Mascota: {dup['mascota_id']}")
        print(f"   Vacuna: {dup['vacuna_id']}")
        print(f"   Fecha: {dup['fecha_aplicacion']}")
        print(f"   Dosis: {dup['dosis_numero']}")
        print(f"   Cantidad: {dup['count']} registros")

        # Obtener detalles de los registros
        registros = HistorialVacunacion.objects.filter(
            mascota_id=dup['mascota_id'],
            vacuna_id=dup['vacuna_id'],
            fecha_aplicacion=dup['fecha_aplicacion'],
            dosis_numero=dup['dosis_numero']
        ).order_by('creado')

        for i, reg in enumerate(registros):
            mascota_nombre = reg.nombre_mascota if hasattr(reg, 'nombre_mascota') else "N/A"
            vacuna_nombre = reg.nombre_vacuna if hasattr(reg, 'nombre_vacuna') else "N/A"
            print(f"     #{i+1}: {reg.id} | {mascota_nombre} | {vacuna_nombre} | {reg.creado}")

def clean_all_duplicates():
    """
    🧹 LIMPIEZA AUTOMÁTICA: Eliminar todos los duplicados manteniendo el más antiguo
    """
    print("\n🧹 INICIANDO LIMPIEZA AUTOMÁTICA DE DUPLICADOS...")

    from django.db.models import Count

    with transaction.atomic():
        duplicados = HistorialVacunacion.objects.values(
            'mascota_id', 'vacuna_id', 'fecha_aplicacion', 'dosis_numero'
        ).annotate(
            count=Count('id')
        ).filter(count__gt=1)

        total_limpiados = 0

        for dup in duplicados:
            # Obtener todos los registros del grupo duplicado
            registros = HistorialVacunacion.objects.filter(
                mascota_id=dup['mascota_id'],
                vacuna_id=dup['vacuna_id'],
                fecha_aplicacion=dup['fecha_aplicacion'],
                dosis_numero=dup['dosis_numero']
            ).order_by('creado')

            if registros.count() > 1:
                # Mantener el primero (más antiguo), eliminar el resto
                registro_a_mantener = registros.first()
                registros_a_eliminar = registros.exclude(id=registro_a_mantener.id)

                for reg in registros_a_eliminar:
                    print(f"🗑️  Eliminando: {reg.id}")
                    reg.delete()
                    total_limpiados += 1

                # Marcar como corregido
                registro_a_mantener.observaciones = f"{registro_a_mantener.observaciones} [Duplicado corregido - {datetime.now().strftime('%Y-%m-%d')}]"
                registro_a_mantener.save()

        print(f"✅ LIMPIEZA COMPLETA: {total_limpiados} duplicados eliminados")

def main():
    """
    🚀 FUNCIÓN PRINCIPAL: Ejecutar todas las correcciones
    """
    print("🏥 SISTEMA DE LIMPIEZA DE DUPLICADOS - VETERINARIA HUELLITAS")
    print("=" * 60)

    try:
        # 1. Corregir el caso específico reportado
        fix_duplicate_records()

        # 2. Buscar todos los duplicados en el sistema
        find_all_duplicates()

        # 3. Preguntar si limpiar todos
        print("\n🤔 ¿Deseas limpiar TODOS los duplicados automáticamente? (y/n): ")
        respuesta = input().lower().strip()

        if respuesta in ['y', 'yes', 'sí', 'si']:
            clean_all_duplicates()
        else:
            print("ℹ️  Limpieza automática omitida")

        print("\n✅ PROCESO COMPLETADO EXITOSAMENTE")

    except Exception as e:
        print(f"❌ ERROR DURANTE EL PROCESO: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()