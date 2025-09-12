from rest_framework import viewsets, status
from .models import *
from .serializers import *
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404

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
    
    @action(detail=True, methods=['post'], url_path='aplicar')
    def aplicar(self, request, pk=None):
        """
        🎯 ENDPOINT PRINCIPAL: Aplicar vacuna con cálculo automático inteligente
        URL: POST /api/vacunas/{id}/aplicar/
        Body: {
            "mascota_id": "uuid",
            "fecha_aplicacion": "2025-01-15",
            "dosis_numero": 1,
            "veterinario_id": "uuid",
            "observaciones": "",
            "lote": "ABC123"
        }
        """
        from datetime import date
        from dateutil.relativedelta import relativedelta
        from datetime import timedelta
        
        try:
            vacuna = self.get_object()  # Obtener vacuna por ID de la URL
            data = request.data
            
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
            
            # 🧠 LÓGICA 100% ROBUSTA - TODOS LOS CASOS EDGE CUBIERTOS
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
            
            # 🔧 FIX: Usar dosis_numero enviado por frontend, NO calcularlo automáticamente
            dosis_numero_frontend = data.get('dosis_numero', historial_count + 1)
            
            # 🛡️ VALIDACIONES ROBUSTAS DE DOSIS_NUMERO
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
            
            # ⭐ NUEVA VALIDACIÓN ESTRICTA: Dosis no puede exceder protocolo configurado
            # Para protocolo inicial (primeras dosis)
            if dosis_numero_frontend > vacuna.dosis_total:
                # Permitir solo si es un refuerzo anual (después de completar protocolo inicial)
                if historial_count < vacuna.dosis_total:
                    return Response({
                        'success': False,
                        'message': f'Dosis {dosis_numero_frontend} excede protocolo de {vacuna.nombre} ({vacuna.dosis_total} dosis máximo). Complete protocolo inicial primero.',
                        'error_code': 'DOSE_EXCEEDS_PROTOCOL',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Si ya completó el protocolo, limitar refuerzos a máximo 20 dosis totales
                if dosis_numero_frontend > 20:
                    return Response({
                        'success': False,
                        'message': f'Dosis {dosis_numero_frontend} demasiado alta. Máximo 20 dosis incluyendo refuerzos.',
                        'error_code': 'DOSE_LIMIT_EXCEEDED',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # ⭐ NUEVA VALIDACIÓN ANTI-DUPLICADOS: Prevenir múltiples aplicaciones
            # 1. No permitir misma vacuna el mismo día
            aplicaciones_hoy = HistorialVacunacion.objects.filter(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                fecha_aplicacion=fecha_aplicacion,
                estado__in=['aplicada', 'vigente', 'completado']
            )
            
            if aplicaciones_hoy.exists():
                return Response({
                    'success': False,
                    'message': f'Ya se aplicó {vacuna.nombre} a esta mascota el {fecha_aplicacion}. No se pueden aplicar múltiples dosis el mismo día.',
                    'error_code': 'DUPLICATE_VACCINE_SAME_DAY',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 2. Validar intervalo mínimo entre aplicaciones (7 días mínimo)
            from datetime import timedelta
            fecha_limite_reciente = fecha_aplicacion - timedelta(days=7)
            aplicaciones_recientes = HistorialVacunacion.objects.filter(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                fecha_aplicacion__gte=fecha_limite_reciente,
                fecha_aplicacion__lt=fecha_aplicacion,
                estado__in=['aplicada', 'vigente', 'completado']
            ).order_by('-fecha_aplicacion')
            
            if aplicaciones_recientes.exists():
                ultima_aplicacion = aplicaciones_recientes.first()
                dias_transcurridos = (fecha_aplicacion - ultima_aplicacion.fecha_aplicacion).days
                return Response({
                    'success': False,
                    'message': f'{vacuna.nombre} fue aplicada hace {dias_transcurridos} días ({ultima_aplicacion.fecha_aplicacion}). Debe esperar al menos 7 días entre aplicaciones.',
                    'error_code': 'VACCINE_TOO_SOON',
                    'status': 'error'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 3. Para vacunas de dosis única, validar que no tenga ya una aplicación vigente
            if vacuna.dosis_total == 1:
                aplicaciones_vigentes = HistorialVacunacion.objects.filter(
                    mascota_id=data['mascota_id'],
                    vacuna=vacuna,
                    estado__in=['aplicada', 'vigente'],
                    proxima_fecha__gte=fecha_aplicacion  # Aún vigente
                ).exclude(fecha_aplicacion=fecha_aplicacion)
                
                if aplicaciones_vigentes.exists():
                    aplicacion_vigente = aplicaciones_vigentes.first()
                    return Response({
                        'success': False,
                        'message': f'{vacuna.nombre} ya está vigente para esta mascota (aplicada: {aplicacion_vigente.fecha_aplicacion}, válida hasta: {aplicacion_vigente.proxima_fecha}). No necesita refuerzo aún.',
                        'error_code': 'VACCINE_STILL_VALID',
                        'status': 'error'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
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
            
            # 4. VERIFICAR DOSIS ATRASADAS CON PROTOCOLO INTELIGENTE
            ultima_aplicacion = historial_previo_query.last()
            if ultima_aplicacion and historial_count > 0:
                dias_desde_ultima = (fecha_aplicacion - ultima_aplicacion.fecha_aplicacion).days
                
                # Calcular máximo atraso permitido según el protocolo actual
                dosis_previa = historial_count  # La dosis anterior (1-based)
                
                if protocolo_info['intervalos'] and dosis_previa <= len(protocolo_info['intervalos']):
                    # Usar intervalo específico del protocolo
                    intervalo_esperado_semanas = protocolo_info['intervalos'][dosis_previa - 1]
                    max_atraso_dinamico = (intervalo_esperado_semanas * 7) + 21  # Intervalo + 3 semanas tolerancia
                else:
                    # Fallback: usar configuración base
                    max_atraso_dinamico = vacuna.max_dias_atraso
                
                if dias_desde_ultima > max_atraso_dinamico:
                    reiniciar_protocolo = True
                    HistorialVacunacion.objects.filter(
                        mascota_id=data['mascota_id'],
                        vacuna=vacuna,
                        estado__in=['aplicada', 'vigente']
                    ).update(estado='vencida_reinicio')
                    dosis_real_en_protocolo = 1  # Reiniciar como dosis 1
                    print(f"Protocolo reiniciado: {dias_desde_ultima} días > {max_atraso_dinamico} días permitidos")
            
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
            
            # 📝 Crear nuevo registro PRIMERO (sin marcar anteriores aún)
            historial = HistorialVacunacion.objects.create(
                mascota_id=data['mascota_id'],
                vacuna=vacuna,
                fecha_aplicacion=fecha_aplicacion,
                proxima_fecha=proxima_fecha,
                veterinario_id=data['veterinario_id'],
                dosis_numero=dosis_real_en_protocolo,  # ✅ Usar dosis calculada
                lote=data.get('lote', ''),
                observaciones=data.get('observaciones', ''),
                estado='vigente' if es_dosis_final else 'aplicada'  # Estado correcto
            )
            
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
            Q(proxima_fecha__lte=fecha_alerta, proxima_fecha__gte=date.today()) |   # Próximas a vencer (7 días)
            Q(estado='vencida_reinicio')  # 🆕 INCLUIR vacunas que necesitan reinicio
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
            
            # 🚨 MANEJAR ESTADO VENCIDA_REINICIO CON PRIORIDAD MÁXIMA
            if item.estado == 'vencida_reinicio':
                estado_alert = 'vencida'
                vencidas_count += 1
                prioridad = 'critica'  # Máxima prioridad para reinicio
                color = 'red'
            elif dias_restantes < 0:
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


@api_view(['GET'])
def get_veterinario_externo(request):
    """
    Obtener ID del veterinario externo creado automáticamente por migración
    Para casos de historial de vacunación previo
    URL: GET /api/veterinario-externo/
    """
    try:
        veterinario_externo = Veterinario.objects.get(
            trabajador__email='externo@veterinaria.com'
        )
        return Response({
            'veterinario_externo_id': str(veterinario_externo.id),
            'nombre': f"{veterinario_externo.trabajador.nombres} {veterinario_externo.trabajador.apellidos}",
            'mensaje': 'Veterinario para historial de vacunación externa'
        })
    except Veterinario.DoesNotExist:
        return Response({
            'error': 'Veterinario externo no encontrado. Verifica que la migración se ejecutó correctamente.'
        }, status=404)


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
