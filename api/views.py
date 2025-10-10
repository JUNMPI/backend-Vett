from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from django.utils import timezone

# Imports para fechas y tiempo
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# Imports adicionales
import uuid
import re
import traceback

# Imports específicos de modelos
from .models import (
    Especialidad, Consultorio, TipoDocumento, Trabajador, Veterinario,
    Servicio, Producto, Mascota, Responsable, Cita, Usuario,
    EstadoCita, Vacuna, HistorialVacunacion, HistorialMedico,
    # 🚀 Nuevos modelos profesionales
    HorarioTrabajo, SlotTiempo, PermisoRol
)
# DiaTrabajo ya no se usa - dias_trabajo se genera dinámicamente desde HorarioTrabajo

# Imports específicos de serializers
from .serializers import (
    EspecialidadSerializer, ConsultorioSerializer, TipoDocumentoSerializer,
    TrabajadorSerializer, VeterinarioSerializer, ServicioSerializer,
    ProductoSerializer, MascotaSerializer, ResponsableSerializer,
    CitaSerializer, CustomTokenObtainPairSerializer, VacunaSerializer,
    HistorialVacunacionSerializer, HistorialMedicoSerializer, VacunasAlertaSerializer,
    # 🚀 Nuevos serializers profesionales
    HorarioTrabajoSerializer, SlotTiempoSerializer, CitaProfesionalSerializer,
    # 🔐 Serializers de permisos
    PermisoRolSerializer, PermisoRolBulkUpdateSerializer
)

# ViewSet for Especialidad
class EspecialidadViewSet(viewsets.ModelViewSet):
    # Definimos el queryset de manera explícita aquí
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

    # Método que filtra las especialidades activas
    def get_queryset(self):
        # Solo devuelve especialidades cuyo estado sea 'ACTIVO' (insensible a mayúsculas/minúsculas)
        return Especialidad.objects.all()

    @action(detail=False, methods=['get'], url_path='activos')
    def activos(self, request):
        # Devuelve solo los tipos de documento cuyo estado es 'ACTIVO'
        especialidad_activos = Especialidad.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(especialidad_activos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        especialidad = self.get_object()
        especialidad.estado = 'Inactivo'
        especialidad.save()
        return Response({'status': 'especialidad desactivada'})
    # Método para activar una especialidad
    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        especialidad = self.get_object()
        especialidad.estado = 'Activo'
        especialidad.save()
        return Response({'status': 'especialidad activada'})


    # Método para obtener todas las especialidades (activas e inactivas)
    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        # Devuelve todas las especialidades, independientemente de su estado
        especialidades = Especialidad.objects.all()
        serializer = self.get_serializer(especialidades, many=True)
        return Response(serializer.data)
    # Método para contar las especialidades
    @action(detail=False, methods=['get'], url_path='count')
    def count(self, request):
        # Contamos el número total de especialidades
        count = Especialidad.objects.count()
        # Devolvemos la respuesta en formato JSON
        return Response({'total': count})

# ViewSet for Consultorio
class ConsultorioViewSet(viewsets.ModelViewSet):
    queryset = Consultorio.objects.all()  # <- Esto es importante
    serializer_class = ConsultorioSerializer

    def get_queryset(self):
        # Solo consultorios abiertos
        return Consultorio.objects.all()

    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        consultorios = Consultorio.objects.all()
        serializer = self.get_serializer(consultorios, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='cerrar')
    def cerrar(self, request, pk=None):
        consultorio = self.get_object()
        consultorio.disponible = 'Cerrado'
        consultorio.save()
        return Response({'status': 'Consultorio cerrado'})

    @action(detail=True, methods=['patch'], url_path='abrir')
    def abrir(self, request, pk=None):
        consultorio = self.get_object()
        consultorio.disponible = 'Abierto'
        consultorio.save()
        return Response({'status': 'Consultorio abierto'})
    @action(detail=False, methods=['get'], url_path='abiertos')
    def abiertos(self, request):
        # Devuelve solo los tipos de documento cuyo estado es 'ACTIVO'
        especialidad_activos = Especialidad.objects.filter(estado__iexact='abiertos')
        serializer = self.get_serializer(especialidad_activos, many=True)
        return Response(serializer.data)


# ViewSet for TipoDocumento
class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer
    def get_queryset(self):
            # Solo devuelve tipos de documento cuyo estado sea 'ACTIVO'
        return TipoDocumento.objects.all()
    
    @action(detail=False, methods=['get'], url_path='activos')
    def activos(self, request):
        # Devuelve solo los tipos de documento cuyo estado es 'ACTIVO'
        tipos_documento_activos = TipoDocumento.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(tipos_documento_activos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        tipo_documento = self.get_object()
        tipo_documento.estado = 'INACTIVO'
        tipo_documento.save()
        return Response({'status': 'Tipo de documento desactivado'})
    # Método para activar un tipo de documento
    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        tipo_documento = self.get_object()
        tipo_documento.estado = 'Activo'
        tipo_documento.save()
        return Response({'status': 'Tipo de documento activado'})

    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        # Devuelve todos los tipos de documento, independientemente de su estado
        tipos_documento = TipoDocumento.objects.all()
        serializer = self.get_serializer(tipos_documento, many=True)
        return Response(serializer.data)




# ViewSet for Trabajador
# En api/views.py, reemplaza la clase TrabajadorViewSet existente

class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadorSerializer
    
    def get_queryset(self):
        # Por defecto devuelve todos los trabajadores (activos e inactivos)
        return Trabajador.objects.all()

    # 🆕 NUEVA ACCIÓN: Desactivar trabajador
    @action(detail=True, methods=['patch'], url_path='desactivar')
    def desactivar(self, request, pk=None):
        trabajador = self.get_object()
        trabajador.estado = 'Inactivo'
        trabajador.save()
        
        # También desactivamos el usuario asociado
        usuario = trabajador.usuario
        usuario.is_active = False
        usuario.save()
        
        return Response({'status': 'Trabajador desactivado correctamente'})

    # 🆕 NUEVA ACCIÓN: Activar trabajador
    @action(detail=True, methods=['patch'], url_path='activar')
    def activar(self, request, pk=None):
        trabajador = self.get_object()
        trabajador.estado = 'Activo'
        trabajador.save()
        
        # También activamos el usuario asociado
        usuario = trabajador.usuario
        usuario.is_active = True
        usuario.save()
        
        return Response({'status': 'Trabajador activado correctamente'})

    # 🆕 NUEVA ACCIÓN: Obtener solo trabajadores activos
    @action(detail=False, methods=['get'], url_path='activos')
    def activos(self, request):
        trabajadores_activos = Trabajador.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(trabajadores_activos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='reset-password')
    def reset_password(self, request, pk=None):
        trabajador = self.get_object()
        nueva_password = request.data.get('password')

        if not nueva_password or len(nueva_password) < 6:
            return Response({'error': 'La contraseña debe tener al menos 6 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)

        usuario = trabajador.usuario
        usuario.set_password(nueva_password)
        usuario.save()

        return Response({'mensaje': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], url_path='editar')
    def edit_trabajador(self, request, pk=None):
        trabajador = self.get_object()
        serializer = TrabajadorSerializer(trabajador, data=request.data, partial=False)

        if serializer.is_valid():
            usuario_data = serializer.validated_data.get('usuario', None)
            if usuario_data and usuario_data.get('email'):
                email = usuario_data['email']
                if Usuario.objects.filter(email=email).exclude(id=trabajador.usuario.id).exists():
                    return Response({'error': 'El correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='veterinarios')
    def veterinarios(self, request):
        # Solo veterinarios activos
        veterinarios = Trabajador.objects.filter(usuario__rol__iexact='Veterinario', estado__iexact='activo')
        serializer = self.get_serializer(veterinarios, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='count')
    def count(self, request):
        count = Trabajador.objects.count()
        return Response({'total': count})

# ViewSet for Veterinario
class VeterinarioViewSet(viewsets.ModelViewSet):
    queryset = Veterinario.objects.all()
    serializer_class = VeterinarioSerializer

    # ENDPOINT ELIMINADO: asignar-dias
    # Ya no es necesario porque dias_trabajo se genera automáticamente desde horarios_trabajo.
    # El frontend debe usar el endpoint POST /api/horarios-trabajo/ en su lugar.

    #buscar el trabajador por id de trabajador
    @action(detail=False, methods=['get'], url_path='por-trabajador/(?P<trabajador_id>[^/.]+)')
    def por_trabajador(self, request, trabajador_id=None):
        veterinario = get_object_or_404(Veterinario, trabajador__id=trabajador_id)
        serializer = self.get_serializer(veterinario)
        return Response(serializer.data)
    
# ViewSet for Service
class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

    # Filtra servicios activos por defecto y permite filtrar por categoría
    def get_queryset(self):
        queryset = Servicio.objects.all()

        # Filtro por categoría
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)

        # Filtro por estado
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset

    # Desactiva un servicio (cambia su estado a INACTIVO)
    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        servicio = self.get_object()
        servicio.estado = 'Inactivo'
        servicio.save()
        return Response({'status': 'servicio desactivado'})

    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        servicio = self.get_object()
        servicio.estado = 'Activo'
        servicio.save()
        return Response({'status': 'servicio activado'})

    # Devuelve todos los servicios, sin importar su estado
    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        servicios = Servicio.objects.all()
        serializer = self.get_serializer(servicios, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='activos')
    def activos(self, request):
        # Devuelve solo los servicios cuyo estado es 'ACTIVO'
        servicios_activos = Servicio.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(servicios_activos, many=True)
        return Response(serializer.data)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    # Devuelve todos los productos (activos e inactivos) para que los endpoints individuales funcionen
    def get_queryset(self):
        return Producto.objects.all()

    # Desactiva un producto (cambia su estado a INACTIVO)
    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        producto = self.get_object()
        producto.estado = 'Inactivo'
        producto.save()
        return Response({'status': 'producto desactivado'})

    # Activa un producto (cambia su estado a ACTIVO)
    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        producto = self.get_object()
        producto.estado = 'Activo'
        producto.save()
        return Response({'status': 'producto activado'})

    @action(detail=False, methods=['get'], url_path='activos')
    def activos(self, request):
        # Devuelve solo los productos cuyo estado es 'ACTIVO'
        productos_activos = Producto.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(productos_activos, many=True)
        return Response(serializer.data)

    # Devuelve todos los productos, sin importar su estado
    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        productos = Producto.objects.all()
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)
    # Método para contar los productos
    @action(detail=False, methods=['get'], url_path='count')
    def count(self, request):
        # Contamos el número total de productos
        count = Producto.objects.count()
        # Devolvemos la respuesta en formato JSON
        return Response({'total': count})
    
    @action(detail=False, methods=['get'], url_path='vacunas')
    def vacunas_inventario(self, request):
        """
        Endpoint adicional para obtener productos tipo vacuna
        URL: GET /api/productos/vacunas/
        """
        from django.db.models import Q
        
        productos_vacunas = Producto.objects.filter(
            Q(tipo__icontains='vacuna') |
            Q(subtipo__icontains='vacuna') |
            Q(nombre__icontains='vacuna') |
            Q(descripcion__icontains='vacuna')
        ).filter(estado__iexact='activo')
        
        search = request.query_params.get('search')
        if search:
            productos_vacunas = productos_vacunas.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search) |
                Q(proveedor__icontains=search)
            )
        
        # Sin límite - mostrar todos los productos disponibles
        
        serializer = self.get_serializer(productos_vacunas, many=True)
        return Response(serializer.data)
    
class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer

    def create(self, request, *args, **kwargs):
        """
        🛡️ CORRECCION CRITICA: Sanitización de caracteres especiales
        """
        import re
        import html

        data = request.data.copy()

        # Lista de campos de texto que necesitan sanitización
        campos_texto = ['nombreMascota', 'raza', 'color', 'observaciones']

        for campo in campos_texto:
            if campo in data and data[campo]:
                valor = str(data[campo])

                # 1. Escape HTML para prevenir XSS
                valor = html.escape(valor)

                # 2. Remover caracteres peligrosos específicos
                caracteres_peligrosos = ['<', '>', '"', "'", '&', 'script', 'javascript', 'onload', 'onerror']
                for char in caracteres_peligrosos:
                    valor = valor.replace(char, '')

                # 3. Limitar longitud (prevenir DoS)
                if len(valor) > 100:
                    valor = valor[:100]

                # 4. Validar que no sea solo espacios
                if not valor.strip():
                    return Response({
                        'error': f'Campo {campo} no puede estar vacío o contener solo espacios',
                        'error_code': 'INVALID_FIELD_VALUE'
                    }, status=status.HTTP_400_BAD_REQUEST)

                data[campo] = valor.strip()

        # Continuar con la creación normal
        request._full_data = data
        return super().create(request, *args, **kwargs)

    # Filtra mascotas activas por defecto
    @action(detail=False, methods=['get'], url_path='activas')
    def activos(self, request):
        # Devuelve solo las mascotas cuyo estado es 'ACTIVO'
        mascotas_activos = Mascota.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(mascotas_activos, many=True)
        return Response(serializer.data)
    # Desactiva una mascota (cambia su estado a INACTIVO)
    @action(detail=True, methods=['patch'],url_path='desactivar')
    def desactivar(self, request, pk=None):
        mascota = self.get_object()
        mascota.estado = 'Inactivo'
        mascota.save()
        return Response({'status': 'mascota desactivada'})
    # Método para activar una mascota
    @action(detail=True, methods=['patch'], url_path='activar')
    def activar(self, request, pk=None):
        mascota = self.get_object()
        mascota.estado = 'Activo'
        mascota.save()
        return Response({'status': 'mascota activada'})
    # Método para contar las mascotas
    @action(detail=False, methods=['get'], url_path='count')
    def count(self, request):
        # Contamos el número total de mascotas
        count = Mascota.objects.count()
        # Devolvemos la respuesta en formato JSON
        return Response({'total': count})
    
    @action(detail=True, methods=['get'], url_path='historial-vacunacion')
    def historial_vacunacion(self, request, pk=None):
        """
        🐾 ENDPOINT PARA FRONTEND: Historial de vacunación por mascota
        URL: GET /api/mascotas/{id}/historial-vacunacion/
        Devuelve historial completo con nombres de vacuna y veterinario
        """
        from .models import HistorialVacunacion
        from .serializers import HistorialVacunacionSerializer
        
        mascota = self.get_object()
        
        # Obtener historial de vacunación de esta mascota
        historial = HistorialVacunacion.objects.filter(
            mascota=mascota
        ).select_related(
            'vacuna', 'veterinario', 'veterinario__trabajador'
        ).order_by('-fecha_aplicacion')
        
        # Usar el serializer que ya tiene los campos correctos
        serializer = HistorialVacunacionSerializer(historial, many=True)
        
        return Response({
            'mascota_id': str(mascota.id),
            'mascota_nombre': mascota.nombreMascota,
            'total_vacunas': historial.count(),
            'historial': serializer.data,
            'status': 'success'
        })
    
class ResponsableViewSet(viewsets.ModelViewSet):
    queryset = Responsable.objects.all()
    serializer_class = ResponsableSerializer


class CitaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Cita y acciones personalizadas:
      - cambiar-estado
      - reprogramar
      - por-veterinario
    """
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer

    def get_queryset(self):
        """
        Filtrado automático de citas según el rol del usuario:
        - VETERINARIO: Solo ve SUS propias citas
        - ADMIN/RECEPCIONISTA: Ven TODAS las citas

        También soporta filtrado manual con query param 'veterinario_id'
        """
        user = self.request.user
        queryset = Cita.objects.all()

        # Si es veterinario, solo mostrar SUS citas
        if user.rol == 'veterinario':
            try:
                # Obtener el veterinario asociado al usuario
                veterinario = user.trabajador.veterinario
                queryset = queryset.filter(veterinario=veterinario)
            except Exception as e:
                # Si no tiene veterinario asociado, no mostrar nada
                return Cita.objects.none()

        # Filtrado adicional por query param (para admin/recepcionista)
        vet_id = self.request.query_params.get('veterinario_id')
        if vet_id and user.rol != 'veterinario':
            queryset = queryset.filter(veterinario__id=vet_id)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Crear cita con validación de slots y prevención de conflictos
        """
        from datetime import datetime, timedelta

        data = request.data
        veterinario_id = data.get('veterinario')
        fecha = data.get('fecha')
        hora = data.get('hora')
        servicio_id = data.get('servicio')

        try:
            # Validar que existan los objetos
            veterinario = Veterinario.objects.get(id=veterinario_id)
            servicio = Servicio.objects.get(id=servicio_id)
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_obj = datetime.strptime(hora, '%H:%M' if ':' in hora and len(hora) == 5 else '%H:%M:%S').time()

        except (Veterinario.DoesNotExist, Servicio.DoesNotExist):
            return Response({
                'error': 'Veterinario o Servicio no encontrado',
                'error_code': 'INVALID_REFERENCES'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'error': 'Formato de fecha u hora inválido',
                'error_code': 'INVALID_DATE_FORMAT'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Calcular duración total del servicio
        duracion_total = servicio.duracion_total_minutos()

        # Verificar conflictos con otras citas
        hora_inicio_dt = datetime.combine(fecha_obj, hora_obj)
        hora_fin_dt = hora_inicio_dt + timedelta(minutes=duracion_total)

        citas_conflicto = Cita.objects.filter(
            veterinario=veterinario,
            fecha=fecha_obj,
            estado__in=['pendiente', 'confirmada']  # Solo citas activas
        ).exclude(
            Q(hora__gte=hora_fin_dt.time()) | Q(hora__lt=hora_obj)
        )

        if citas_conflicto.exists():
            cita_conflicto = citas_conflicto.first()
            return Response({
                'error': f'El veterinario ya tiene una cita a las {cita_conflicto.hora}',
                'error_code': 'TIME_CONFLICT',
                'cita_existente': {
                    'id': str(cita_conflicto.id),
                    'hora': str(cita_conflicto.hora),
                    'mascota': cita_conflicto.mascota.nombreMascota
                }
            }, status=status.HTTP_409_CONFLICT)

        # Buscar slot correspondiente
        slot = SlotTiempo.objects.filter(
            veterinario=veterinario,
            fecha=fecha_obj,
            hora_inicio=hora_obj
        ).first()

        # Si existe slot, validar disponibilidad
        if slot:
            if not slot.disponible:
                return Response({
                    'error': 'El slot seleccionado no está disponible',
                    'error_code': 'SLOT_NOT_AVAILABLE',
                    'motivo': slot.motivo_no_disponible
                }, status=status.HTTP_400_BAD_REQUEST)

            if slot.esta_reservado_temporalmente():
                return Response({
                    'error': 'El slot está reservado temporalmente por otro usuario',
                    'error_code': 'SLOT_RESERVED',
                    'reservado_hasta': slot.reservado_hasta
                }, status=status.HTTP_409_CONFLICT)

        # Crear la cita
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            cita = serializer.save()

            # Marcar slot como ocupado si existe
            if slot:
                slot.disponible = False
                slot.motivo_no_disponible = 'ocupado'
                slot.reservado_hasta = None  # Limpiar reserva temporal
                slot.save()

            return Response({
                'mensaje': 'Cita creada exitosamente',
                'cita': serializer.data,
                'slot_ocupado': str(slot.id) if slot else None,
                'status': 'success'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        """
        PATCH /api/citas/{id}/cambiar-estado/
        Body: { "estado": "<nuevo_estado>" }
        Solo admite uno de los valores definidos en EstadoCita.ESTADO_CHOICES.

        Si se cancela una cita, libera automáticamente el slot
        """
        cita = self.get_object()
        nuevo_estado = request.data.get('estado')

        if nuevo_estado not in dict(EstadoCita.ESTADO_CHOICES).keys():
            return Response(
                {'error': f"Estado inválido: {nuevo_estado}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        estado_anterior = cita.estado
        cita.estado = nuevo_estado
        cita.save()

        # Si se cancela la cita, liberar el slot
        if nuevo_estado == EstadoCita.CANCELADA and estado_anterior != EstadoCita.CANCELADA:
            slot = SlotTiempo.objects.filter(
                veterinario=cita.veterinario,
                fecha=cita.fecha,
                hora_inicio=cita.hora
            ).first()

            if slot:
                slot.disponible = True
                slot.motivo_no_disponible = ''
                slot.save()

                return Response({
                    'status': 'estado actualizado',
                    'mensaje': 'Cita cancelada y slot liberado',
                    'slot_liberado': str(slot.id)
                }, status=status.HTTP_200_OK)

        return Response({'status': 'estado actualizado'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='reprogramar')
    def reprogramar(self, request, pk=None):
        """
        PATCH /api/citas/{id}/reprogramar/
        Body: { "fecha": "YYYY-MM-DD", "hora": "HH:MM:SS" }
        Cambia la fecha y hora y marca estado como "reprogramada".
        Libera el slot anterior y ocupa el nuevo slot.
        """
        from datetime import datetime, timedelta

        cita = self.get_object()
        nueva_fecha = request.data.get('fecha')
        nueva_hora = request.data.get('hora')

        if not nueva_fecha or not nueva_hora:
            return Response(
                {'error': 'Se requieren "fecha" y "hora" para reprogramar.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            nueva_fecha_obj = datetime.strptime(nueva_fecha, '%Y-%m-%d').date()
            nueva_hora_obj = datetime.strptime(nueva_hora, '%H:%M' if ':' in nueva_hora and len(nueva_hora) == 5 else '%H:%M:%S').time()
        except ValueError:
            return Response({
                'error': 'Formato de fecha u hora inválido',
                'error_code': 'INVALID_DATE_FORMAT'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Guardar datos antiguos para liberar slot
        fecha_anterior = cita.fecha
        hora_anterior = cita.hora

        # Calcular duración total del servicio
        servicio = cita.servicio
        duracion_total = servicio.duracion_total_minutos()

        # Verificar conflictos con otras citas en el nuevo horario
        hora_inicio_dt = datetime.combine(nueva_fecha_obj, nueva_hora_obj)
        hora_fin_dt = hora_inicio_dt + timedelta(minutes=duracion_total)

        citas_conflicto = Cita.objects.filter(
            veterinario=cita.veterinario,
            fecha=nueva_fecha_obj,
            estado__in=['pendiente', 'confirmada', 'reprogramada']
        ).exclude(
            Q(hora__gte=hora_fin_dt.time()) | Q(hora__lt=nueva_hora_obj)
        ).exclude(id=cita.id)  # Excluir la cita actual

        if citas_conflicto.exists():
            cita_conflicto = citas_conflicto.first()
            return Response({
                'error': f'El veterinario ya tiene una cita a las {cita_conflicto.hora}',
                'error_code': 'TIME_CONFLICT',
                'cita_existente': {
                    'id': str(cita_conflicto.id),
                    'hora': str(cita_conflicto.hora),
                    'mascota': cita_conflicto.mascota.nombreMascota
                }
            }, status=status.HTTP_409_CONFLICT)

        # Verificar disponibilidad del nuevo slot
        nuevo_slot = SlotTiempo.objects.filter(
            veterinario=cita.veterinario,
            fecha=nueva_fecha_obj,
            hora_inicio=nueva_hora_obj
        ).first()

        if nuevo_slot:
            if not nuevo_slot.disponible:
                return Response({
                    'error': 'El nuevo slot no está disponible',
                    'error_code': 'SLOT_NOT_AVAILABLE',
                    'motivo': nuevo_slot.motivo_no_disponible
                }, status=status.HTTP_400_BAD_REQUEST)

        # 1. Liberar slot anterior
        slot_anterior = SlotTiempo.objects.filter(
            veterinario=cita.veterinario,
            fecha=fecha_anterior,
            hora_inicio=hora_anterior
        ).first()

        if slot_anterior:
            slot_anterior.disponible = True
            slot_anterior.motivo_no_disponible = ''
            slot_anterior.save()

        # 2. Actualizar la cita
        cita.fecha = nueva_fecha
        cita.hora = nueva_hora
        cita.estado = EstadoCita.REPROGRAMADA
        cita.save()

        # 3. Marcar nuevo slot como ocupado
        if nuevo_slot:
            nuevo_slot.disponible = False
            nuevo_slot.motivo_no_disponible = 'ocupado'
            nuevo_slot.reservado_hasta = None  # Limpiar reserva temporal si existe
            nuevo_slot.save()

        return Response({
            'status': 'cita reprogramada',
            'mensaje': 'Cita reprogramada exitosamente',
            'slot_anterior_liberado': str(slot_anterior.id) if slot_anterior else None,
            'nuevo_slot_ocupado': str(nuevo_slot.id) if nuevo_slot else None,
            'nueva_fecha': nueva_fecha,
            'nueva_hora': nueva_hora
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='por-veterinario/(?P<veterinario_id>[^/.]+)')
    def por_veterinario(self, request, veterinario_id=None):
        """
        GET /api/citas/por-veterinario/{veterinario_id}/
        Devuelve solo las citas asignadas al veterinario con ID {veterinario_id}.
        """
        citas_vet = Cita.objects.filter(veterinario__id=veterinario_id)
        serializer = self.get_serializer(citas_vet, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='mi-calendario')
    def mi_calendario(self, request):
        """
        GET /api/citas/mi-calendario/?fecha=2025-10-06

        Endpoint para VETERINARIOS: Ver sus propias citas del día.
        Si no se especifica fecha, muestra las del día actual.

        Query params:
        - fecha: YYYY-MM-DD (opcional, default: hoy)

        Retorna citas ordenadas por hora con información completa.
        NOTA: Detecta automáticamente el veterinario del usuario autenticado.
        """
        from datetime import date as date_class

        # Obtener fecha del query param o usar hoy
        fecha_str = request.query_params.get('fecha')
        if fecha_str:
            try:
                fecha = date_class.fromisoformat(fecha_str)
            except ValueError:
                return Response({
                    'error': 'Formato de fecha inválido. Use YYYY-MM-DD',
                    'error_code': 'INVALID_DATE_FORMAT'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            fecha = date_class.today()

        # Obtener veterinario del usuario autenticado
        user = request.user

        try:
            # Intentar obtener el veterinario asociado al usuario
            veterinario = user.trabajador.veterinario
        except Exception as e:
            return Response({
                'error': 'Usuario no tiene un veterinario asociado',
                'error_code': 'NO_VETERINARIO_ASOCIADO',
                'detalle': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        # Obtener citas del veterinario para esa fecha
        citas = Cita.objects.filter(
            veterinario=veterinario,
            fecha=fecha
        ).exclude(
            estado='cancelada'
        ).select_related(
            'mascota', 'servicio', 'responsable'
        ).order_by('hora')

        # Construir respuesta con información detallada
        citas_data = []
        for cita in citas:
            citas_data.append({
                'id': str(cita.id),
                'hora': str(cita.hora),
                'estado': cita.estado,
                'mascota': {
                    'id': str(cita.mascota.id),
                    'nombre': cita.mascota.nombreMascota,
                    'especie': cita.mascota.especie,
                    'raza': cita.mascota.raza
                },
                'responsable': {
                    'id': str(cita.responsable.id),
                    'nombre': f"{cita.responsable.nombres} {cita.responsable.apellidos}",
                    'telefono': cita.responsable.telefono
                },
                'servicio': {
                    'id': str(cita.servicio.id),
                    'nombre': cita.servicio.nombre,
                    'categoria': cita.servicio.categoria,
                    'duracion_minutos': cita.servicio.duracion_total_minutos(),
                    'precio': str(cita.servicio.precio)
                },
                'notas': cita.notas or ''
            })

        return Response({
            'fecha': str(fecha),
            'veterinario': {
                'id': str(veterinario.id),
                'nombre': f"{veterinario.trabajador.nombres} {veterinario.trabajador.apellidos}"
            },
            'total_citas': len(citas_data),
            'citas': citas_data,
            'status': 'success'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='calendario-recepcion')
    def calendario_recepcion(self, request):
        """
        GET /api/citas/calendario-recepcion/?fecha=2025-10-06

        Endpoint para RECEPCIONISTAS: Ver todas las citas de TODOS los veterinarios del día.
        Si no se especifica fecha, muestra las del día actual.

        Query params:
        - fecha: YYYY-MM-DD (opcional, default: hoy)
        - veterinario: UUID (opcional, filtrar por veterinario específico)

        Retorna citas agrupadas por veterinario, ordenadas por hora.
        """
        from datetime import date as date_class

        # Obtener fecha del query param o usar hoy
        fecha_str = request.query_params.get('fecha')
        if fecha_str:
            try:
                fecha = date_class.fromisoformat(fecha_str)
            except ValueError:
                return Response({
                    'error': 'Formato de fecha inválido. Use YYYY-MM-DD',
                    'error_code': 'INVALID_DATE_FORMAT'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            fecha = date_class.today()

        # Filtro opcional por veterinario
        veterinario_id = request.query_params.get('veterinario')

        # Base query
        citas_query = Cita.objects.filter(
            fecha=fecha
        ).exclude(
            estado='cancelada'
        ).select_related(
            'veterinario', 'veterinario__trabajador', 'mascota', 'servicio', 'responsable'
        ).order_by('veterinario', 'hora')

        # Aplicar filtro de veterinario si existe
        if veterinario_id:
            citas_query = citas_query.filter(veterinario_id=veterinario_id)

        citas = citas_query

        # Agrupar por veterinario
        veterinarios_dict = {}
        for cita in citas:
            vet_id = str(cita.veterinario.id)

            if vet_id not in veterinarios_dict:
                veterinarios_dict[vet_id] = {
                    'veterinario': {
                        'id': vet_id,
                        'nombre': f"{cita.veterinario.trabajador.nombres} {cita.veterinario.trabajador.apellidos}",
                        'especialidad': cita.veterinario.especialidad
                    },
                    'citas': []
                }

            veterinarios_dict[vet_id]['citas'].append({
                'id': str(cita.id),
                'hora': str(cita.hora),
                'estado': cita.estado,
                'mascota': {
                    'id': str(cita.mascota.id),
                    'nombre': cita.mascota.nombreMascota,
                    'especie': cita.mascota.especie,
                    'raza': cita.mascota.raza
                },
                'responsable': {
                    'id': str(cita.responsable.id),
                    'nombre': f"{cita.responsable.nombres} {cita.responsable.apellidos}",
                    'telefono': cita.responsable.telefono
                },
                'servicio': {
                    'id': str(cita.servicio.id),
                    'nombre': cita.servicio.nombre,
                    'categoria': cita.servicio.categoria,
                    'duracion_minutos': cita.servicio.duracion_total_minutos(),
                    'precio': str(cita.servicio.precio)
                },
                'notas': cita.notas or ''
            })

        # Convertir dict a lista
        veterinarios_lista = list(veterinarios_dict.values())

        # Calcular totales
        total_citas = sum(len(v['citas']) for v in veterinarios_lista)
        total_veterinarios = len(veterinarios_lista)

        return Response({
            'fecha': str(fecha),
            'total_veterinarios': total_veterinarios,
            'total_citas': total_citas,
            'veterinarios': veterinarios_lista,
            'status': 'success'
        }, status=status.HTTP_200_OK)

    # 🛒 NUEVOS ENDPOINTS PARA SERVICIOS CATEGORIZADOS

    @action(detail=True, methods=['get'], url_path='modal-completar')
    def modal_completar(self, request, pk=None):
        """
        GET /api/citas/{id}/modal-completar/
        Obtiene la estructura del modal para completar cita según categoría
        """
        cita = self.get_object()
        categoria = cita.servicio.categoria

        # Estructura base de respuesta
        response_data = {
            'cita_id': cita.id,
            'categoria': categoria,
            'servicio_nombre': cita.servicio.nombre,
            'mascota_nombre': cita.mascota.nombreMascota,
            'precio_base': cita.servicio.precio,
            'permite_adicionales': cita.servicio.permite_servicios_adicionales(),
            'precio_fijo': cita.servicio.es_precio_fijo()
        }

        # Agregar campos específicos según categoría
        if categoria == 'CONSULTA':
            response_data.update({
                'servicios_disponibles': ServicioSerializer(
                    Servicio.objects.filter(categoria__in=['CONSULTA', 'CIRUGIA'], estado='Activo').exclude(id=cita.servicio.id),
                    many=True
                ).data,
                'productos_disponibles': ProductoSerializer(
                    Producto.objects.filter(estado='Activo'),
                    many=True
                ).data
            })
        elif categoria == 'BAÑADO':
            response_data.update({
                'tipos_pelaje': [
                    'Corto', 'Mediano', 'Largo', 'Rizado', 'Doble capa'
                ]
            })
        elif categoria == 'VACUNACION':
            from datetime import datetime, timedelta
            response_data.update({
                'vacunas_disponibles': VacunaSerializer(
                    Vacuna.objects.filter(estado='Activo'),
                    many=True
                ).data,
                'proxima_cita_sugerida': (datetime.now() + timedelta(days=30)).date()
            })

        return Response(response_data)

    @action(detail=True, methods=['post'], url_path='completar')
    def completar_cita(self, request, pk=None):
        """
        POST /api/citas/{id}/completar/
        Completa la cita con información específica según categoría
        """
        cita = self.get_object()
        data = request.data.copy()
        data['cita'] = cita.id

        try:
            with transaction.atomic():
                # Crear o actualizar el detalle de la cita
                detalle, created = DetalleCompletarCita.objects.get_or_create(
                    cita=cita,
                    defaults=data
                )

                if not created:
                    # Actualizar detalle existente
                    serializer = DetalleCompletarCitaSerializer(detalle, data=data, partial=True)
                else:
                    # Nuevo detalle
                    serializer = DetalleCompletarCitaSerializer(detalle, data=data, partial=True)

                if serializer.is_valid():
                    detalle = serializer.save()
                    detalle.completado = True
                    detalle.completado_en = timezone.now()

                    # Asignar veterinario si está disponible
                    veterinario_id = request.data.get('veterinario_id')
                    if veterinario_id:
                        try:
                            veterinario = Veterinario.objects.get(id=veterinario_id)
                            detalle.completado_por = veterinario
                        except Veterinario.DoesNotExist:
                            pass

                    detalle.save()

                    # Calcular totales
                    detalle.calcular_totales()

                    # Cambiar estado de la cita
                    cita.estado = 'COMPLETADA'
                    cita.save()

                    return Response({
                        'mensaje': 'Cita completada exitosamente',
                        'detalle': DetalleCompletarCitaSerializer(detalle).data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'error': f'Error al completar la cita: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='agregar-servicio')
    def agregar_servicio(self, request, pk=None):
        """
        POST /api/citas/{id}/agregar-servicio/
        Agrega un servicio o producto adicional a la cita
        """
        cita = self.get_object()

        if not cita.servicio.permite_servicios_adicionales():
            return Response({
                'error': 'Este tipo de servicio no permite agregar servicios adicionales'
            }, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['cita'] = cita.id

        serializer = ServicioAdicionalSerializer(data=data)
        if serializer.is_valid():
            servicio_adicional = serializer.save()

            # Actualizar totales del detalle si existe
            if hasattr(cita, 'detalle'):
                cita.detalle.calcular_totales()

            return Response({
                'mensaje': 'Servicio adicional agregado exitosamente',
                'servicio_adicional': ServicioAdicionalSerializer(servicio_adicional).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='resumen-total')
    def resumen_total(self, request, pk=None):
        """
        GET /api/citas/{id}/resumen-total/
        Obtiene resumen de totales calculados
        """
        cita = self.get_object()

        precio_base = cita.servicio.precio
        servicios_adicionales = cita.servicios_adicionales.all()

        subtotal_servicios = sum([
            item.subtotal for item in servicios_adicionales if item.servicio
        ])
        subtotal_productos = sum([
            item.subtotal for item in servicios_adicionales if item.producto
        ])
        total_final = precio_base + subtotal_servicios + subtotal_productos

        return Response({
            'precio_base': precio_base,
            'subtotal_servicios': subtotal_servicios,
            'subtotal_productos': subtotal_productos,
            'total_final': total_final,
            'servicios_adicionales': ServicioAdicionalSerializer(servicios_adicionales, many=True).data
        })


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class RegistrarTrabajadorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TrabajadorSerializer(data=request.data)
        if serializer.is_valid():
            trabajador = serializer.save()
            return Response({
                'mensaje': 'Trabajador registrado correctamente.',
                'trabajador_id': str(trabajador.id)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🐾 VIEWSETS SISTEMA DE VACUNACIÓN

class VacunaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión del catálogo de vacunas
    """
    queryset = Vacuna.objects.all()
    serializer_class = VacunaSerializer
    
    def get_queryset(self):
        queryset = Vacuna.objects.all()
        
        # Filtro por estado
        estado = self.request.query_params.get('estado')
        if estado and estado != 'todas':
            queryset = queryset.filter(estado__iexact=estado)
        
        # Filtro de búsqueda
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(enfermedad_previene__icontains=search) |
                Q(especies__icontains=search)
            )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """Listado con estadísticas como especifica el frontend"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Estadísticas para el frontend
        total = Vacuna.objects.count()
        activas = Vacuna.objects.filter(estado='Activo').count()
        inactivas = Vacuna.objects.filter(estado='Inactivo').count()
        obligatorias = Vacuna.objects.filter(es_obligatoria=True).count()
        
        return Response({
            'data': serializer.data,
            'estadisticas': {
                'total': total,
                'activas': activas, 
                'inactivas': inactivas,
                'obligatorias': obligatorias
            },
            'message': 'Vacunas obtenidas exitosamente',
            'status': 'success'
        })
    
    def create(self, request, *args, **kwargs):
        """Crear con formato de respuesta específico"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            vacuna = serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'Vacuna creada exitosamente',
                'status': 'success'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'data': None,
            'message': 'Error al crear vacuna',
            'errors': serializer.errors,
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='activas')
    def activas(self, request):
        """Obtener solo vacunas activas"""
        vacunas_activas = Vacuna.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(vacunas_activas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='por-especie/(?P<especie>[^/.]+)')
    def por_especie(self, request, especie=None):
        """Obtener vacunas por especie"""
        vacunas = Vacuna.objects.filter(
            especies__icontains=especie.title(),
            estado__iexact='activo'
        )
        serializer = self.get_serializer(vacunas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='obligatorias')
    def obligatorias(self, request):
        """Obtener solo vacunas obligatorias"""
        vacunas_obligatorias = Vacuna.objects.filter(
            es_obligatoria=True,
            estado__iexact='activo'
        )
        serializer = self.get_serializer(vacunas_obligatorias, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        """Desactivar vacuna"""
        vacuna = self.get_object()
        vacuna.estado = 'Inactivo'
        vacuna.save()
        return Response({'status': 'vacuna desactivada'})
    
    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        """Activar vacuna"""
        vacuna = self.get_object()
        vacuna.estado = 'Activo'
        vacuna.save()
        return Response({'status': 'vacuna activada'})
    
    @action(detail=True, methods=['patch'], url_path='update-estado')
    def update_estado(self, request, pk=None):
        """
        Actualizar solo el estado de una vacuna (Activo/Inactivo)
        URL: PATCH /api/vacunas/{id}/update-estado/
        Body: {"estado": "Activo"} o {"estado": "Inactivo"}
        """
        vacuna = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in ['Activo', 'Inactivo']:
            return Response(
                {'error': 'Estado debe ser "Activo" o "Inactivo"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        vacuna.estado = nuevo_estado
        vacuna.save()
        
        serializer = self.get_serializer(vacuna)
        return Response({
            'status': f'vacuna {nuevo_estado.lower()}ada',
            'vacuna': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='por-especie/(?P<especie>[^/.]+)')
    def por_especie(self, request, especie=None):
        """
        Obtener vacunas filtradas por especie
        URL: GET /api/vacunas/por-especie/Perro/
        """
        vacunas = Vacuna.objects.filter(
            especies__contains=[especie],
            estado__iexact='activo'
        ).order_by('nombre')
        
        serializer = self.get_serializer(vacunas, many=True)
        return Response({
            'data': serializer.data,
            'especie': especie,
            'total': vacunas.count(),
            'message': f'Vacunas para {especie} obtenidas exitosamente',
            'status': 'success'
        })

    @action(detail=False, methods=['get'], url_path='productos-vacunas')
    def productos_vacunas(self, request):
        """
        Obtener solo productos que sean vacunas del inventario
        URL: GET /api/vacunas/productos-vacunas/
        Query params: ?search=nombre (opcional)
        """
        from django.db.models import Q
        
        # Filtrar productos que contengan "vacuna" en nombre, tipo o subtipo
        productos = Producto.objects.filter(
            Q(tipo__icontains='vacuna') |
            Q(subtipo__icontains='vacuna') |
            Q(nombre__icontains='vacuna')
        ).filter(estado__iexact='activo')
        
        # Búsqueda opcional por nombre
        search = request.query_params.get('search')
        if search:
            productos = productos.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        
        # Sin límite - mostrar todos los productos disponibles
        
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='cambiar-estado')
    def cambiar_estado_vacuna(self, request, pk=None):
        """
        Endpoint específico para cambiar estado como especifica el frontend
        URL: POST /api/vacunas/{id}/cambiar-estado/
        """
        vacuna = self.get_object()
        nuevo_estado = 'Inactivo' if vacuna.estado == 'Activo' else 'Activo'
        vacuna.estado = nuevo_estado
        vacuna.save()
        
        serializer = self.get_serializer(vacuna)
        return Response({
            'data': serializer.data,
            'message': f'Estado cambiado a {nuevo_estado}',
            'status': 'success'
        })
    
    @action(detail=True, methods=['post'], url_path='aplicar-protocolo-completo')
    def aplicar_protocolo_completo(self, request, pk=None):
        """
        🎯 NUEVO ENDPOINT: Aplicar protocolo completo de vacuna en una sola operación
        URL: POST /api/vacunas/{id}/aplicar-protocolo-completo/
        Body: {
            "mascota_id": "uuid",
            "fecha_aplicacion": "2025-01-15",
            "veterinario_id": "uuid",
            "observaciones": "Protocolo completo aplicado",
            "lote": "ABC123",
            "dosis_aplicadas": 2  // Opcional: especificar cuántas dosis se aplicaron
        }
        """
        try:
            vacuna = self.get_object()
            data = request.data
            
            # Validaciones básicas
            campos_requeridos = ['mascota_id', 'fecha_aplicacion', 'veterinario_id']
            for campo in campos_requeridos:
                if campo not in data or not data[campo]:
                    return Response({
                        'success': False,
                        'message': f'Campo requerido faltante: {campo}',
                        'error_code': 'MISSING_REQUIRED_FIELD',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            from datetime import date as date_class
            fecha_aplicacion = date_class.fromisoformat(data['fecha_aplicacion'])
            
            # Validar fecha no futura
            if fecha_aplicacion > date_class.today():
                return Response({
                    'success': False,
                    'message': f'Fecha de aplicación no puede ser futura: {fecha_aplicacion}',
                    'error_code': 'FUTURE_APPLICATION_DATE',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Determinar cuántas dosis se aplicaron
            dosis_aplicadas = data.get('dosis_aplicadas', vacuna.dosis_total)
            
            # Validar que no exceda el protocolo
            if dosis_aplicadas > vacuna.dosis_total:
                dosis_aplicadas = vacuna.dosis_total
            
            # Obtener veterinario
            try:
                veterinario = Veterinario.objects.get(id=data['veterinario_id'])
            except Veterinario.DoesNotExist:
                return Response({
                    'success': False,
                    'message': f'Veterinario no encontrado: {data["veterinario_id"]}',
                    'error_code': 'VETERINARIAN_NOT_FOUND',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear un solo registro que represente el protocolo completo
            from datetime import timedelta
            from dateutil.relativedelta import relativedelta
            
            observaciones_protocolo = data.get('observaciones', '') + f' (Protocolo completo: {dosis_aplicadas} dosis aplicadas)'
            
            # Calcular próxima fecha (refuerzo anual)
            proxima_fecha = fecha_aplicacion + relativedelta(months=vacuna.frecuencia_meses)
            
            # Crear registro único
            historial_record = HistorialVacunacion.objects.create(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                fecha_aplicacion=fecha_aplicacion,
                proxima_fecha=proxima_fecha,
                veterinario=veterinario,
                lote=data.get('lote', ''),
                laboratorio=data.get('laboratorio', ''),
                dosis_numero=dosis_aplicadas,  # Número total de dosis aplicadas
                observaciones=observaciones_protocolo,
                estado='aplicada'  # 🆕 Siempre aplicada al crear, el serializer calculará dinámicamente
            )
            
            return Response({
                'success': True,
                'message': f'Protocolo completo de {vacuna.nombre} aplicado correctamente',
                'data': {
                    'historial_id': str(historial_record.id),
                    'dosis_aplicadas': dosis_aplicadas,
                    'protocolo_completo': True,
                    'proxima_fecha': proxima_fecha.isoformat(),
                    'mensaje_usuario': f'Protocolo completo aplicado ({dosis_aplicadas} dosis). Próximo refuerzo en {vacuna.frecuencia_meses} meses',
                    'protocolo_info': {
                        'dosis_aplicadas': dosis_aplicadas,
                        'dosis_total_protocolo': vacuna.dosis_total,
                        'es_protocolo_completo': True,
                        'proxima_accion': 'refuerzo_anual'
                    }
                },
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error aplicando protocolo completo: {str(e)}',
                'error_code': 'PROTOCOL_APPLICATION_ERROR',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'], url_path='aplicar')
    @transaction.atomic
    def aplicar(self, request, pk=None):
        """
        🎯 ENDPOINT PRINCIPAL: Aplicar vacuna con cálculo automático inteligente
        URL: POST /api/vacunas/{id}/aplicar/
        Body: {
            "mascota_id": "uuid",
            "fecha_aplicacion": "2025-01-15",
            "dosis_numero": 1,                    // Opcional: número de dosis específica
            "veterinario_id": "uuid",
            "observaciones": "",
            "lote": "ABC123",
            "protocolo_completo": false,          // NUEVO: true = protocolo completo en una sola aplicación
            "dosis_aplicadas": 2                  // NUEVO: cuántas dosis del protocolo se aplicaron
        }
        """
        try:
            # DEBUGGING ESPECIFICO SOLICITADO POR FRONTEND
            print("DEBUGGING DOSIS RECIBIDO:")
            print("- dosis_numero:", request.data.get('dosis_numero'))
            print("- tipo dosis_numero:", type(request.data.get('dosis_numero')))
            print("- aplicar_protocolo_completo:", request.data.get('aplicar_protocolo_completo'))
            print("- datos completos:", request.data)

            # Verificar si la validación está fallando en caso específico
            if request.data.get('dosis_numero') == 9:
                print("CASO ESPECIFICO DETECTADO: Dosis 9 de 10")

            # 🛡️ CORRECCION CRITICA: Manejo seguro de vacunas inexistentes
            try:
                vacuna = self.get_object()  # Obtener vacuna por ID de la URL
            except Vacuna.DoesNotExist:
                return Response({
                    'success': False,
                    'message': f'Vacuna no encontrada con ID: {pk}',
                    'error_code': 'VACCINE_NOT_FOUND',
                    'status': 'error'
                }, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({
                    'success': False,
                    'message': f'Error al obtener vacuna: {str(e)}',
                    'error_code': 'VACCINE_LOOKUP_ERROR',
                    'status': 'error'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            data = request.data
            
            # DEBUG: Validar que la vacuna existe y tiene datos correctos
            if not vacuna:
                return Response({
                    'success': False,
                    'message': f'Vacuna no encontrada con ID: {pk}',
                    'error_code': 'VACCINE_NOT_FOUND',
                    'status': 'error'
                }, status=status.HTTP_404_NOT_FOUND)
                
            if not hasattr(vacuna, 'nombre') or not vacuna.nombre:
                return Response({
                    'success': False,
                    'message': f'Vacuna con ID {pk} no tiene nombre válido',
                    'error_code': 'INVALID_VACCINE_DATA',
                    'status': 'error'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # 🛡️ VALIDACIONES DE ENTRADA ROBUSTAS
            # Validar campos requeridos
            campos_requeridos = ['mascota_id', 'fecha_aplicacion', 'veterinario_id']
            for campo in campos_requeridos:
                if campo not in data or not data[campo]:
                    return Response({
                        'success': False,
                        'message': f'Campo requerido faltante: {campo}',
                        'error_code': 'MISSING_REQUIRED_FIELD',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que IDs sean válidos UUIDs
            import uuid
            try:
                uuid.UUID(str(data['mascota_id']))
                uuid.UUID(str(data['veterinario_id']))
            except ValueError:
                return Response({
                    'success': False,
                    'message': 'IDs inválidos (deben ser UUIDs válidos)',
                    'error_code': 'INVALID_UUID_FORMAT',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # ⭐ NUEVA LÓGICA: Detectar si es protocolo completo o dosis individual
            es_protocolo_completo = data.get('protocolo_completo', False) or data.get('aplicar_protocolo_completo', False)
            
            if es_protocolo_completo:
                # 🎯 MODO PROTOCOLO COMPLETO
                return self._aplicar_protocolo_completo_integrado(vacuna, data)
            else:
                # 🎯 MODO DOSIS INDIVIDUAL (lógica existente)
                return self._aplicar_dosis_individual(vacuna, data)
        
        except ValidationError as ve:
            return Response({
                'success': False,
                'message': f'Datos invalidos: {str(ve)}',
                'error_code': 'VALIDATION_ERROR',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({
                'success': False,
                'message': f'Datos invalidos: {str(ve)}',
                'error_code': 'VALIDATION_ERROR',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log del error para debugging
            print(f"ERROR INESPERADO en aplicar vacuna: {str(e)}")
            return Response({
                'success': False,
                'message': 'Error interno del servidor',
                'error_code': 'INTERNAL_SERVER_ERROR',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _aplicar_protocolo_completo_integrado(self, vacuna, data):
        """Aplicar protocolo completo dentro del endpoint principal"""
        try:
            from datetime import date as date_class
            from dateutil.relativedelta import relativedelta

            fecha_aplicacion = date_class.fromisoformat(data['fecha_aplicacion'])

            # Validar fecha no futura
            if fecha_aplicacion > date_class.today():
                return Response({
                    'success': False,
                    'message': f'Fecha de aplicación no puede ser futura: {fecha_aplicacion}',
                    'error_code': 'FUTURE_APPLICATION_DATE',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 🛡️ VALIDACIÓN ANTI-DUPLICADOS PARA PROTOCOLO COMPLETO
            # Verificar si ya existe un protocolo completo de esta vacuna para esta mascota
            protocolos_existentes = HistorialVacunacion.objects.filter(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                dosis_numero=vacuna.dosis_total,  # Protocolo completo siempre usa dosis_total
                estado__in=['aplicada', 'vigente', 'completado']
            )

            if protocolos_existentes.exists():
                # Verificar si hay duplicado exacto por fecha
                protocolo_mismo_dia = protocolos_existentes.filter(fecha_aplicacion=fecha_aplicacion)
                if protocolo_mismo_dia.exists():
                    return Response({
                        'success': False,
                        'message': f'🚨 Protocolo completo duplicado: Ya existe un protocolo completo de {vacuna.nombre} para esta mascota en la fecha {fecha_aplicacion}',
                        'error_code': 'DUPLICATE_COMPLETE_PROTOCOL',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Si hay protocolos anteriores, verificar si realmente necesita uno nuevo
                return Response({
                    'success': False,
                    'message': f'⚠️ Protocolo existente: Esta mascota ya tiene un protocolo completo de {vacuna.nombre}. ¿Desea aplicar un refuerzo en su lugar?',
                    'error_code': 'EXISTING_COMPLETE_PROTOCOL',
                    'data': {
                        'protocolo_existente': True,
                        'sugerencia': 'Usar dosis individual para refuerzo'
                    },
                    'status': 'warning'
                }, status=status.HTTP_409_CONFLICT)

            # Determinar cuántas dosis se aplicaron
            dosis_aplicadas = data.get('dosis_aplicadas', vacuna.dosis_total)
            
            # Validar que no exceda el protocolo
            if dosis_aplicadas > vacuna.dosis_total:
                dosis_aplicadas = vacuna.dosis_total
            
            # Obtener veterinario
            try:
                veterinario = Veterinario.objects.get(id=data['veterinario_id'])
            except Veterinario.DoesNotExist:
                return Response({
                    'success': False,
                    'message': f'Veterinario no encontrado: {data["veterinario_id"]}',
                    'error_code': 'VETERINARIAN_NOT_FOUND',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear observaciones específicas para protocolo completo
            observaciones_base = data.get('observaciones', '')
            observaciones_protocolo = f'{observaciones_base} (Protocolo completo: {dosis_aplicadas} dosis aplicadas)'.strip()
            
            # Calcular próxima fecha (refuerzo anual)
            proxima_fecha = fecha_aplicacion + relativedelta(months=vacuna.frecuencia_meses)
            
            # Crear registro único que representa el protocolo completo
            historial_record = HistorialVacunacion.objects.create(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                fecha_aplicacion=fecha_aplicacion,
                proxima_fecha=proxima_fecha,
                veterinario=veterinario,
                lote=data.get('lote', ''),
                laboratorio=data.get('laboratorio', ''),
                dosis_numero=vacuna.dosis_total,  # CORREGIDO: Usar dosis_total de la vacuna
                observaciones=observaciones_protocolo,
                estado='aplicada'  # 🆕 Siempre aplicada al crear, el serializer calculará dinámicamente
            )
            
            return Response({
                'success': True,
                'message': f'Protocolo completo de {vacuna.nombre} aplicado correctamente',
                'data': {
                    'historial_id': str(historial_record.id),
                    'dosis_aplicadas': dosis_aplicadas,
                    'protocolo_completo': True,
                    'proxima_fecha': proxima_fecha.isoformat(),
                    'mensaje_usuario': f'Protocolo completo aplicado ({dosis_aplicadas} dosis). Próximo refuerzo en {vacuna.frecuencia_meses} meses',
                    'protocolo_info': {
                        'dosis_aplicadas': dosis_aplicadas,
                        'dosis_total_protocolo': vacuna.dosis_total,
                        'es_protocolo_completo': True,
                        'proxima_accion': 'refuerzo_anual'
                    }
                },
                'status': 'success'
            })

        except Exception as e:
            # Log detallado del error para debugging
            print(f"ERROR EN PROTOCOLO COMPLETO: {str(e)}")
            print(f"TIPO ERROR: {type(e)}")
            import traceback
            print(f"TRACEBACK: {traceback.format_exc()}")
            return Response({
                'success': False,
                'message': f'Error aplicando protocolo completo: {str(e)}',
                'error_code': 'PROTOCOL_APPLICATION_ERROR',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _aplicar_dosis_individual(self, vacuna, data):
        """Aplicar dosis individual (lógica existente)"""
        try:
            from datetime import date
            from dateutil.relativedelta import relativedelta
            from datetime import timedelta
            
            # 🧠 LÓGICA EXISTENTE PARA DOSIS INDIVIDUALES
            fecha_aplicacion = date.fromisoformat(data['fecha_aplicacion'])
            
            # ⭐ NUEVA VALIDACIÓN: Fecha no puede ser futura
            if fecha_aplicacion > date.today():
                return Response({
                    'success': False,
                    'message': f'Fecha de aplicación no puede ser futura: {fecha_aplicacion}. Debe ser hoy o anterior.',
                    'error_code': 'FUTURE_APPLICATION_DATE',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar fecha no sea extremadamente antigua (>10 años atrás) 
            from datetime import timedelta
            if fecha_aplicacion < date.today() - timedelta(days=3650):
                return Response({
                    'success': False,
                    'message': f'Fecha muy antigua: {fecha_aplicacion}. Máximo 10 años atrás.',
                    'error_code': 'DATE_TOO_OLD',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 🔒 VALIDACIONES CRÍTICAS PREVIAS
            if vacuna.dosis_total <= 0:
                raise ValueError(f"dosis_total inválida: {vacuna.dosis_total}")
            if vacuna.frecuencia_meses <= 0:
                raise ValueError(f"frecuencia_meses inválida: {vacuna.frecuencia_meses}")
            if vacuna.dosis_total > 1 and vacuna.intervalo_dosis_semanas <= 0:
                raise ValueError(f"intervalo_dosis_semanas inválido: {vacuna.intervalo_dosis_semanas}")
            if vacuna.max_dias_atraso <= 0:
                raise ValueError(f"max_dias_atraso inválido: {vacuna.max_dias_atraso}")
            
            # 1. OBTENER HISTORIAL Y CONTEXTO
            historial_previo_query = HistorialVacunacion.objects.filter(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                estado__in=['aplicada', 'vigente', 'completado']
            ).order_by('fecha_aplicacion')
            
            historial_count = historial_previo_query.count()
            
            # 🔧 FIX: Usar dosis_numero enviado por frontend, con manejo robusto
            dosis_numero_raw = data.get('dosis_numero')
            
            # 🛡️ MANEJO ROBUSTO DE DOSIS_NUMERO (para casos edge del frontend)
            if dosis_numero_raw is None or dosis_numero_raw == '':
                # Si no viene dosis_numero, calcular automáticamente
                dosis_numero_frontend = historial_count + 1
            else:
                # Convertir a entero de forma segura
                try:
                    dosis_numero_frontend = int(dosis_numero_raw)
                except (ValueError, TypeError):
                    return Response({
                        'success': False,
                        'message': f'Número de dosis inválido: "{dosis_numero_raw}". Debe ser un número entero.',
                        'error_code': 'INVALID_DOSE_FORMAT',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que sea positivo
            if dosis_numero_frontend <= 0:
                return Response({
                    'success': False,
                    'message': f'Número de dosis inválido: {dosis_numero_frontend}. Debe ser mayor a 0.',
                    'error_code': 'INVALID_DOSE_NUMBER',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if dosis_numero_frontend > 50:  # Límite médicamente razonable
                return Response({
                    'success': False,
                    'message': f'Número de dosis excesivo: {dosis_numero_frontend}. Máximo permitido: 50.',
                    'error_code': 'DOSE_NUMBER_EXCEEDED',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 🛡️ CORRECCION CRITICA: Validación ESTRICTA de límites de protocolo
            dosis_maxima_protocolo = vacuna.dosis_total

            # DEBUGGING ADICIONAL PARA CASO ESPECIFICO
            print(f"VALIDACION DE DOSIS:")
            print(f"- dosis_numero_frontend: {dosis_numero_frontend}")
            print(f"- dosis_maxima_protocolo (vacuna.dosis_total): {dosis_maxima_protocolo}")
            print(f"- vacuna.nombre: {vacuna.nombre}")
            print(f"- Validacion: {dosis_numero_frontend} > {dosis_maxima_protocolo} = {dosis_numero_frontend > dosis_maxima_protocolo}")

            # 1. Validar que la dosis no exceda el protocolo de la vacuna
            if dosis_numero_frontend > dosis_maxima_protocolo:
                return Response({
                    'success': False,
                    'message': f'ERROR: Dosis inválida: Se intentó aplicar dosis {dosis_numero_frontend} pero el protocolo de {vacuna.nombre} solo requiere {dosis_maxima_protocolo} dosis máximo.',
                    'error_code': 'PROTOCOL_DOSE_EXCEEDED',
                    'debug_info': {
                        'dosis_solicitada': dosis_numero_frontend,
                        'dosis_maxima_protocolo': dosis_maxima_protocolo,
                        'vacuna_nombre': vacuna.nombre
                    },
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 2. Validar límite absoluto de seguridad - CORREGIDO: Usar dosis_total de la vacuna
            # Solo aplicar límite si excede AMPLIAMENTE el protocolo de la vacuna
            limite_seguridad_absoluto = max(dosis_maxima_protocolo, 5)  # Al menos 5, o el protocolo de la vacuna

            if dosis_numero_frontend > limite_seguridad_absoluto and dosis_numero_frontend > 15:  # Solo para casos extremos >15
                return Response({
                    'success': False,
                    'message': f'AVISO: Dosis {dosis_numero_frontend} excede límites médicos extremos. Máximo recomendado: {limite_seguridad_absoluto} dosis.',
                    'error_code': 'DOSE_REQUIRES_AUTHORIZATION',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 🛡️ CORRECCION CRITICA: Validación anti-duplicados ESTRICTA con timing
            from django.utils import timezone
            from datetime import timedelta

            # 1. VALIDACIÓN TEMPORAL ESTRICTA: Prevenir aplicaciones en ventana de 30 segundos
            timeframe_critico = timezone.now() - timedelta(seconds=30)

            aplicaciones_recientes = HistorialVacunacion.objects.filter(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                fecha_aplicacion=fecha_aplicacion,
                dosis_numero=dosis_numero_frontend,
                creado__gte=timeframe_critico,  # Solo últimos 30 segundos
                estado__in=['aplicada', 'vigente', 'completado']
            )

            if aplicaciones_recientes.exists():
                return Response({
                    'success': False,
                    'message': f'🚨 Duplicado detectado: Se intentó aplicar la misma dosis en los últimos 30 segundos. Esto podría ser un doble-click accidental.',
                    'error_code': 'RECENT_DUPLICATE_DETECTED',
                    'debug_info': {
                        'timeframe': '30 segundos',
                        'aplicaciones_encontradas': aplicaciones_recientes.count()
                    },
                    'status': 'error'
                }, status=status.HTTP_409_CONFLICT)

            # 2. VALIDACIÓN DIARIA: No permitir misma vacuna, mismo día, MISMA DOSIS
            aplicaciones_duplicadas = HistorialVacunacion.objects.filter(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                fecha_aplicacion=fecha_aplicacion,
                dosis_numero=dosis_numero_frontend,  # Misma dosis = duplicado real
                estado__in=['aplicada', 'vigente', 'completado']
            )

            if aplicaciones_duplicadas.exists():
                return Response({
                    'success': False,
                    'message': f'Ya se aplicó dosis {dosis_numero_frontend} de {vacuna.nombre} a esta mascota el {fecha_aplicacion}. No se puede aplicar la misma dosis dos veces el mismo día.',
                    'error_code': 'DUPLICATE_EXACT_DOSE',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 🔒 VALIDACIÓN INTELIGENTE: Prevenir duplicados pero permitir refuerzos legítimos
            aplicaciones_existentes = HistorialVacunacion.objects.filter(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                estado__in=['aplicada', 'vigente', 'proxima', 'completado']
            ).order_by('-fecha_aplicacion')

            if aplicaciones_existentes.exists():
                ultima_aplicacion = aplicaciones_existentes.first()

                # Calcular días desde última aplicación
                dias_desde_ultima = (fecha_aplicacion - ultima_aplicacion.fecha_aplicacion).days

                # 🔒 REGLA 1: Prevenir duplicados RECIENTES (menos de 30 días)
                if dias_desde_ultima < 30:
                    return Response({
                        'success': False,
                        'message': f'{vacuna.nombre} fue aplicada recientemente el {ultima_aplicacion.fecha_aplicacion} (hace {dias_desde_ultima} días). Espere al menos 30 días para reaplicar.',
                        'error_code': 'RECENTLY_APPLIED',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # 🔒 REGLA 2: Para dosis única, verificar si realmente necesita refuerzo
                if vacuna.dosis_total == 1:
                    # Permitir refuerzo solo si la anterior está vencida o próxima a vencer
                    if ultima_aplicacion.estado in ['vigente'] and dias_desde_ultima < 300:  # ~10 meses
                        return Response({
                            'success': False,
                            'message': f'{vacuna.nombre} aún está vigente (aplicada el {ultima_aplicacion.fecha_aplicacion}). No necesita refuerzo hasta que esté próxima a vencer.',
                            'error_code': 'VACCINE_STILL_VALID',
                            'status': 'error'
                        }, status=status.HTTP_400_BAD_REQUEST)

                # 🔒 REGLA 3: Para multi-dosis, verificar protocolo activo
                elif aplicaciones_existentes.count() >= vacuna.dosis_total:
                    # Permitir solo si todas las dosis anteriores están vencidas (reinicio de protocolo)
                    estados_anteriores = [app.estado for app in aplicaciones_existentes]
                    if any(estado in ['vigente', 'proxima', 'aplicada'] for estado in estados_anteriores):
                        return Response({
                            'success': False,
                            'message': f'{vacuna.nombre} ya completó su protocolo de {vacuna.dosis_total} dosis y aún tiene protección activa. Para reiniciar protocolo, espere a que todas las dosis estén vencidas.',
                            'error_code': 'PROTOCOL_STILL_ACTIVE',
                            'status': 'error'
                        }, status=status.HTTP_400_BAD_REQUEST)
            
            # 2. Solo validar duplicados exactos en fechas muy cercanas (mismo día con misma dosis ya validado arriba)
            # No validar intervalos - permitir flexibilidad total para uso normal
            
            dosis_real_en_protocolo = dosis_numero_frontend
            
            # 2. EDAD DE LA MASCOTA (CON FALLBACK SEGURO)
            from django.utils import timezone
            mascota = Mascota.objects.get(id=data['mascota_id'])
            if mascota.fechaNacimiento:
                edad_actual_dias = (timezone.now().date() - mascota.fechaNacimiento).days
                es_cachorro = edad_actual_dias <= 365
            else:
                edad_actual_dias = 365  # Fallback: asumir adulto
                es_cachorro = False
            
            # 3. DETERMINAR PROTOCOLO EFECTIVO PRIMERO (ORDEN DE PRECEDENCIA ESTRICTO)
            protocolo_info = {
                'tipo': '',
                'dosis_total': vacuna.dosis_total,
                'intervalos': []
            }
            
            # Variables para verificación de atraso inteligente
            reiniciar_protocolo = False
            
            # PRECEDENCIA 1: Protocolo complejo JSON (más específico)
            if vacuna.protocolo_dosis and len(vacuna.protocolo_dosis) > 0:
                protocolo_info['tipo'] = 'PROTOCOLO_COMPLEJO'
                protocolo_info['dosis_total'] = len(vacuna.protocolo_dosis)
                
                # Validar y extraer intervalos
                for i, dosis_info in enumerate(vacuna.protocolo_dosis):
                    if isinstance(dosis_info, dict) and 'semanas_siguiente' in dosis_info:
                        semanas = dosis_info.get('semanas_siguiente', vacuna.intervalo_dosis_semanas)
                        if semanas > 0:
                            protocolo_info['intervalos'].append(semanas)
                        else:
                            protocolo_info['intervalos'].append(vacuna.intervalo_dosis_semanas)
                    else:
                        protocolo_info['intervalos'].append(vacuna.intervalo_dosis_semanas)
            
            # PRECEDENCIA 2: Protocolo cachorro (si aplica)
            elif (vacuna.protocolo_cachorro and 
                  isinstance(vacuna.protocolo_cachorro, dict) and 
                  len(vacuna.protocolo_cachorro) > 0 and 
                  es_cachorro and 
                  historial_count == 0):
                
                protocolo_info['tipo'] = 'PROTOCOLO_CACHORRO'
                p_cachorro = vacuna.protocolo_cachorro
                
                dosis_total_cachorro = p_cachorro.get('dosis_total', vacuna.dosis_total)
                if dosis_total_cachorro > 0:
                    protocolo_info['dosis_total'] = dosis_total_cachorro
                
                intervalos_cachorro = p_cachorro.get('intervalos', [])
                if intervalos_cachorro and isinstance(intervalos_cachorro, list):
                    for intervalo in intervalos_cachorro:
                        if intervalo > 0:
                            protocolo_info['intervalos'].append(intervalo)
                        else:
                            protocolo_info['intervalos'].append(vacuna.intervalo_dosis_semanas)
                else:
                    protocolo_info['intervalos'] = [vacuna.intervalo_dosis_semanas] * (dosis_total_cachorro - 1)
            
            # PRECEDENCIA 3: Protocolo estándar (fallback siempre)
            else:
                protocolo_info['tipo'] = 'PROTOCOLO_ESTANDAR'
                protocolo_info['dosis_total'] = vacuna.dosis_total
                protocolo_info['intervalos'] = [vacuna.intervalo_dosis_semanas] * (vacuna.dosis_total - 1)
            
            # 4. 🔥 VERIFICAR DOSIS ATRASADAS CON PROTOCOLO INTELIGENTE (FIXED + DEBUG)
            ultima_aplicacion = historial_previo_query.last()
            print(f"DEBUG vencida_reinicio: historial_count={historial_count}, ultima_aplicacion={ultima_aplicacion}")

            if ultima_aplicacion and historial_count > 0:
                # 🚨 FIX CRÍTICO: Comparar con próxima_fecha esperada, NO con fecha_aplicacion
                dias_desde_proxima_esperada = (fecha_aplicacion - ultima_aplicacion.proxima_fecha).days
                print(f"DEBUG: dias_desde_proxima_esperada={dias_desde_proxima_esperada}, ultima_proxima={ultima_aplicacion.proxima_fecha}")

                # Calcular máximo atraso permitido según el protocolo actual
                dosis_previa = historial_count  # La dosis anterior (1-based)
                print(f"DEBUG: dosis_previa={dosis_previa}, protocolo_intervalos={protocolo_info.get('intervalos')}")

                if protocolo_info['intervalos'] and dosis_previa <= len(protocolo_info['intervalos']):
                    # Usar intervalo específico del protocolo
                    intervalo_esperado_semanas = protocolo_info['intervalos'][dosis_previa - 1]
                    max_atraso_dinamico = (intervalo_esperado_semanas * 7) + 21  # Intervalo + 3 semanas tolerancia
                    print(f"DEBUG: Usando intervalo protocolo: {intervalo_esperado_semanas} semanas, max_atraso_dinamico={max_atraso_dinamico}")
                else:
                    # Fallback: usar configuración base
                    max_atraso_dinamico = vacuna.max_dias_atraso
                    print(f"DEBUG: Usando max_dias_atraso base: {max_atraso_dinamico}")

                print(f"DEBUG: Comparando {dias_desde_proxima_esperada} > {max_atraso_dinamico}? {dias_desde_proxima_esperada > max_atraso_dinamico}")

                # 🔥 LÓGICA CORREGIDA: Usar días desde próxima fecha esperada
                if dias_desde_proxima_esperada > max_atraso_dinamico:
                    reiniciar_protocolo = True
                    # Marcar registros previos como vencida_reinicio
                    registros_actualizados = HistorialVacunacion.objects.filter(
                        mascota_id=data['mascota_id'],
                        vacuna=vacuna,
                        estado__in=['aplicada', 'vigente', 'vencida']  # 🆕 Incluir 'vencida'
                    ).update(estado='vencida_reinicio')
                    dosis_real_en_protocolo = 1  # Reiniciar como dosis 1
                    print(f"🚀 PROTOCOLO REINICIADO: {dias_desde_proxima_esperada} días desde próxima fecha > {max_atraso_dinamico} días permitidos")
                    print(f"📝 {registros_actualizados} registros marcados como vencida_reinicio")
                else:
                    print(f"DEBUG: NO se reinicia protocolo. {dias_desde_proxima_esperada} <= {max_atraso_dinamico}")
            
            # 5. CALCULAR PRÓXIMA FECHA (ALGORITMO UNIVERSAL)
            dosis_total_efectiva = protocolo_info['dosis_total']
            
            try:
                if dosis_real_en_protocolo == 1 and dosis_total_efectiva == 1:
                    # ESCENARIO 1: VACUNA DOSIS ÚNICA
                    proxima_fecha = fecha_aplicacion + relativedelta(months=vacuna.frecuencia_meses)
                    es_dosis_final = True
                    intervalo_usado = f"{vacuna.frecuencia_meses} meses"
                    
                elif dosis_real_en_protocolo < dosis_total_efectiva:
                    # ESCENARIO 2: PROTOCOLO INCOMPLETO
                    indice_intervalo = dosis_real_en_protocolo - 1  # 0-based
                    
                    if protocolo_info['intervalos'] and indice_intervalo < len(protocolo_info['intervalos']):
                        intervalo_semanas = protocolo_info['intervalos'][indice_intervalo]
                    else:
                        intervalo_semanas = vacuna.intervalo_dosis_semanas
                    
                    # Validación final del intervalo
                    if intervalo_semanas <= 0:
                        intervalo_semanas = vacuna.intervalo_dosis_semanas
                    
                    proxima_fecha = fecha_aplicacion + timedelta(weeks=intervalo_semanas)
                    es_dosis_final = False
                    intervalo_usado = f"{intervalo_semanas} semanas"
                    
                else:
                    # ESCENARIO 3: PROTOCOLO COMPLETO - REFUERZO ANUAL
                    proxima_fecha = fecha_aplicacion + relativedelta(months=vacuna.frecuencia_meses)
                    es_dosis_final = True
                    intervalo_usado = f"{vacuna.frecuencia_meses} meses"
                
                # Validar fecha calculada
                if proxima_fecha <= fecha_aplicacion:
                    raise ValueError(f"Fecha calculada inválida: {proxima_fecha}")
                    
            except Exception as calc_error:
                # FALLBACK DE EMERGENCIA: Refuerzo anual
                proxima_fecha = fecha_aplicacion + relativedelta(months=vacuna.frecuencia_meses)
                es_dosis_final = True
                intervalo_usado = f"{vacuna.frecuencia_meses} meses (fallback)"
                print(f"WARNING: Usando fallback por error: {str(calc_error)}")
            
            # 🔒 VERIFICACIÓN FINAL ANTI-RACE CONDITION: Verificar duplicados otra vez
            # Esta verificación ocurre dentro de la transacción atómica
            verificacion_final = HistorialVacunacion.objects.filter(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                fecha_aplicacion=fecha_aplicacion,
                dosis_numero=dosis_numero_frontend,
                estado__in=['aplicada', 'vigente', 'completado']
            )

            if verificacion_final.exists():
                return Response({
                    'success': False,
                    'message': f'🔒 Race condition detectada: Otro proceso ya aplicó esta vacuna durante la validación.',
                    'error_code': 'RACE_CONDITION_DUPLICATE',
                    'status': 'error'
                }, status=status.HTTP_409_CONFLICT)

            # 📝 Crear nuevo registro PRIMERO (sin marcar anteriores aún)
            try:
                historial = HistorialVacunacion.objects.create(
                    mascota_id=data['mascota_id'],
                    vacuna=vacuna,
                    fecha_aplicacion=fecha_aplicacion,
                    proxima_fecha=proxima_fecha,
                    veterinario_id=data['veterinario_id'],
                    dosis_numero=dosis_real_en_protocolo,  # Usar dosis calculada
                    lote=data.get('lote', ''),
                    observaciones=data.get('observaciones', ''),
                    estado='aplicada'  # 🆕 Siempre aplicada al crear, el serializer calculará dinámicamente
                )
            except IntegrityError as e:
                return Response({
                    'success': False,
                    'message': f'🔒 Error de integridad: Posible duplicado detectado.',
                    'error_code': 'INTEGRITY_ERROR_DUPLICATE',
                    'status': 'error'
                }, status=status.HTTP_409_CONFLICT)
            
            # 🔄 SOLO marcar registros anteriores como completado SI es dosis final
            if es_dosis_final or dosis_real_en_protocolo >= dosis_total_efectiva:
                HistorialVacunacion.objects.filter(
                    mascota_id=data['mascota_id'],
                    vacuna=vacuna,
                    estado__in=['aplicada', 'vigente', 'vencida', 'proxima']
                ).exclude(id=historial.id).update(estado='completado')
            
            # 📊 Generar mensaje personalizado inteligente
            if not es_dosis_final:
                mensaje_usuario = f"Próxima dosis (#{dosis_real_en_protocolo + 1}) en {intervalo_usado}"
            else:
                mensaje_usuario = f"Próximo refuerzo en {intervalo_usado}"
            
            return Response({
                'success': True,
                'message': f'Vacuna {vacuna.nombre} aplicada correctamente',
                'data': {
                    'historial_id': str(historial.id),
                    'proxima_fecha': proxima_fecha.isoformat(),
                    'proxima_fecha_calculada': True,
                    'mensaje_usuario': mensaje_usuario,
                    'protocolo_info': {
                        'dosis_actual': dosis_real_en_protocolo,
                        'dosis_total_original': vacuna.dosis_total,
                        'dosis_total_efectiva': dosis_total_efectiva,
                        'es_dosis_final': es_dosis_final,
                        'intervalo_usado': intervalo_usado,
                        'protocolo_usado': protocolo_info['tipo'],
                        'reinicio_por_atraso': reiniciar_protocolo,
                        'es_cachorro': es_cachorro,
                        'edad_dias': edad_actual_dias
                    }
                },
                'status': 'success'
            }, status=201)
            
        except ValueError as e:
            # Errores de validación específicos (fechas, datos inválidos)
            return Response({
                'success': False,
                'message': f'Datos inválidos: {str(e)}',
                'error_code': 'VALIDATION_ERROR',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Mascota.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Mascota no encontrada',
                'error_code': 'MASCOTA_NOT_FOUND',
                'status': 'error'
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Veterinario.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Veterinario no encontrado',
                'error_code': 'VETERINARIO_NOT_FOUND', 
                'status': 'error'
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # Log del error para debugging (en producción usar logging)
            print(f"ERROR INESPERADO en aplicar vacuna: {str(e)}")
            return Response({
                'success': False,
                'message': 'Error interno del servidor',
                'error_code': 'INTERNAL_SERVER_ERROR',
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistorialVacunacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión del historial de vacunación
    """
    queryset = HistorialVacunacion.objects.all()
    serializer_class = HistorialVacunacionSerializer
    
    def calcular_proxima_fecha(self, vacuna, fecha_aplicacion, dosis_numero):
        """
        🧠 ALGORITMO INTELIGENTE: Calcula próxima fecha según protocolo de vacunación
        
        LÓGICA:
        - Si dosis_numero < dosis_total: Próxima dosis del mismo ciclo (+intervalo_dosis_semanas)
        - Si dosis_numero >= dosis_total: Último refuerzo anual (+frecuencia_meses)
        
        EJEMPLOS:
        - Rabia (1 dosis, refuerzo anual): Dosis 1 → +12 meses
        - Triple (3 dosis + refuerzo): Dosis 1,2 → +4 semanas | Dosis 3 → +12 meses
        """
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta
        
        if dosis_numero < vacuna.dosis_total:
            # 📅 Próxima dosis del mismo ciclo inicial
            proxima_fecha = fecha_aplicacion + timedelta(weeks=vacuna.intervalo_dosis_semanas)
            return proxima_fecha
        else:
            # 📅 Último refuerzo: próximo ciclo anual
            proxima_fecha = fecha_aplicacion + relativedelta(months=vacuna.frecuencia_meses)
            return proxima_fecha

    def calcular_estado_inicial(self, proxima_fecha):
        """
        🧠 CALCULAR ESTADO INICIAL CORRECTO al momento de aplicación
        Garantiza que el estado sea coherente desde la creación
        """
        from datetime import date

        # Si no hay próxima fecha, usar estado por defecto
        if not proxima_fecha:
            return 'aplicada'

        try:
            today = date.today()
            dias_diferencia = (proxima_fecha - today).days

            # 🔍 LÓGICA DE ESTADOS INICIAL:
            # 1. VENCIDA: Si la próxima fecha ya pasó
            if dias_diferencia < 0:
                return 'vencida'

            # 2. PRÓXIMA: Si vence en los próximos 30 días
            elif 0 <= dias_diferencia <= 30:
                return 'proxima'

            # 3. VIGENTE: Si vence en más de 30 días
            else:
                return 'vigente'

        except Exception as e:
            # En caso de error, devolver estado seguro
            print(f"Error calculando estado inicial: {e}")
            return 'aplicada'

    def get_queryset(self):
        mascota_id = self.request.query_params.get('mascota_id')
        if mascota_id:
            return HistorialVacunacion.objects.filter(mascota__id=mascota_id)
        return HistorialVacunacion.objects.all()
    
    @action(detail=False, methods=['get'], url_path='por-mascota/(?P<mascota_id>[^/.]+)')
    def por_mascota(self, request, mascota_id=None):
        """Obtener historial de vacunación por mascota"""
        historial = HistorialVacunacion.objects.filter(
            mascota__id=mascota_id
        ).order_by('-fecha_aplicacion')
        serializer = self.get_serializer(historial, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='vencidas')
    def vencidas(self, request):
        """Obtener vacunas vencidas"""
        from datetime import date
        historial_vencido = HistorialVacunacion.objects.filter(
            proxima_fecha__lt=date.today()
        ).order_by('proxima_fecha')
        serializer = self.get_serializer(historial_vencido, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='proximas')
    def proximas(self, request):
        """Obtener vacunas próximas a vencer (próximos 30 días)"""
        from datetime import date, timedelta
        fecha_limite = date.today() + timedelta(days=30)
        historial_proximo = HistorialVacunacion.objects.filter(
            proxima_fecha__gte=date.today(),
            proxima_fecha__lte=fecha_limite
        ).order_by('proxima_fecha')
        serializer = self.get_serializer(historial_proximo, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='alertas')
    def alertas(self, request):
        """
        Endpoint especializado para alertas del dashboard
        Devuelve vacunas vencidas y próximas a vencer con información completa
        """
        from datetime import date, timedelta
        from django.db.models import Q
        
        # Vacunas vencidas o próximas a vencer (próximos 7 días)
        fecha_limite = date.today() + timedelta(days=7)
        
        alertas_query = HistorialVacunacion.objects.filter(
            Q(proxima_fecha__lt=date.today()) |  # Vencidas
            Q(proxima_fecha__lte=fecha_limite)   # Próximas a vencer
        ).select_related('mascota', 'vacuna', 'mascota__responsable').order_by('proxima_fecha')
        
        alertas_data = []
        for item in alertas_query:
            dias_vencimiento = (item.proxima_fecha - date.today()).days
            estado_alert = 'vencida' if dias_vencimiento < 0 else 'proxima'
            
            alertas_data.append({
                'mascota_id': str(item.mascota.id),
                'nombre_mascota': item.mascota.nombreMascota,
                'vacuna_nombre': item.vacuna.nombre,
                'proxima_fecha': item.proxima_fecha,
                'dias_vencimiento': dias_vencimiento,
                'estado': estado_alert,
                'responsable_nombre': f"{item.mascota.responsable.nombres} {item.mascota.responsable.apellidos}",
                'responsable_telefono': item.mascota.responsable.telefono
            })
        
        serializer = VacunasAlertaSerializer(alertas_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='estadisticas')
    def estadisticas(self, request):
        """Estadísticas generales de vacunación"""
        from datetime import date, timedelta
        
        total_vacunas = HistorialVacunacion.objects.count()
        vencidas = HistorialVacunacion.objects.filter(
            proxima_fecha__lt=date.today()
        ).count()
        proximas_30_dias = HistorialVacunacion.objects.filter(
            proxima_fecha__gte=date.today(),
            proxima_fecha__lte=date.today() + timedelta(days=30)
        ).count()
        
        return Response({
            'total_vacunas_aplicadas': total_vacunas,
            'vacunas_vencidas': vencidas,
            'vacunas_proximas_30_dias': proximas_30_dias,
            'porcentaje_cumplimiento': round((total_vacunas - vencidas) / total_vacunas * 100, 2) if total_vacunas > 0 else 0
        })
    
    @action(detail=False, methods=['post'], url_path='aplicar-vacuna')
    def aplicar_vacuna(self, request):
        """
        Endpoint para aplicar una vacuna con cálculo automático de próxima fecha
        URL: POST /api/historial-vacunacion/aplicar-vacuna/
        Body: {
            "mascota_id": "uuid",
            "vacuna_id": "uuid", 
            "fecha_aplicacion": "2025-09-07",
            "veterinario_id": "uuid",
            "lote": "L123456",
            "observaciones": "Primera dosis",
            "dosis_numero": 1
        }
        """
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        try:
            data = request.data
            
            # Obtener la vacuna para calcular próxima fecha
            vacuna_id = data.get('vacuna_id') or data.get('vacuna')  # Acepta ambos formatos
            vacuna = Vacuna.objects.get(id=vacuna_id)
            fecha_aplicacion = date.fromisoformat(data['fecha_aplicacion'])
            
            # 🧠 LÓGICA INTELIGENTE: Calcular próxima fecha según protocolo de vacunación
            dosis_numero = data.get('dosis_numero', 1)
            proxima_fecha = self.calcular_proxima_fecha(vacuna, fecha_aplicacion, dosis_numero)
            
                # 🔄 ACTUALIZAR REGISTROS ANTERIORES DE LA MISMA VACUNA
            # Marcar registros anteriores como "completados" para eliminar alertas
            registros_anteriores = HistorialVacunacion.objects.filter(
                mascota_id=data.get('mascota_id') or data.get('mascota'),
                vacuna_id=vacuna_id,
                estado__in=['aplicada', 'vigente', 'vencida', 'proxima']  # Todos los estados activos
            )
            
            # Actualizar estados anteriores a "completado" para que no aparezcan en alertas
            registros_anteriores.update(estado='completado')
            
            # Crear el registro de historial con datos calculados
            historial_data = {
                **data,
                'proxima_fecha': proxima_fecha.isoformat(),
                'estado': 'aplicada'  # Recién aplicada, será vigente hasta que se acerque próxima fecha
            }
            
            serializer = self.get_serializer(data=historial_data)
            if serializer.is_valid():
                historial = serializer.save()
                
                # 📊 GENERAR MENSAJE PERSONALIZADO SEGÚN PROTOCOLO
                dias_restantes = (proxima_fecha - fecha_aplicacion).days
                if dosis_numero < vacuna.dosis_total:
                    mensaje_usuario = f"Próxima dosis (#{dosis_numero + 1}) en {vacuna.intervalo_dosis_semanas} semanas"
                else:
                    mensaje_usuario = f"Próximo refuerzo en {vacuna.frecuencia_meses} meses"
                
                return Response({
                    'success': True,
                    'message': f'Vacuna {vacuna.nombre} aplicada correctamente',
                    'data': {
                        'historial_id': str(historial.id),
                        'proxima_fecha': proxima_fecha.isoformat(),
                        'proxima_fecha_calculada': True,
                        'mensaje_usuario': mensaje_usuario,
                        'protocolo_info': {
                            'dosis_actual': dosis_numero,
                            'dosis_total': vacuna.dosis_total,
                            'es_dosis_final': dosis_numero >= vacuna.dosis_total,
                            'intervalo_usado': f"{vacuna.intervalo_dosis_semanas} semanas" if dosis_numero < vacuna.dosis_total else f"{vacuna.frecuencia_meses} meses"
                        }
                    },
                    'status': 'success'
                }, status=201)
            else:
                return Response({
                    'message': 'Error en los datos proporcionados',
                    'errors': serializer.errors,
                    'status': 'error'
                }, status=400)
                
        except Vacuna.DoesNotExist:
            return Response({
                'message': 'Vacuna no encontrada',
                'status': 'error'
            }, status=404)
        except Exception as e:
            return Response({
                'message': f'Error al aplicar vacuna: {str(e)}',
                'status': 'error'
            }, status=500)


# 🚨 ENDPOINT ESPECIALIZADO PARA DASHBOARD DE ALERTAS
@api_view(['GET'])
def alertas_dashboard(request):
    """
    Endpoint especializado para alertas del dashboard principal
    URL: GET /api/dashboard/alertas-vacunacion/
    Devuelve vacunas vencidas y próximas a vencer con información completa
    """
    from datetime import date, timedelta
    from django.db.models import Q
    
    try:
        # LIMPIEZA Y ACTUALIZACIÓN AUTOMÁTICA DE ESTADOS
        fecha_limpieza = date.today() - timedelta(days=7)
        fecha_hoy = date.today()
        fecha_proxima = date.today() + timedelta(days=7)
        
        # 1. Limpiar alertas vencidas hace más de 1 semana
        HistorialVacunacion.objects.filter(
            proxima_fecha__lte=fecha_limpieza,
            estado='vencida'
        ).update(estado='completado')
        
        # 2. Actualizar estados según fechas actuales
        # Definir límites de tiempo para clasificación
        fecha_reinicio = date.today() - timedelta(days=180)  # 6 meses = reinicio
        fecha_critica = date.today() + timedelta(days=7)

        # PRIMERO: Marcar como vencidas normales las que pasaron su fecha (pero <180 días)
        HistorialVacunacion.objects.filter(
            proxima_fecha__lt=fecha_hoy,
            proxima_fecha__gte=fecha_reinicio,
            estado='aplicada'
        ).update(estado='vencida')

        # DESPUÉS: Marcar como vencida_reinicio las muy vencidas (>180 días) - SOBRESCRIBE vencidas normales si es necesario
        HistorialVacunacion.objects.filter(
            proxima_fecha__lt=fecha_reinicio,
            estado__in=['aplicada', 'vencida']
        ).update(estado='vencida_reinicio')

        # Marcar como críticas las próximas (0-7 días)
        HistorialVacunacion.objects.filter(
            proxima_fecha__lte=fecha_critica,
            proxima_fecha__gte=fecha_hoy,
            estado='aplicada'
        ).exclude(
            estado='vencida_reinicio'
        ).update(estado='critica')

        # Marcar como próximas las que están en rango normal (8-30 días)
        fecha_proxima_normal = date.today() + timedelta(days=30)
        HistorialVacunacion.objects.filter(
            proxima_fecha__lte=fecha_proxima_normal,
            proxima_fecha__gt=fecha_critica,
            estado='aplicada'
        ).exclude(
            estado='vencida_reinicio'
        ).update(estado='proxima')

        # 3. PROGRESIÓN AUTOMÁTICA DE MULTI-DOSIS (FIX GIARDIA)
        # Encontrar vacunas vencidas que necesitan pasar a la siguiente dosis
        from dateutil.relativedelta import relativedelta
        from django.db.models import F

        vacunas_multidosis_vencidas = HistorialVacunacion.objects.filter(
            proxima_fecha__lt=fecha_hoy,
            estado='vencida',
            dosis_numero__lt=F('vacuna__dosis_total')  # Dose < total required
        ).select_related('vacuna', 'mascota', 'veterinario')

        for registro_vencido in vacunas_multidosis_vencidas:
            # Check if next dose already exists
            siguiente_dosis_existente = HistorialVacunacion.objects.filter(
                mascota=registro_vencido.mascota,
                vacuna=registro_vencido.vacuna,
                dosis_numero=registro_vencido.dosis_numero + 1
            ).exists()

            if not siguiente_dosis_existente:
                # Create next dose record
                siguiente_dosis = HistorialVacunacion.objects.create(
                    mascota=registro_vencido.mascota,
                    vacuna=registro_vencido.vacuna,
                    fecha_aplicacion=None,  # NULL - to be applied when actually administered
                    proxima_fecha=fecha_hoy + timedelta(weeks=registro_vencido.vacuna.intervalo_dosis_semanas),
                    veterinario=registro_vencido.veterinario,
                    dosis_numero=registro_vencido.dosis_numero + 1,
                    estado='proxima',  # Next dose is pending
                    observaciones=f'Dosis {registro_vencido.dosis_numero + 1} creada automáticamente tras vencimiento de dosis {registro_vencido.dosis_numero}'
                )

                # Mark the previous dose as completed (replaced by next dose)
                registro_vencido.estado = 'completado'
                registro_vencido.save()

                print(f"AUTO-PROGRESIÓN: {registro_vencido.vacuna.nombre} - Dosis {registro_vencido.dosis_numero} -> Dosis {siguiente_dosis.dosis_numero} para {registro_vencido.mascota.nombreMascota}")
        
        # 🎯 CONSULTA SIMPLE - Solo vencidas y próximas (como solicitó el usuario)
        fecha_limite = date.today() + timedelta(days=30)  # 30 días hacia futuro
        fecha_limite_vencidas = date.today() - timedelta(days=180)  # No más de 180 días vencidas

        alertas_query = HistorialVacunacion.objects.filter(
            proxima_fecha__gte=fecha_limite_vencidas,  # No más de 180 días vencidas
            proxima_fecha__lte=fecha_limite  # No más de 30 días futuras
        ).exclude(
            estado='completado'
        ).select_related(
            'mascota', 'vacuna', 'mascota__responsable', 'veterinario'
        ).order_by('proxima_fecha')

        # 📊 CLASIFICACIÓN SIMPLE - Solo dos categorías
        alertas_data = []
        vencidas_count = 0
        proximas_count = 0

        for item in alertas_query:
            dias_restantes = (item.proxima_fecha - date.today()).days

            # 🎯 SOLO DOS ESTADOS como solicitó el usuario
            if dias_restantes < 0:  # Vencida (pero no más de 180 días)
                estado_alert = 'vencida'
                vencidas_count += 1
                prioridad = 'alta'
                color = 'red'
            else:  # Próxima (0-30 días)
                estado_alert = 'proxima'
                proximas_count += 1
                prioridad = 'media'
                color = 'yellow'
            
            alertas_data.append({
                'id': str(item.id),
                'mascota_id': str(item.mascota.id),
                'mascota_nombre': item.mascota.nombreMascota,
                'mascota_especie': item.mascota.especie,
                'vacuna_id': str(item.vacuna.id),
                'vacuna_nombre': item.vacuna.nombre,
                'es_obligatoria': item.vacuna.es_obligatoria,
                'fecha_aplicacion': item.fecha_aplicacion,
                'proxima_fecha': item.proxima_fecha,
                'dias_restantes': dias_restantes,
                'estado': estado_alert,  # Estado calculado en tiempo real
                'prioridad': prioridad,
                'dosis_numero': item.dosis_numero,
                'responsable_nombre': f"{item.mascota.responsable.nombres} {item.mascota.responsable.apellidos}",
                'responsable_telefono': item.mascota.responsable.telefono,
                'veterinario_nombre': f"{item.veterinario.trabajador.nombres} {item.veterinario.trabajador.apellidos}" if item.veterinario else None,
                'color': color
            })
        
        # 📊 ESTADÍSTICAS SIMPLES - Solo dos categorías
        mascotas_con_alertas = len(set([item['mascota_id'] for item in alertas_data]))

        estadisticas = {
            'total_alertas': len(alertas_data),
            'vencidas': vencidas_count,
            'proximas': proximas_count,
            'mascotas_requieren_atencion': mascotas_con_alertas,
            'fecha_consulta': date.today().isoformat()
        }
        
        return Response({
            'data': alertas_data,
            'estadisticas': estadisticas,
            'message': f'{len(alertas_data)} alertas de vacunación encontradas',
            'status': 'success'
        })
        
    except Exception as e:
        return Response({
            'message': f'Error al obtener alertas: {str(e)}',
            'status': 'error'
        }, status=500)


@api_view(['GET'])
def get_veterinario_externo(request):
    """
    Obtener ID del veterinario externo creado automáticamente por migración
    Para casos de historial de vacunación previo
    URL: GET /api/veterinario-externo/
    """
    try:
        # Intentar buscar por el email nuevo primero
        veterinario_externo = Veterinario.objects.filter(
            trabajador__email='veterinario.externo@sistema.com'
        ).first()

        # Si no existe, buscar por el email antiguo (compatibilidad)
        if not veterinario_externo:
            veterinario_externo = Veterinario.objects.filter(
                trabajador__email='externo@veterinaria.com'
            ).first()

        # Si no existe ninguno, buscar por rol veterinario_externo
        if not veterinario_externo:
            veterinario_externo = Veterinario.objects.filter(
                trabajador__usuario__rol='veterinario_externo'
            ).first()

        if not veterinario_externo:
            return Response({
                'error': 'Veterinario externo no encontrado. Verifica que la migración se ejecutó correctamente.'
            }, status=404)

        return Response({
            'veterinario_id': str(veterinario_externo.id),
            'veterinario_externo_id': str(veterinario_externo.id),
            'nombre': f"{veterinario_externo.trabajador.nombres} {veterinario_externo.trabajador.apellidos}",
            'email': veterinario_externo.trabajador.email,
            'mensaje': 'Veterinario para historial de vacunación externa'
        })
    except Exception as e:
        return Response({
            'error': f'Error al buscar veterinario externo: {str(e)}'
        }, status=500)


class HistorialMedicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión del historial médico
    """
    queryset = HistorialMedico.objects.all()
    serializer_class = HistorialMedicoSerializer
    
    def get_queryset(self):
        mascota_id = self.request.query_params.get('mascota_id')
        if mascota_id:
            return HistorialMedico.objects.filter(mascota__id=mascota_id)
        return HistorialMedico.objects.all()
    
    @action(detail=False, methods=['get'], url_path='por-mascota/(?P<mascota_id>[^/.]+)')
    def por_mascota(self, request, mascota_id=None):
        """Obtener historial médico completo por mascota"""
        historial = HistorialMedico.objects.filter(
            mascota__id=mascota_id
        ).order_by('-fecha')
        serializer = self.get_serializer(historial, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='por-tipo/(?P<tipo>[^/.]+)')
    def por_tipo(self, request, tipo=None):
        """Obtener historiales por tipo de atención"""
        historial = HistorialMedico.objects.filter(tipo=tipo).order_by('-fecha')
        serializer = self.get_serializer(historial, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='resumen-mascota/(?P<mascota_id>[^/.]+)')
    def resumen_mascota(self, request, mascota_id=None):
        """Resumen médico de la mascota"""
        from django.db.models import Count
        
        historial = HistorialMedico.objects.filter(mascota__id=mascota_id)
        
        resumen = {
            'total_consultas': historial.count(),
            'consultas_por_tipo': historial.values('tipo').annotate(
                total=Count('tipo')
            ).order_by('-total'),
            'ultima_consulta': historial.first().fecha if historial.exists() else None,
            'veterinarios_atendieron': historial.values(
                'veterinario__trabajador__nombres',
                'veterinario__trabajador__apellidos'
            ).distinct().count()
        }
        
        return Response(resumen)


# 🚀 VIEWSETS PROFESIONALES PARA SISTEMA DE CITAS



class HorarioTrabajoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de horarios de trabajo de veterinarios
    """
    queryset = HorarioTrabajo.objects.all()
    serializer_class = HorarioTrabajoSerializer
    filterset_fields = ['veterinario', 'dia_semana', 'activo']
    ordering_fields = ['veterinario', 'dia_semana', 'hora_inicio']
    ordering = ['veterinario', 'dia_semana']

    def get_queryset(self):
        """
        Optimizar consultas con select_related y aplicar filtros de query params
        """
        queryset = super().get_queryset().select_related(
            'veterinario__trabajador'
        )

        # Filtro por veterinario
        veterinario_id = self.request.query_params.get('veterinario')
        if veterinario_id:
            queryset = queryset.filter(veterinario=veterinario_id)

        # Filtro por día de la semana
        dia_semana = self.request.query_params.get('dia_semana')
        if dia_semana:
            queryset = queryset.filter(dia_semana=dia_semana)

        # Filtro por activo
        activo = self.request.query_params.get('activo')
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')

        return queryset

    @action(detail=False, methods=['get'], url_path='veterinario/(?P<veterinario_id>[^/.]+)')
    def horarios_veterinario(self, request, veterinario_id=None):
        """Obtener horarios de un veterinario específico"""
        horarios = self.get_queryset().filter(
            veterinario__id=veterinario_id,
            activo=True
        ).order_by('dia_semana')

        serializer = self.get_serializer(horarios, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def disponibilidad_semana(self, request):
        """
        Obtener disponibilidad de todos los veterinarios para la semana
        """
        from datetime import date, timedelta

        veterinario_id = request.query_params.get('veterinario')
        fecha_inicio = request.query_params.get('fecha_inicio')

        # Calcular semana actual si no se especifica
        if not fecha_inicio:
            hoy = date.today()
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fecha_inicio = inicio_semana.strftime('%Y-%m-%d')

        queryset = self.get_queryset().filter(activo=True)
        if veterinario_id:
            queryset = queryset.filter(veterinario__id=veterinario_id)

        # Mapear días de la semana
        dias_map = {
            0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES',
            4: 'VIERNES', 5: 'SABADO', 6: 'DOMINGO'
        }

        # Crear estructura de respuesta
        disponibilidad = {}
        for horario in queryset:
            vet_id = str(horario.veterinario.id)
            if vet_id not in disponibilidad:
                disponibilidad[vet_id] = {
                    'veterinario': horario.veterinario.__str__(),
                    'dias': {}
                }

            disponibilidad[vet_id]['dias'][horario.dia_semana] = {
                'hora_inicio': horario.hora_inicio.strftime('%H:%M'),
                'hora_fin': horario.hora_fin.strftime('%H:%M'),
                'descanso_inicio': horario.hora_inicio_descanso.strftime('%H:%M') if horario.hora_inicio_descanso else None,
                'descanso_fin': horario.hora_fin_descanso.strftime('%H:%M') if horario.hora_fin_descanso else None,
                'duracion_jornada': HorarioTrabajoSerializer().get_duracion_jornada(horario)
            }

        return Response({
            'fecha_inicio': fecha_inicio,
            'disponibilidad': disponibilidad
        })


class SlotTiempoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de slots de tiempo
    Principalmente para consulta y generación automática
    """
    queryset = SlotTiempo.objects.all()
    serializer_class = SlotTiempoSerializer
    filterset_fields = ['veterinario', 'fecha', 'disponible']
    ordering_fields = ['fecha', 'hora_inicio', 'veterinario']
    ordering = ['fecha', 'hora_inicio']

    def get_queryset(self):
        """Optimizar consultas y filtros"""
        queryset = super().get_queryset().select_related(
            'veterinario__trabajador',
            'consultorio'
        )

        # Filtros por fecha
        fecha_desde = self.request.query_params.get('fecha_desde')
        fecha_hasta = self.request.query_params.get('fecha_hasta')

        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)

        return queryset

    @action(detail=False, methods=['post'], url_path='generar-slots')
    def generar_slots(self, request):
        """
        POST /api/slots-tiempo/generar-slots/

        Generar slots automáticamente basado en horarios de trabajo

        Body:
        {
            "veterinario_id": "uuid",
            "fecha_inicio": "2025-10-06",
            "fecha_fin": "2025-10-12",
            "duracion_slot_minutos": 30  // opcional, default 30
        }
        """
        from datetime import date, timedelta, datetime, time

        data = request.data
        veterinario_id = data.get('veterinario_id')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        duracion_slot = int(data.get('duracion_slot_minutos', 30))

        if not all([veterinario_id, fecha_inicio, fecha_fin]):
            return Response({
                'error': 'veterinario_id, fecha_inicio y fecha_fin son requeridos',
                'error_code': 'MISSING_PARAMETERS'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            veterinario = Veterinario.objects.get(id=veterinario_id)
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        except Veterinario.DoesNotExist:
            return Response({
                'error': 'Veterinario no encontrado',
                'error_code': 'VETERINARIAN_NOT_FOUND'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({
                'error': 'Formato de fecha inválido. Use YYYY-MM-DD',
                'error_code': 'INVALID_DATE_FORMAT'
            }, status=status.HTTP_400_BAD_REQUEST)

        slots_creados = 0
        slots_omitidos = 0
        fecha_actual = fecha_inicio

        while fecha_actual <= fecha_fin:
            dia_semana_numero = fecha_actual.weekday()  # 0=Lunes, 6=Domingo

            # Buscar horario de trabajo para este día
            horario = HorarioTrabajo.objects.filter(
                veterinario=veterinario,
                dia_semana=dia_semana_numero,
                activo=True
            ).first()

            if horario:
                # Generar slots para este día
                hora_actual = datetime.combine(fecha_actual, horario.hora_inicio)
                hora_fin_dia = datetime.combine(fecha_actual, horario.hora_fin)

                while hora_actual < hora_fin_dia:
                    hora_fin_slot = hora_actual + timedelta(minutes=duracion_slot)

                    # No generar slots que pasen del horario de fin
                    if hora_fin_slot.time() > horario.hora_fin:
                        break

                    # Verificar que no coincida con horario de descanso
                    en_descanso = False
                    if horario.tiene_descanso and horario.hora_inicio_descanso and horario.hora_fin_descanso:
                        if (hora_actual.time() >= horario.hora_inicio_descanso and
                            hora_actual.time() < horario.hora_fin_descanso):
                            en_descanso = True

                    if not en_descanso:
                        # Verificar si no existe ya este slot
                        slot_existente = SlotTiempo.objects.filter(
                            veterinario=veterinario,
                            fecha=fecha_actual,
                            hora_inicio=hora_actual.time()
                        ).first()

                        if not slot_existente:
                            SlotTiempo.objects.create(
                                veterinario=veterinario,
                                fecha=fecha_actual,
                                hora_inicio=hora_actual.time(),
                                hora_fin=hora_fin_slot.time(),
                                duracion_minutos=duracion_slot,
                                disponible=True,
                                generado_automaticamente=True
                            )
                            slots_creados += 1
                        else:
                            slots_omitidos += 1

                    hora_actual = hora_fin_slot

            fecha_actual += timedelta(days=1)

        return Response({
            'mensaje': f'Slots generados exitosamente para {veterinario.trabajador.nombres} {veterinario.trabajador.apellidos}',
            'slots_creados': slots_creados,
            'slots_omitidos': slots_omitidos,
            'periodo': {
                'inicio': str(fecha_inicio),
                'fin': str(fecha_fin)
            },
            'veterinario': {
                'id': str(veterinario.id),
                'nombre': f'{veterinario.trabajador.nombres} {veterinario.trabajador.apellidos}'
            },
            'status': 'success'
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """
        GET /api/slots-tiempo/disponibles/

        Obtener solo slots disponibles con filtros

        Query params:
        - veterinario: UUID del veterinario
        - fecha: Fecha específica (YYYY-MM-DD)
        - fecha_desde: Desde fecha (YYYY-MM-DD)
        - fecha_hasta: Hasta fecha (YYYY-MM-DD)
        - solo_futuro: true/false (default: true)
        """
        from datetime import date, datetime

        # Liberar slots con reserva temporal expirada
        slots_expirados = SlotTiempo.objects.filter(
            reservado_hasta__lt=timezone.now()
        ).exclude(reservado_hasta__isnull=True)

        for slot in slots_expirados:
            slot.reservado_hasta = None
            slot.save()

        # Filtrar slots disponibles
        queryset = self.get_queryset().filter(
            disponible=True
        )

        # Excluir slots reservados temporalmente
        queryset = queryset.filter(
            Q(reservado_hasta__isnull=True) |
            Q(reservado_hasta__lt=timezone.now())
        )

        # Filtro por veterinario
        veterinario_id = request.query_params.get('veterinario')
        if veterinario_id:
            queryset = queryset.filter(veterinario__id=veterinario_id)

        # Filtro por fecha específica
        fecha_especifica = request.query_params.get('fecha')
        if fecha_especifica:
            try:
                fecha = datetime.strptime(fecha_especifica, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha=fecha)
            except ValueError:
                pass

        # Solo fechas futuras
        solo_futuro = request.query_params.get('solo_futuro', 'true')
        if solo_futuro.lower() == 'true':
            queryset = queryset.filter(fecha__gte=date.today())

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'total': queryset.count(),
            'status': 'success'
        })

    @action(detail=True, methods=['post'], url_path='reservar-temporal')
    def reservar_temporal(self, request, pk=None):
        """
        POST /api/slots-tiempo/{id}/reservar-temporal/

        Reserva temporalmente un slot por N minutos

        Body:
        {
            "minutos": 5  // default: 5
        }
        """
        slot = self.get_object()

        # Verificar si está disponible
        if not slot.disponible:
            return Response({
                'error': 'El slot no está disponible',
                'error_code': 'SLOT_NOT_AVAILABLE'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si ya está reservado
        if slot.esta_reservado_temporalmente():
            return Response({
                'error': f'El slot ya está reservado hasta {slot.reservado_hasta}',
                'error_code': 'SLOT_ALREADY_RESERVED',
                'reservado_hasta': slot.reservado_hasta
            }, status=status.HTTP_409_CONFLICT)

        # Reservar temporalmente
        minutos = int(request.data.get('minutos', 5))
        slot.reservado_hasta = timezone.now() + timedelta(minutes=minutos)
        slot.save()

        return Response({
            'mensaje': 'Slot reservado temporalmente',
            'slot_id': str(slot.id),
            'reservado_hasta': slot.reservado_hasta,
            'minutos_restantes': minutos,
            'status': 'success'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='liberar-reserva')
    def liberar_reserva(self, request, pk=None):
        """
        POST /api/slots-tiempo/{id}/liberar-reserva/

        Libera una reserva temporal manualmente
        """
        slot = self.get_object()

        if not slot.reservado_hasta:
            return Response({
                'error': 'El slot no tiene una reserva temporal activa',
                'error_code': 'NO_RESERVATION_FOUND'
            }, status=status.HTTP_400_BAD_REQUEST)

        slot.reservado_hasta = None
        slot.save()

        return Response({
            'mensaje': 'Reserva liberada exitosamente',
            'slot_id': str(slot.id),
            'status': 'success'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='liberar-expirados')
    def liberar_expirados(self, request):
        """
        POST /api/slots-tiempo/liberar-expirados/

        Libera automáticamente todos los slots con reserva expirada
        (Este endpoint se puede llamar desde un cron job)
        """
        slots_expirados = SlotTiempo.objects.filter(
            reservado_hasta__lt=timezone.now()
        ).exclude(reservado_hasta__isnull=True)

        count = slots_expirados.count()
        slots_expirados.update(reservado_hasta=None)

        return Response({
            'mensaje': f'Se liberaron {count} slots con reserva expirada',
            'slots_liberados': count,
            'status': 'success'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='calendario')
    def calendario(self, request):
        """
        GET /api/slots-tiempo/calendario/

        Obtiene slots en formato calendario visual

        Query params:
        - veterinario: UUID del veterinario (requerido)
        - fecha: Fecha específica (YYYY-MM-DD) o default hoy
        """
        from datetime import date, datetime

        veterinario_id = request.query_params.get('veterinario')
        if not veterinario_id:
            return Response({
                'error': 'El parámetro veterinario es requerido',
                'error_code': 'MISSING_VETERINARIO'
            }, status=status.HTTP_400_BAD_REQUEST)

        fecha_param = request.query_params.get('fecha')
        if fecha_param:
            try:
                fecha = datetime.strptime(fecha_param, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'error': 'Formato de fecha inválido. Use YYYY-MM-DD',
                    'error_code': 'INVALID_DATE_FORMAT'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            fecha = date.today()

        # Obtener slots del día
        slots = SlotTiempo.objects.filter(
            veterinario__id=veterinario_id,
            fecha=fecha
        ).order_by('hora_inicio')

        # Agrupar por estado
        calendario_data = []
        for slot in slots:
            # Verificar si hay cita asociada
            from .models import Cita
            cita = Cita.objects.filter(
                veterinario__id=veterinario_id,
                fecha=fecha,
                hora=slot.hora_inicio
            ).exclude(estado='CANCELADA').first()

            estado_slot = 'disponible'
            detalle = None

            if cita:
                estado_slot = 'ocupado'
                detalle = {
                    'cita_id': str(cita.id),
                    'mascota': cita.mascota.nombreMascota,
                    'servicio': cita.servicio.nombre,
                    'estado': cita.estado
                }
            elif slot.esta_reservado_temporalmente():
                estado_slot = 'reservado_temporal'
                detalle = {
                    'reservado_hasta': slot.reservado_hasta
                }
            elif not slot.disponible:
                estado_slot = 'no_disponible'
                detalle = {
                    'motivo': slot.motivo_no_disponible
                }

            calendario_data.append({
                'slot_id': str(slot.id),
                'hora_inicio': slot.hora_inicio.strftime('%H:%M'),
                'hora_fin': slot.hora_fin.strftime('%H:%M'),
                'duracion_minutos': slot.duracion_minutos,
                'estado': estado_slot,
                'detalle': detalle
            })

        return Response({
            'fecha': str(fecha),
            'veterinario_id': veterinario_id,
            'slots': calendario_data,
            'total_slots': len(calendario_data),
            'disponibles': len([s for s in calendario_data if s['estado'] == 'disponible']),
            'ocupados': len([s for s in calendario_data if s['estado'] == 'ocupado']),
            'status': 'success'
        })


class CitaProfesionalViewSet(viewsets.ModelViewSet):
    """
    ViewSet extendido para gestión profesional de citas
    Incluye funcionalidades avanzadas como conflictos, recordatorios, etc.
    """
    queryset = Cita.objects.all()
    serializer_class = CitaProfesionalSerializer
    filterset_fields = ['veterinario', 'estado', 'fecha']
    ordering_fields = ['fecha', 'hora', 'fecha_creacion']
    ordering = ['fecha', 'hora']

    def get_queryset(self):
        """Optimizar consultas"""
        return super().get_queryset().select_related(
            'mascota', 'veterinario__trabajador', 'servicio'
        )

    @action(detail=False, methods=['get'])
    def agenda_dia(self, request):
        """
        Obtener agenda completa de un día específico
        """
        fecha = request.query_params.get('fecha')
        veterinario_id = request.query_params.get('veterinario')

        if not fecha:
            from datetime import date
            fecha = date.today().strftime('%Y-%m-%d')

        queryset = self.get_queryset().filter(fecha=fecha)
        if veterinario_id:
            queryset = queryset.filter(veterinario__id=veterinario_id)

        # Organizar por veterinario
        agenda = {}
        for cita in queryset.order_by('veterinario', 'hora'):
            vet_key = str(cita.veterinario.id)
            if vet_key not in agenda:
                agenda[vet_key] = {
                    'veterinario': cita.veterinario.__str__(),
                    'citas': []
                }

            serializer = self.get_serializer(cita)
            agenda[vet_key]['citas'].append(serializer.data)

        return Response({
            'fecha': fecha,
            'agenda': agenda,
            'total_citas': queryset.count()
        })

    @action(detail=False, methods=['post'])
    def verificar_conflictos(self, request):
        """
        Verificar conflictos de horario antes de crear una cita
        """
        data = request.data
        veterinario_id = data.get('veterinario')
        fecha = data.get('fecha')
        hora = data.get('hora')
        duracion = int(data.get('duracion_minutos', 30))

        if not all([veterinario_id, fecha, hora]):
            return Response({
                'error': 'veterinario, fecha y hora son requeridos'
            }, status=400)

        from datetime import datetime, timedelta
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_obj = datetime.strptime(hora, '%H:%M').time()
            fecha_hora_inicio = datetime.combine(fecha_obj, hora_obj)
            fecha_hora_fin = fecha_hora_inicio + timedelta(minutes=duracion)
        except ValueError as e:
            return Response({'error': f'Error en formato de fecha/hora: {e}'}, status=400)

        # Buscar citas existentes que puedan generar conflicto
        citas_conflicto = Cita.objects.filter(
            veterinario__id=veterinario_id,
            fecha=fecha_obj,
            hora__range=(
                (fecha_hora_inicio - timedelta(minutes=30)).time(),
                (fecha_hora_fin + timedelta(minutes=30)).time()
            )
        ).exclude(estado='CANCELADA')

        conflictos = []
        for cita in citas_conflicto:
            conflictos.append({
                'id': cita.id,
                'hora': cita.hora.strftime('%H:%M'),
                'mascota': cita.mascota.nombreMascota,
                'servicio': cita.servicio.nombre,
                'estado': cita.estado
            })

        return Response({
            'tiene_conflictos': len(conflictos) > 0,
            'conflictos': conflictos,
            'recomendaciones': self._generar_recomendaciones(veterinario_id, fecha_obj, hora_obj)
        })

    def _generar_recomendaciones(self, veterinario_id, fecha, hora_solicitada):
        """Generar recomendaciones de horarios alternativos"""
        from datetime import datetime, timedelta

        # Buscar slots disponibles cercanos
        slots_disponibles = SlotTiempo.objects.filter(
            veterinario__id=veterinario_id,
            fecha=fecha,
            disponible=True,
            bloqueado=False
        ).order_by('hora_inicio')

        recomendaciones = []
        hora_solicitada_dt = datetime.combine(fecha, hora_solicitada)

        for slot in slots_disponibles[:5]:  # Top 5 recomendaciones
            slot_dt = datetime.combine(fecha, slot.hora_inicio)
            diferencia = abs((slot_dt - hora_solicitada_dt).total_seconds() / 60)  # En minutos

            recomendaciones.append({
                'hora_inicio': slot.hora_inicio.strftime('%H:%M'),
                'hora_fin': slot.hora_fin.strftime('%H:%M'),
                'diferencia_minutos': int(diferencia)
            })

        return sorted(recomendaciones, key=lambda x: x['diferencia_minutos'])


# ============================================================================
# ENDPOINTS DE AUTENTICACIÓN Y PERMISOS
# ============================================================================

@api_view(['GET'])
def obtener_permisos_usuario(request):
    """
    GET /api/auth/permisos/

    Obtiene los permisos del usuario autenticado.
    El frontend usa esto para mostrar/ocultar opciones del menú.

    Requiere: Token JWT en headers

    Returns:
        {
            "usuario": {
                "id": "uuid",
                "email": "user@example.com",
                "rol": "veterinario",
                "rol_display": "Veterinario"
            },
            "permisos": {
                "dashboard": {"ver": true},
                "citas": {
                    "ver": true,
                    "crear": false,
                    ...
                },
                ...
            }
        }
    """
    from .permissions import PermisosPorRol
    from .choices import Rol

    if not request.user.is_authenticated:
        return Response({
            'error': 'Usuario no autenticado',
            'error_code': 'NOT_AUTHENTICATED'
        }, status=status.HTTP_401_UNAUTHORIZED)

    usuario = request.user
    rol = usuario.rol

    # Obtener nombre legible del rol
    rol_display = dict(Rol.ROL_CHOICES).get(rol, rol)

    # Obtener permisos del rol
    permisos = PermisosPorRol.obtener_permisos(rol)

    return Response({
        'usuario': {
            'id': str(usuario.id),
            'email': usuario.email,
            'rol': rol,
            'rol_display': rol_display,
            'is_staff': usuario.is_staff,
            'is_superuser': usuario.is_superuser
        },
        'permisos': permisos,
        'status': 'success'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def obtener_info_usuario(request):
    """
    GET /api/auth/me/

    Obtiene información completa del usuario autenticado.
    Incluye datos del trabajador si existe.

    Requiere: Token JWT en headers

    Returns:
        {
            "id": "uuid",
            "email": "user@example.com",
            "rol": "veterinario",
            "trabajador": {
                "id": "uuid",
                "nombres": "Juan",
                "apellidos": "Pérez",
                "telefono": "987654321"
            },
            "veterinario": {  // Solo si es veterinario
                "id": "uuid",
                "especialidad": "Medicina General"
            }
        }
    """
    if not request.user.is_authenticated:
        return Response({
            'error': 'Usuario no autenticado',
            'error_code': 'NOT_AUTHENTICATED'
        }, status=status.HTTP_401_UNAUTHORIZED)

    usuario = request.user
    response_data = {
        'id': str(usuario.id),
        'email': usuario.email,
        'rol': usuario.rol,
        'rol_display': dict(Rol.ROL_CHOICES).get(usuario.rol, usuario.rol),
        'is_staff': usuario.is_staff
    }

    # Agregar datos del trabajador si existe
    try:
        trabajador = usuario.trabajador
        response_data['trabajador'] = {
            'id': str(trabajador.id),
            'nombres': trabajador.nombres,
            'apellidos': trabajador.apellidos,
            'email': trabajador.email,
            'telefono': trabajador.telefono,
            'documento': trabajador.documento,
            'estado': trabajador.estado
        }

        # Si es veterinario, agregar datos adicionales
        if usuario.rol == Rol.VETERINARIO:
            try:
                veterinario = Veterinario.objects.get(trabajador=trabajador)
                response_data['veterinario'] = {
                    'id': str(veterinario.id),
                    'especialidad': veterinario.especialidad,
                    'registro_profesional': veterinario.registro_profesional,
                    'anios_experiencia': veterinario.anios_experiencia
                }
            except Veterinario.DoesNotExist:
                pass

    except Trabajador.DoesNotExist:
        response_data['trabajador'] = None

    return Response(response_data, status=status.HTTP_200_OK)


# ============================================
# GESTIÓN DINÁMICA DE PERMISOS
# ============================================

class PermisoRolViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión dinámica de permisos por rol.

    Endpoints:
    - GET /api/permisos-rol/              → Listar todos los permisos
    - GET /api/permisos-rol/{id}/         → Ver un permiso específico
    - POST /api/permisos-rol/             → Crear nuevo permiso
    - PUT /api/permisos-rol/{id}/         → Actualizar permiso completo
    - PATCH /api/permisos-rol/{id}/       → Actualizar permiso parcial
    - DELETE /api/permisos-rol/{id}/      → Eliminar permiso

    Endpoints personalizados:
    - GET /api/permisos-rol/por-rol/?rol=veterinario   → Permisos de un rol específico
    - POST /api/permisos-rol/actualizar-masivo/        → Actualizar múltiples permisos a la vez
    - GET /api/permisos-rol/modulos-disponibles/       → Lista de módulos del sistema
    - POST /api/permisos-rol/inicializar-defaults/     → Crear permisos por defecto
    """
    queryset = PermisoRol.objects.all()
    serializer_class = PermisoRolSerializer
    # permission_classes = [EsAdministrador]  # Solo admin puede gestionar permisos

    def get_queryset(self):
        """
        Permite filtrar por rol via query param
        """
        queryset = PermisoRol.objects.all()
        rol = self.request.query_params.get('rol', None)

        if rol:
            queryset = queryset.filter(rol=rol)

        return queryset

    @action(detail=False, methods=['get'], url_path='por-rol')
    def por_rol(self, request):
        """
        GET /api/permisos-rol/por-rol/?rol=veterinario

        Obtiene todos los permisos de un rol específico.
        """
        rol = request.query_params.get('rol')

        if not rol:
            return Response(
                {'error': 'Debe proporcionar el parámetro "rol"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        permisos = PermisoRol.objects.filter(rol=rol)
        serializer = self.get_serializer(permisos, many=True)

        return Response({
            'rol': rol,
            'permisos': serializer.data
        })

    @action(detail=False, methods=['post'], url_path='actualizar-masivo')
    def actualizar_masivo(self, request):
        """
        POST /api/permisos-rol/actualizar-masivo/

        Body:
        {
            "rol": "veterinario",
            "permisos": [
                {"modulo": "citas", "permisos": {"ver": true, "crear": false}},
                {"modulo": "mascotas", "permisos": {"ver": true, "editar": false}}
            ]
        }

        Actualiza múltiples permisos de un rol en una sola petición.
        """
        serializer = PermisoRolBulkUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rol = serializer.validated_data['rol']
        permisos_data = serializer.validated_data['permisos']

        actualizados = []
        creados = []

        with transaction.atomic():
            for item in permisos_data:
                modulo = item['modulo']
                permisos = item['permisos']
                descripcion = item.get('descripcion_modulo', '')

                permiso_obj, created = PermisoRol.objects.update_or_create(
                    rol=rol,
                    modulo=modulo,
                    defaults={
                        'permisos': permisos,
                        'descripcion_modulo': descripcion
                    }
                )

                if created:
                    creados.append(modulo)
                else:
                    actualizados.append(modulo)

        return Response({
            'mensaje': 'Permisos actualizados correctamente',
            'rol': rol,
            'actualizados': actualizados,
            'creados': creados,
            'total': len(permisos_data)
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='modulos-disponibles')
    def modulos_disponibles(self, request):
        """
        GET /api/permisos-rol/modulos-disponibles/

        Retorna la lista de módulos disponibles en el sistema
        con sus acciones posibles.
        """
        modulos = {
            'dashboard': {
                'nombre': 'Dashboard',
                'descripcion': 'Panel principal con estadísticas',
                'acciones': ['ver']
            },
            'citas': {
                'nombre': 'Citas',
                'descripcion': 'Gestión de citas veterinarias',
                'acciones': ['ver', 'crear', 'editar', 'eliminar', 'calendario_general', 'mi_calendario']
            },
            'mascotas': {
                'nombre': 'Mascotas',
                'descripcion': 'Gestión de mascotas',
                'acciones': ['ver', 'crear', 'editar', 'eliminar']
            },
            'responsables': {
                'nombre': 'Clientes',
                'descripcion': 'Gestión de dueños de mascotas',
                'acciones': ['ver', 'crear', 'editar', 'eliminar']
            },
            'vacunas': {
                'nombre': 'Vacunación',
                'descripcion': 'Sistema de vacunación',
                'acciones': ['ver', 'crear', 'editar', 'eliminar', 'aplicar', 'historial']
            },
            'historial_clinico': {
                'nombre': 'Historial Clínico',
                'descripcion': 'Historial médico de mascotas',
                'acciones': ['ver', 'crear', 'editar']
            },
            'servicios': {
                'nombre': 'Servicios',
                'descripcion': 'Catálogo de servicios veterinarios',
                'acciones': ['ver', 'crear', 'editar', 'eliminar']
            },
            'productos': {
                'nombre': 'Productos',
                'descripcion': 'Inventario de productos',
                'acciones': ['ver', 'crear', 'editar', 'eliminar']
            },
            'usuarios': {
                'nombre': 'Usuarios',
                'descripcion': 'Gestión de usuarios del sistema',
                'acciones': ['ver', 'crear', 'editar', 'eliminar']
            },
            'trabajadores': {
                'nombre': 'Trabajadores',
                'descripcion': 'Gestión de trabajadores',
                'acciones': ['ver', 'crear', 'editar', 'eliminar']
            },
            'veterinarios': {
                'nombre': 'Veterinarios',
                'descripcion': 'Gestión de veterinarios',
                'acciones': ['ver', 'crear', 'editar', 'eliminar', 'horarios', 'slots']
            },
            'reportes': {
                'nombre': 'Reportes',
                'descripcion': 'Generación de reportes',
                'acciones': ['ver', 'generar']
            },
            'configuracion': {
                'nombre': 'Configuración',
                'descripcion': 'Configuración del sistema',
                'acciones': ['ver', 'editar']
            }
        }

        return Response(modulos)

    @action(detail=False, methods=['post'], url_path='inicializar-defaults')
    def inicializar_defaults(self, request):
        """
        POST /api/permisos-rol/inicializar-defaults/

        Crea los permisos por defecto para todos los roles.
        Útil para inicializar el sistema o resetear permisos.
        """
        from .permissions import PermisosPorRol

        creados = 0
        actualizados = 0

        with transaction.atomic():
            for rol, permisos_rol in PermisosPorRol.PERMISOS.items():
                for modulo, permisos_modulo in permisos_rol.items():
                    permiso_obj, created = PermisoRol.objects.update_or_create(
                        rol=rol,
                        modulo=modulo,
                        defaults={
                            'permisos': permisos_modulo,
                            'descripcion_modulo': f'Permisos de {modulo} para {rol}'
                        }
                    )

                    if created:
                        creados += 1
                    else:
                        actualizados += 1

        return Response({
            'mensaje': 'Permisos inicializados correctamente',
            'creados': creados,
            'actualizados': actualizados,
            'total': creados + actualizados
        }, status=status.HTTP_200_OK)


