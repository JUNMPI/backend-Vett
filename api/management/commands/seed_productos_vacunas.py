# seed_productos_vacunas.py
from django.core.management.base import BaseCommand
from api.models import Vacuna, Producto
from api.choices import Estado
from decimal import Decimal
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Crea productos en inventario para todas las vacunas existentes y los vincula'

    def handle(self, *args, **options):
        vacunas = Vacuna.objects.all()
        
        laboratorios = [
            "Laboratorio VetPharma", 
            "BioPet Industries", 
            "Zoetis Perú", 
            "MSD Animal Health",
            "Virbac Perú",
            "Merck Animal Health",
            "Boehringer Ingelheim",
            "Elanco Animal Health"
        ]
        
        productos_creados = 0
        productos_vinculados = 0
        
        for vacuna in vacunas:
            # Crear producto correspondiente en inventario
            nombre_producto = f"Vacuna {vacuna.nombre}"
            
            # Verificar si ya existe un producto similar
            producto_existente = Producto.objects.filter(
                nombre__icontains=vacuna.nombre
            ).first()
            
            if not producto_existente:
                # Generar datos realistas para el producto
                precio_base = random.uniform(35.0, 120.0)
                stock_inicial = random.randint(15, 80)
                laboratorio = random.choice(laboratorios)
                
                # Fecha de vencimiento entre 1-3 años
                dias_vencimiento = random.randint(365, 1095)
                fecha_vencimiento = date.today() + timedelta(days=dias_vencimiento)
                
                # Descripción basada en la especie y enfermedad
                especie_str = ', '.join(vacuna.especies) if vacuna.especies else 'Múltiples especies'
                descripcion = f"Vacuna para {especie_str.lower()} que previene: {vacuna.enfermedad_previene[:100]}..."
                
                producto = Producto.objects.create(
                    nombre=nombre_producto,
                    descripcion=descripcion,
                    proveedor=laboratorio,
                    tipo="Vacuna",
                    subtipo=f"Vacuna {especie_str}",
                    stock=stock_inicial,
                    precio_compra=Decimal(str(round(precio_base, 2))),
                    precio_venta=Decimal(str(round(precio_base * 1.4, 2))),  # 40% markup
                    fecha_vencimiento=fecha_vencimiento,
                    estado=Estado.ACTIVO
                )
                productos_creados += 1
                print(f'Producto creado: {producto.nombre} - Stock: {producto.stock} - Precio: ${producto.precio_venta}')
                
                # Vincular la vacuna con el producto
                vacuna.producto_inventario = producto
                vacuna.save()
                productos_vinculados += 1
                print(f'  Vinculado con vacuna: {vacuna.nombre}')
            else:
                # Si existe un producto similar, vincularlo
                vacuna.producto_inventario = producto_existente
                vacuna.save()
                productos_vinculados += 1
                print(f'Producto existente vinculado: {producto_existente.nombre} - {vacuna.nombre}')
        
        print(f'\n=== RESUMEN ===')
        print(f'Productos creados: {productos_creados}')
        print(f'Vacunas vinculadas: {productos_vinculados}')
        print(f'Total productos tipo "Vacuna": {Producto.objects.filter(tipo="Vacuna").count()}')
        print(f'Total vacunas con producto: {Vacuna.objects.filter(producto_inventario__isnull=False).count()}')