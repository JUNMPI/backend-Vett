from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
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
