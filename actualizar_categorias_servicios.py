import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import Servicio

def actualizar_categorias_servicios():
    print("ACTUALIZANDO CATEGORIAS DE SERVICIOS...")
    print("=" * 50)

    # Mapeo de servicios a categorías
    categorias_servicios = {
        'Consulta': 'CONSULTA',
        'bañado simple': 'BAÑADO',
        'bañado mas corte simple': 'BAÑADO',
        'bañado premium': 'BAÑADO',
    }

    servicios_actualizados = 0
    for servicio in Servicio.objects.filter(estado='Activo'):
        nombre = servicio.nombre

        if nombre in categorias_servicios:
            nueva_categoria = categorias_servicios[nombre]
            servicio.categoria = nueva_categoria
            servicio.save()
            servicios_actualizados += 1

            print(f"OK {nombre} -> {nueva_categoria}")
        else:
            print(f"INFO {nombre} - Manteniendo categoría por defecto: CONSULTA")

    print(f"\nServicios actualizados: {servicios_actualizados}")

    # Mostrar resumen final
    print("\n" + "=" * 50)
    print("SERVICIOS CON CATEGORIAS ASIGNADAS:")

    for categoria_key, categoria_name in Servicio.CATEGORIA_CHOICES:
        servicios_categoria = Servicio.objects.filter(categoria=categoria_key, estado='Activo')
        if servicios_categoria.exists():
            print(f"\n{categoria_name}:")
            for servicio in servicios_categoria:
                precio_fijo = "Precio fijo" if servicio.es_precio_fijo() else "Permite adicionales"
                print(f"  - {servicio.nombre} (S/ {servicio.precio}, {servicio.duracion_minutos}min) - {precio_fijo}")

    print("\nCATEGORIZACION COMPLETADA!")

if __name__ == '__main__':
    actualizar_categorias_servicios()