#!/usr/bin/env python3
"""
SCRIPT DE LIMPIEZA DE DUPLICADOS - Sistema Veterinario Huellitas
Autor: Claude Code Django
Fecha: 2025-09-15
"""

import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import HistorialVacunacion, Mascota, Vacuna
from django.db import transaction

def fix_specific_duplicate():
    """
    Corregir el duplicado específico de Animal prueba 12
    """
    print("Buscando duplicados de Animal prueba 12...")

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

    print(f"Encontrados {registros_duplicados.count()} registros duplicados")

    if registros_duplicados.count() > 1:
        # Mantener el primero, eliminar los demás
        registro_a_mantener = registros_duplicados.first()
        registros_a_eliminar = registros_duplicados.exclude(id=registro_a_mantener.id)

        print(f"Manteniendo registro: {registro_a_mantener.id}")
        for registro in registros_a_eliminar:
            print(f"Eliminando duplicado: {registro.id}")
            registro.delete()

        # Actualizar observaciones del registro mantenido
        registro_a_mantener.observaciones = "(Aplicada en clinica externa) Dosis 2/2 - Protocolo completo - Duplicado corregido"
        registro_a_mantener.save()

        print("DUPLICADOS CORREGIDOS EXITOSAMENTE")
        return True
    else:
        print("No se encontraron duplicados para corregir")
        return False

def find_all_duplicates():
    """
    Buscar todos los duplicados en el sistema
    """
    print("\nBuscando todos los duplicados en el sistema...")

    from django.db.models import Count

    duplicados = HistorialVacunacion.objects.values(
        'mascota_id', 'vacuna_id', 'fecha_aplicacion', 'dosis_numero'
    ).annotate(
        count=Count('id')
    ).filter(count__gt=1)

    total_duplicados = len(duplicados)
    print(f"REPORTE: {total_duplicados} grupos de duplicados encontrados")

    for dup in duplicados:
        print(f"\nDUPLICADO DETECTADO:")
        print(f"   Mascota: {dup['mascota_id']}")
        print(f"   Vacuna: {dup['vacuna_id']}")
        print(f"   Fecha: {dup['fecha_aplicacion']}")
        print(f"   Dosis: {dup['dosis_numero']}")
        print(f"   Cantidad: {dup['count']} registros")

    return total_duplicados

def main():
    """
    Función principal
    """
    print("SISTEMA DE LIMPIEZA DE DUPLICADOS - VETERINARIA HUELLITAS")
    print("=" * 60)

    try:
        # 1. Corregir el caso específico reportado
        corregido = fix_specific_duplicate()

        # 2. Buscar todos los duplicados en el sistema
        total_duplicados = find_all_duplicates()

        if corregido:
            print("\nEL DUPLICADO ESPECIFICO HA SIDO CORREGIDO")

        if total_duplicados > 0:
            print(f"\nSe encontraron {total_duplicados} grupos adicionales de duplicados")
            print("Revisa el log anterior para mas detalles")
        else:
            print("\nNo se encontraron duplicados adicionales")

        print("\nPROCESO COMPLETADO EXITOSAMENTE")

    except Exception as e:
        print(f"ERROR DURANTE EL PROCESO: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()