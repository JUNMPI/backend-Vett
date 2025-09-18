
import os
import sys
import django
sys.path.append(r'C:\Users\ASUS\Downloads\Veterinaria-Backend-Django (2)\Veterinaria-Backend-Django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huellitas.settings')
django.setup()

from api.models import HistorialVacunacion
from datetime import date, timedelta

print("Ejecutando actualización manual de estados...")

# Fechas para la lógica
fecha_hoy = date.today()
fecha_proxima = fecha_hoy + timedelta(days=30)  # 30 días de anticipación
fecha_limpieza = fecha_hoy - timedelta(days=90)  # Limpiar registros muy viejos

print(f"Fecha hoy: {fecha_hoy}")
print(f"Fecha límite próxima: {fecha_proxima}")

# Contar antes
total_antes = HistorialVacunacion.objects.count()
vencidas_antes = HistorialVacunacion.objects.filter(estado='vencida').count()
aplicadas_antes = HistorialVacunacion.objects.filter(estado='aplicada').count()
proximas_antes = HistorialVacunacion.objects.filter(estado='proxima').count()

print(f"\nANTES - Total: {total_antes}, Vencidas: {vencidas_antes}, Aplicadas: {aplicadas_antes}, Próximas: {proximas_antes}")

# 1. Marcar como vencidas las que pasaron su fecha
actualizadas_vencidas = HistorialVacunacion.objects.filter(
    proxima_fecha__lt=fecha_hoy,
    estado='aplicada'
).update(estado='vencida')

print(f"Marcadas como vencidas: {actualizadas_vencidas}")

# 2. Marcar como próximas las que están en rango de alerta
actualizadas_proximas = HistorialVacunacion.objects.filter(
    proxima_fecha__lte=fecha_proxima,
    proxima_fecha__gte=fecha_hoy,
    estado='aplicada'
).update(estado='proxima')

print(f"Marcadas como próximas: {actualizadas_proximas}")

# Contar después
vencidas_despues = HistorialVacunacion.objects.filter(estado='vencida').count()
aplicadas_despues = HistorialVacunacion.objects.filter(estado='aplicada').count()
proximas_despues = HistorialVacunacion.objects.filter(estado='proxima').count()

print(f"\nDESPUES - Vencidas: {vencidas_despues}, Aplicadas: {aplicadas_despues}, Próximas: {proximas_despues}")
print(f"Cambios - Vencidas: +{vencidas_despues - vencidas_antes}, Próximas: +{proximas_despues - proximas_antes}")

print("Actualización completada.")
