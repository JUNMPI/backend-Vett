from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404
from rest_framework import status
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

    @action(detail=True, methods=['patch'], url_path='asignar-dias')
    def asignar_dias(self, request, pk=None):
        veterinario = self.get_object()
        dias = request.data.get('dias_trabajo', [])

        if not isinstance(dias, list):
            return Response({'error': 'Se requiere una lista de días.'}, status=status.HTTP_400_BAD_REQUEST)

        # Elimina días anteriores
        DiaTrabajo.objects.filter(veterinario=veterinario).delete()

        # Asigna nuevos días
        for dia in dias:
            DiaTrabajo.objects.create(veterinario=veterinario, dia=dia.upper())

        return Response({'status': 'Días asignados correctamente'})
    #buscar el terabajador por id de trabajador
    @action(detail=False, methods=['get'], url_path='por-trabajador/(?P<trabajador_id>[^/.]+)')
    def por_trabajador(self, request, trabajador_id=None):
        veterinario = get_object_or_404(Veterinario, trabajador__id=trabajador_id)
        serializer = self.get_serializer(veterinario)
        return Response(serializer.data)
    
# ViewSet for Service
class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

    # Filtra servicios activos por defecto
    def get_queryset(self):
        return Servicio.objects.all()

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
        Si se recibe query param 'veterinario_id', filtrar por ese vet;
        de lo contrario, devolver todas las citas.
        """
        vet_id = self.request.query_params.get('veterinario_id')
        if vet_id:
            return Cita.objects.filter(veterinario__id=vet_id)
        return Cita.objects.all()

    @action(detail=True, methods=['patch'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        """
        PATCH /api/citas/{id}/cambiar-estado/
        Body: { "estado": "<nuevo_estado>" }
        Solo admite uno de los valores definidos en EstadoCita.ESTADO_CHOICES.
        """
        cita = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado not in dict(EstadoCita.ESTADO_CHOICES).keys():
            return Response(
                {'error': f"Estado inválido: {nuevo_estado}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        cita.estado = nuevo_estado
        cita.save()
        return Response({'status': 'estado actualizado'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='reprogramar')
    def reprogramar(self, request, pk=None):
        """
        PATCH /api/citas/{id}/reprogramar/
        Body: { "fecha": "YYYY-MM-DD", "hora": "HH:MM:SS" }
        Cambia la fecha y hora y marca estado como "reprogramada".
        """
        cita = self.get_object()
        nueva_fecha = request.data.get('fecha')
        nueva_hora = request.data.get('hora')

        if not nueva_fecha or not nueva_hora:
            return Response(
                {'error': 'Se requieren "fecha" y "hora" para reprogramar.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cita.fecha = nueva_fecha
        cita.hora = nueva_hora
        cita.estado = EstadoCita.REPROGRAMADA
        cita.save()
        return Response({'status': 'cita reprogramada'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='por-veterinario/(?P<veterinario_id>[^/.]+)')
    def por_veterinario(self, request, veterinario_id=None):
        """
        GET /api/citas/por-veterinario/{veterinario_id}/
        Devuelve solo las citas asignadas al veterinario con ID {veterinario_id}.
        """
        citas_vet = Cita.objects.filter(veterinario__id=veterinario_id)
        serializer = self.get_serializer(citas_vet, many=True)
        return Response(serializer.data)


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


class HistorialVacunacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión del historial de vacunación
    """
    queryset = HistorialVacunacion.objects.all()
    serializer_class = HistorialVacunacionSerializer
    
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
            
            # Calcular próxima fecha basada en frecuencia de la vacuna
            proxima_fecha = fecha_aplicacion + relativedelta(months=vacuna.frecuencia_meses)
            
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
                
                return Response({
                    'data': self.get_serializer(historial).data,
                    'message': f'Vacuna {vacuna.nombre} aplicada exitosamente',
                    'proxima_vacuna': {
                        'fecha': proxima_fecha.isoformat(),
                        'dias_restantes': (proxima_fecha - date.today()).days,
                        'meses_frecuencia': vacuna.frecuencia_meses
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
        # 🧹 LIMPIEZA Y ACTUALIZACIÓN AUTOMÁTICA DE ESTADOS
        fecha_limpieza = date.today() - timedelta(days=7)
        fecha_hoy = date.today()
        fecha_proxima = date.today() + timedelta(days=7)
        
        # 1. Limpiar alertas vencidas hace más de 1 semana
        HistorialVacunacion.objects.filter(
            proxima_fecha__lte=fecha_limpieza,
            estado='vencida'
        ).update(estado='completado')
        
        # 2. Actualizar estados según fechas actuales
        # Marcar como vencidas las que pasaron su fecha
        HistorialVacunacion.objects.filter(
            proxima_fecha__lt=fecha_hoy,
            estado='aplicada'
        ).update(estado='vencida')
        
        # Marcar como próximas las que están en rango de alerta
        HistorialVacunacion.objects.filter(
            proxima_fecha__lte=fecha_proxima,
            proxima_fecha__gte=fecha_hoy,
            estado='aplicada'
        ).update(estado='proxima')
        
        # Vacunas próximas a vencer (próximos 7 días) y vencidas (máximo 1 semana atrás)
        fecha_alerta = date.today() + timedelta(days=7)
        fecha_vencida_limite = date.today() - timedelta(days=7)  # Solo mostrar vencidas de última semana
        
        alertas_query = HistorialVacunacion.objects.filter(
            Q(proxima_fecha__gte=fecha_vencida_limite, proxima_fecha__lt=date.today()) |  # Vencidas (máximo 1 semana)
            Q(proxima_fecha__lte=fecha_alerta, proxima_fecha__gte=date.today())   # Próximas a vencer (7 días)
        ).exclude(
            estado='completado'  # 🚫 EXCLUIR vacunas ya completadas/reemplazadas
        ).select_related(
            'mascota', 'vacuna', 'mascota__responsable', 'veterinario'
        ).order_by('proxima_fecha')
        
        alertas_data = []
        vencidas_count = 0
        proximas_count = 0
        
        for item in alertas_query:
            dias_restantes = (item.proxima_fecha - date.today()).days
            
            if dias_restantes < 0:
                estado_alert = 'vencida'
                vencidas_count += 1
                prioridad = 'alta'
                color = 'red'
            elif dias_restantes <= 2:
                estado_alert = 'critica'
                proximas_count += 1  
                prioridad = 'alta'
                color = 'orange'
            elif dias_restantes <= 7:
                estado_alert = 'proxima'
                proximas_count += 1
                prioridad = 'media'
                color = 'yellow'
            else:
                continue  # No incluir en alertas
            
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
                'estado': estado_alert,
                'prioridad': prioridad,
                'dosis_numero': item.dosis_numero,
                'responsable_nombre': f"{item.mascota.responsable.nombres} {item.mascota.responsable.apellidos}",
                'responsable_telefono': item.mascota.responsable.telefono,
                'veterinario_nombre': f"{item.veterinario.trabajador.nombres} {item.veterinario.trabajador.apellidos}" if item.veterinario else None,
                'color': color
            })
        
        # Estadísticas del resumen
        estadisticas = {
            'total_alertas': len(alertas_data),
            'vencidas': vencidas_count,
            'proximas': proximas_count,
            'criticas': len([a for a in alertas_data if a['prioridad'] == 'alta']),
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
