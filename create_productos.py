#!/usr/bin/env python
"""
Script para crear 10 productos de ejemplo en la base de datos
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from api.models import Producto

def crear_productos():
    productos_data = [
        {
            'nombre': 'Antiinflamatorio Metacam 5ml',
            'descripcion': 'Antiinflamatorio no esteroideo para perros y gatos',
            'proveedor': 'Boehringer Ingelheim',
            'tipo': 'medicamento',
            'subtipo': 'antiinflamatorio',
            'stock': 25,
            'precio_compra': 45.50,
            'precio_venta': 68.00,
            'fecha_vencimiento': '2025-08-15',
            'estado': 'Activo'
        },
        {
            'nombre': 'Vacuna Rabia Nobivac',
            'descripcion': 'Vacuna contra la rabia para perros y gatos',
            'proveedor': 'Merck Animal Health',
            'tipo': 'vacuna',
            'subtipo': 'rabia',
            'stock': 40,
            'precio_compra': 12.80,
            'precio_venta': 25.00,
            'fecha_vencimiento': '2025-06-30',
            'estado': 'Activo'
        },
        {
            'nombre': 'Shampoo Medicinal Virbac',
            'descripcion': 'Shampoo terapéutico para dermatitis en mascotas',
            'proveedor': 'Virbac',
            'tipo': 'higiene',
            'subtipo': 'dermatológico',
            'stock': 15,
            'precio_compra': 28.90,
            'precio_venta': 45.00,
            'fecha_vencimiento': '2026-12-31',
            'estado': 'Activo'
        },
        {
            'nombre': 'Hills Prescription Diet c/d Urinary 4kg',
            'descripcion': 'Alimento terapéutico para problemas urinarios en gatos',
            'proveedor': "Hill's Pet Nutrition",
            'tipo': 'alimento',
            'subtipo': 'terapéutico',
            'stock': 8,
            'precio_compra': 89.50,
            'precio_venta': 135.00,
            'fecha_vencimiento': '2025-11-20',
            'estado': 'Activo'
        },
        {
            'nombre': 'Collar Antiparasitario Seresto Perro Grande',
            'descripcion': 'Collar de larga duración contra pulgas y garrapatas',
            'proveedor': 'Elanco',
            'tipo': 'venta',
            'subtipo': 'antiparasitario',
            'stock': 12,
            'precio_compra': 85.00,
            'precio_venta': 120.00,
            'fecha_vencimiento': '2027-03-15',
            'estado': 'Activo'
        },
        {
            'nombre': 'Baytril 2.5% Inyectable 100ml',
            'descripcion': 'Antibiótico de amplio espectro para uso veterinario',
            'proveedor': 'Bayer',
            'tipo': 'medicamento',
            'subtipo': 'antibiótico',
            'stock': 6,
            'precio_compra': 125.00,
            'precio_venta': 180.00,
            'fecha_vencimiento': '2025-09-10',
            'estado': 'Activo'
        },
        {
            'nombre': 'Vanguard Plus 5 L4 CV',
            'descripcion': 'Vacuna múltiple para perros (distemper, parvovirus, etc.)',
            'proveedor': 'Zoetis',
            'tipo': 'vacuna',
            'subtipo': 'múltiple',
            'stock': 30,
            'precio_compra': 18.90,
            'precio_venta': 35.00,
            'fecha_vencimiento': '2025-07-25',
            'estado': 'Activo'
        },
        {
            'nombre': 'Omega 3 Premium para Mascotas',
            'descripcion': 'Suplemento nutricional de ácidos grasos omega 3',
            'proveedor': 'VetLife',
            'tipo': 'alimento',
            'subtipo': 'suplemento',
            'stock': 22,
            'precio_compra': 35.60,
            'precio_venta': 55.00,
            'fecha_vencimiento': '2026-05-18',
            'estado': 'Activo'
        },
        {
            'nombre': 'Drontal Plus Comprimidos',
            'descripcion': 'Desparasitante interno para perros, amplio espectro',
            'proveedor': 'Bayer',
            'tipo': 'medicamento',
            'subtipo': 'antiparasitario',
            'stock': 18,
            'precio_compra': 22.40,
            'precio_venta': 38.00,
            'fecha_vencimiento': '2025-12-08',
            'estado': 'Activo'
        },
        {
            'nombre': 'Toallitas Húmedas Pet Clean x50',
            'descripcion': 'Toallitas de limpieza para mascotas con extractos naturales',
            'proveedor': 'Pet Care Solutions',
            'tipo': 'higiene',
            'subtipo': 'limpieza',
            'stock': 35,
            'precio_compra': 8.50,
            'precio_venta': 15.00,
            'fecha_vencimiento': '2027-01-30',
            'estado': 'Activo'
        }
    ]

    productos_creados = 0
    productos_existentes = 0

    for data in productos_data:
        # Verificar si el producto ya existe
        if Producto.objects.filter(nombre=data['nombre']).exists():
            print(f"❯ El producto '{data['nombre']}' ya existe - OMITIDO")
            productos_existentes += 1
            continue

        try:
            # Convertir fecha string a objeto date
            fecha_venc = datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d').date()
            data['fecha_vencimiento'] = fecha_venc

            producto = Producto.objects.create(**data)
            
            # Calcular margen de ganancia
            margen = float(producto.precio_venta - producto.precio_compra)
            porcentaje_margen = (margen / float(producto.precio_compra)) * 100
            
            print(f"✅ Creado: {producto.nombre}")
            print(f"   💰 Compra: S/{producto.precio_compra} | Venta: S/{producto.precio_venta}")
            print(f"   📈 Margen: S/{margen:.2f} ({porcentaje_margen:.1f}%)")
            print(f"   📦 Stock: {producto.stock} | Tipo: {producto.get_tipo_display()}")
            print()
            
            productos_creados += 1
            
        except Exception as e:
            print(f"❌ Error creando '{data['nombre']}': {str(e)}")

    print("="*60)
    print(f"📊 RESUMEN:")
    print(f"✅ Productos creados: {productos_creados}")
    print(f"⚠️  Productos existentes: {productos_existentes}")
    print(f"📦 Total en base de datos: {Producto.objects.count()}")
    print("="*60)

    # Mostrar análisis de rentabilidad
    if productos_creados > 0:
        print("\n💹 ANÁLISIS DE RENTABILIDAD:")
        productos = Producto.objects.all().order_by('-precio_venta')
        
        for producto in productos[:5]:  # Top 5 más caros
            margen = float(producto.precio_venta - producto.precio_compra)
            porcentaje = (margen / float(producto.precio_compra)) * 100
            print(f"• {producto.nombre[:30]:<30} | Margen: {porcentaje:5.1f}% | Ganancia: S/{margen:6.2f}")

if __name__ == '__main__':
    print("🏥 Creando productos para Veterinaria Huellitas...")
    print("="*60)
    crear_productos()