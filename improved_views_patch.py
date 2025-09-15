#!/usr/bin/env python3
"""
🔧 MEJORAS ANTI-DUPLICADOS - Views.py
Sistema Veterinario Huellitas
Autor: Claude Code Django

MEJORAS IMPLEMENTADAS:
1. Transacciones atómicas con locks
2. Validaciones de timing robustas
3. Prevención de race conditions
4. Logging detallado de duplicados
"""

# ==================================================
# 🛡️ MEJORA 1: DECORATOR ANTI-DUPLICADOS
# ==================================================

from functools import wraps
from django.db import transaction
from django.core.cache import cache
from datetime import datetime, timedelta
import hashlib
import logging

logger = logging.getLogger(__name__)

def prevent_duplicates(key_fields=['mascota_id', 'vacuna_id', 'fecha_aplicacion', 'dosis_numero']):
    """
    🛡️ Decorator para prevenir duplicados usando cache y locks

    Uso:
    @prevent_duplicates(['mascota_id', 'vacuna_id', 'fecha_aplicacion'])
    def aplicar(self, request, pk=None):
        ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # Crear clave única basada en los campos
            data = request.data
            key_values = [str(data.get(field, '')) for field in key_fields]
            cache_key = f"duplicate_check:{hashlib.md5('_'.join(key_values).encode()).hexdigest()}"

            # Verificar si hay una operación en curso
            if cache.get(cache_key):
                return Response({
                    'success': False,
                    'message': 'Operación duplicada detectada. Espera un momento antes de reintentar.',
                    'error_code': 'DUPLICATE_OPERATION_IN_PROGRESS',
                    'status': 'error'
                }, status=status.HTTP_409_CONFLICT)

            # Marcar operación como en curso (expiración en 30 segundos)
            cache.set(cache_key, True, 30)

            try:
                result = func(self, request, *args, **kwargs)
                return result
            finally:
                # Limpiar el lock
                cache.delete(cache_key)

        return wrapper
    return decorator

# ==================================================
# 🔒 MEJORA 2: MÉTODO APLICAR MEJORADO
# ==================================================

def aplicar_mejorado(self, request, pk=None):
    """
    🎯 MÉTODO APLICAR MEJORADO CON VALIDACIONES ANTI-DUPLICADOS

    MEJORAS:
    1. Transacción atómica con SELECT FOR UPDATE
    2. Validaciones de timing más estrictas
    3. Prevención de race conditions
    4. Logging detallado para auditoría
    """
    from django.db import transaction
    from django.core.exceptions import ValidationError
    from datetime import datetime, timedelta
    from rest_framework import status
    from rest_framework.response import Response

    try:
        with transaction.atomic():
            # 🔒 LOCK EXCLUSIVO: Obtener vacuna con lock para prevenir race conditions
            try:
                vacuna = Vacuna.objects.select_for_update().get(id=pk)
            except Vacuna.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Vacuna no encontrada',
                    'error_code': 'VACCINE_NOT_FOUND',
                    'status': 'error'
                }, status=status.HTTP_404_NOT_FOUND)

            data = request.data

            # ✅ VALIDACIONES BÁSICAS MEJORADAS
            campos_requeridos = ['mascota_id', 'fecha_aplicacion', 'veterinario_id']
            for campo in campos_requeridos:
                if campo not in data or not data[campo]:
                    return Response({
                        'success': False,
                        'message': f'Campo requerido faltante: {campo}',
                        'error_code': 'MISSING_REQUIRED_FIELD',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # 📅 VALIDACIÓN DE FECHA
            try:
                fecha_aplicacion = date.fromisoformat(data['fecha_aplicacion'])
                fecha_hoy = date.today()

                # No permitir fechas muy futuras (más de 1 año)
                if fecha_aplicacion > fecha_hoy + timedelta(days=365):
                    return Response({
                        'success': False,
                        'message': 'Fecha de aplicación no puede ser más de 1 año en el futuro',
                        'error_code': 'INVALID_FUTURE_DATE',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)

            except ValueError:
                return Response({
                    'success': False,
                    'message': 'Formato de fecha inválido. Use YYYY-MM-DD',
                    'error_code': 'INVALID_DATE_FORMAT',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 🔍 VALIDACIÓN ANTI-DUPLICADOS ROBUSTA
            mascota_id = data['mascota_id']
            dosis_numero = data.get('dosis_numero', 1)

            # 🛡️ VALIDACIÓN 1: Duplicado exacto en timeframe crítico (últimos 5 minutos)
            timeframe_critico = datetime.now() - timedelta(minutes=5)

            duplicados_recientes = HistorialVacunacion.objects.select_for_update().filter(
                mascota_id=mascota_id,
                vacuna=vacuna,
                fecha_aplicacion=fecha_aplicacion,
                dosis_numero=dosis_numero,
                creado__gte=timeframe_critico,
                estado__in=['aplicada', 'vigente']
            )

            if duplicados_recientes.exists():
                # Log del intento de duplicado
                logger.warning(f"Intento de duplicado detectado: Mascota {mascota_id}, Vacuna {vacuna.id}, Fecha {fecha_aplicacion}, Dosis {dosis_numero}")

                return Response({
                    'success': False,
                    'message': f'Duplicado detectado: Ya se aplicó dosis {dosis_numero} de {vacuna.nombre} a esta mascota el {fecha_aplicacion} en los últimos 5 minutos.',
                    'error_code': 'RECENT_DUPLICATE_DETECTED',
                    'debug_info': {
                        'duplicados_encontrados': duplicados_recientes.count(),
                        'timeframe_verificado': '5 minutos',
                        'registros_duplicados': [str(reg.id) for reg in duplicados_recientes]
                    },
                    'status': 'error'
                }, status=status.HTTP_409_CONFLICT)

            # 🛡️ VALIDACIÓN 2: Múltiples aplicaciones mismo día (sospechoso)
            aplicaciones_mismo_dia = HistorialVacunacion.objects.filter(
                mascota_id=mascota_id,
                vacuna=vacuna,
                fecha_aplicacion=fecha_aplicacion,
                estado__in=['aplicada', 'vigente']
            ).count()

            if aplicaciones_mismo_dia >= vacuna.dosis_total:
                return Response({
                    'success': False,
                    'message': f'Ya se completó el protocolo de {vacuna.nombre} para esta mascota el {fecha_aplicacion}. Protocolo: {vacuna.dosis_total} dosis.',
                    'error_code': 'PROTOCOL_ALREADY_COMPLETED',
                    'debug_info': {
                        'aplicaciones_encontradas': aplicaciones_mismo_dia,
                        'protocolo_dosis_total': vacuna.dosis_total
                    },
                    'status': 'error'
                }, status=status.HTTP_409_CONFLICT)

            # 🎯 CONTINUACIÓN DEL PROCESO NORMAL...
            # (Aquí iría el resto de la lógica original del método aplicar)

            # Por ahora, retornamos una respuesta de éxito para testing
            return Response({
                'success': True,
                'message': f'Validaciones anti-duplicados pasadas correctamente',
                'data': {
                    'vacuna_id': str(vacuna.id),
                    'mascota_id': mascota_id,
                    'fecha_aplicacion': fecha_aplicacion.isoformat(),
                    'dosis_numero': dosis_numero,
                    'validaciones_pasadas': [
                        'Duplicado reciente',
                        'Protocolo completo mismo día',
                        'Formato de fecha',
                        'Campos requeridos'
                    ]
                },
                'status': 'success'
            }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error en aplicar_mejorado: {str(e)}")
        return Response({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}',
            'error_code': 'INTERNAL_SERVER_ERROR',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ==================================================
# 🔧 MEJORA 3: CONSTRAINT DE BASE DE DATOS
# ==================================================

SQL_CONSTRAINT_ANTI_DUPLICADOS = """
-- Crear constraint único compuesto para prevenir duplicados a nivel de BD
ALTER TABLE api_historialvacunacion
ADD CONSTRAINT unique_vaccination_per_day
UNIQUE (mascota_id, vacuna_id, fecha_aplicacion, dosis_numero);

-- Crear índice para mejorar performance de validaciones
CREATE INDEX IF NOT EXISTS idx_vaccination_lookup
ON api_historialvacunacion (mascota_id, vacuna_id, fecha_aplicacion, estado);

-- Crear índice para timeframe queries
CREATE INDEX IF NOT EXISTS idx_vaccination_recent
ON api_historialvacunacion (mascota_id, vacuna_id, creado)
WHERE estado IN ('aplicada', 'vigente');
"""

# ==================================================
# 🔧 MEJORA 4: MIDDLEWARE DE RATE LIMITING
# ==================================================

class VaccinationRateLimitMiddleware:
    """
    🛡️ Middleware para limitar la frecuencia de aplicaciones de vacunas
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si es una request de aplicación de vacuna
        if (request.method == 'POST' and
            '/api/vacunas/' in request.path and
            '/aplicar' in request.path):

            # Obtener IP y usuario
            user_id = getattr(request.user, 'id', 'anonymous')
            ip = self.get_client_ip(request)
            cache_key = f"vaccine_rate_limit:{user_id}:{ip}"

            # Verificar rate limit (máximo 5 aplicaciones por minuto)
            current_count = cache.get(cache_key, 0)
            if current_count >= 5:
                from django.http import JsonResponse
                return JsonResponse({
                    'success': False,
                    'message': 'Rate limit excedido. Máximo 5 aplicaciones por minuto.',
                    'error_code': 'RATE_LIMIT_EXCEEDED',
                    'status': 'error'
                }, status=429)

            # Incrementar contador
            cache.set(cache_key, current_count + 1, 60)  # 1 minuto

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

print("✅ MEJORAS ANTI-DUPLICADOS CARGADAS EXITOSAMENTE")
print("📋 FUNCIONES DISPONIBLES:")
print("  - prevent_duplicates (decorator)")
print("  - aplicar_mejorado (método)")
print("  - VaccinationRateLimitMiddleware (middleware)")
print("  - SQL_CONSTRAINT_ANTI_DUPLICADOS (constraint)")