# serializers.py
from rest_framework import serializers
from .models import *
from .choices import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class EspecialidadSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = Especialidad
        fields = ['id', 'nombre', 'estado']


# Serializador para el modelo TipoDocumento
class TipoDocumentoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = TipoDocumento
        fields = ['id', 'nombre', 'estado']


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'password', 'rol']
        extra_kwargs = {
            'email': {'validators': []},  # 🔧 Desactiva el validador automático de unicidad
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = Usuario.objects.create(**validated_data)
        if password:
            usuario.set_password(password)
            usuario.save()
        return usuario

    def update(self, instance, validated_data):
        email = validated_data.get('email')
        if email and email != instance.email:
            if Usuario.objects.filter(email=email).exclude(pk=instance.pk).exists():
                raise serializers.ValidationError({"email": "Este correo ya está en uso."})

        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rol'] = instance.get_rol_display()
        return representation
    
# Serializador para el modelo Trabajador
# En api/serializers.py, reemplaza TrabajadorSerializer existente

class TrabajadorSerializer(serializers.ModelSerializer):
    tipodocumento = serializers.PrimaryKeyRelatedField(queryset=TipoDocumento.objects.all())
    tipodocumento_nombre = serializers.CharField(source='tipodocumento.nombre', read_only=True)
    usuario = UsuarioSerializer()
    # 🆕 NUEVO CAMPO ESTADO
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = Trabajador
        fields = [
            'id', 'nombres', 'apellidos', 'email', 'telefono',
            'tipodocumento', 'tipodocumento_nombre', 'documento', 'usuario', 'estado'  # 🆕 Agregado estado
        ]

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        usuario_serializer = UsuarioSerializer(data=usuario_data)
        usuario_serializer.is_valid(raise_exception=True)
        usuario = usuario_serializer.save()

        trabajador = Trabajador.objects.create(usuario=usuario, **validated_data)
        return trabajador

    def update(self, instance, validated_data):
        usuario_data = validated_data.pop('usuario', None)

        if usuario_data:
            usuario_serializer = UsuarioSerializer(instance.usuario, data=usuario_data, partial=True)
            usuario_serializer.is_valid(raise_exception=True)
            usuario_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class VacunacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacunacion
        fields = '__all__'


class AtencionMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtencionMedica
        fields = '__all__'


class HistorialClinicoSerializer(serializers.ModelSerializer):
    creado = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    vacunas = VacunacionSerializer(many=True, read_only=True)
    atenciones = AtencionMedicaSerializer(many=True, read_only=True)
    mascota_nombre = serializers.CharField(source='mascota.nombreMascota', read_only=True)

    class Meta:
        model = HistorialClinico
        fields = ['id', 'numero_historia', 'creado', 'mascota', 'mascota_nombre', 'vacunas', 'atenciones']


class MascotaSerializer(serializers.ModelSerializer):
    responsable = serializers.PrimaryKeyRelatedField(queryset=Responsable.objects.all())
    nombrecompletoResponsable = serializers.SerializerMethodField()
    historial_clinico = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Mascota
        fields = [
            'id', 'nombreMascota', 'especie', 'raza', 'fechaNacimiento',
            'genero', 'peso', 'color', 'observaciones',
            'responsable', 'nombrecompletoResponsable',
            'estado', 'historial_clinico'
        ]

    def get_nombrecompletoResponsable(self, obj):
        return f"{obj.responsable.nombres} {obj.responsable.apellidos}"

    def get_historial_clinico(self, obj):
        try:
            return HistorialClinicoSerializer(obj.historial_clinico).data
        except HistorialClinico.DoesNotExist:
            return None

    def create(self, validated_data):
        mascota = Mascota.objects.create(**validated_data)
        HistorialClinico.objects.create(mascota=mascota)
        return mascota

class ResponsableSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    tipodocumento_nombre = serializers.CharField(source='tipodocumento.nombre', read_only=True)
    mascotas = MascotaSerializer(many=True, read_only=True)  # Agregamos las mascotas relacionadas

    class Meta:
        model = Responsable
        fields = [
            'id', 'nombres', 'apellidos', 'telefono', 'direccion',
            'ciudad', 'documento', 'tipodocumento','tipodocumento_nombre', 'emergencia', 'usuario','mascotas'
        ]

    def create(self, validated_data):
        # Extraemos los datos del usuario del campo 'usuario'
        usuario_data = validated_data.pop('usuario')

        # Creamos el usuario usando el serializer
        usuario_serializer = UsuarioSerializer(data=usuario_data)
        usuario_serializer.is_valid(raise_exception=True)  # Verificamos si los datos son válidos
        usuario = usuario_serializer.save()  # Guardamos el usuario

        # Creamos el Responsable y asignamos el usuario
        responsable = Responsable.objects.create(usuario=usuario, **validated_data)
        return responsable

    def update(self, instance, validated_data):
        usuario_data = validated_data.pop('usuario', None)

        if usuario_data:
            # Actualizamos el usuario si hay datos nuevos
            usuario_serializer = UsuarioSerializer(instance.usuario, data=usuario_data, partial=True)
            usuario_serializer.is_valid(raise_exception=True)
            usuario_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class DiaTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaTrabajo
        fields = ['dia']

class VeterinarioSerializer(serializers.ModelSerializer):
    trabajador = serializers.PrimaryKeyRelatedField(queryset=Trabajador.objects.all())
    especialidad = serializers.PrimaryKeyRelatedField(queryset=Especialidad.objects.all())
    dias_trabajo = DiaTrabajoSerializer(many=True, required=False, allow_null=True)  # Usar el serializador anidado
    nombreEspecialidad = serializers.CharField(source='especialidad.nombre', read_only=True)
    class Meta:
        model = Veterinario
        fields = ['id', 'trabajador', 'especialidad','nombreEspecialidad', 'dias_trabajo']  # Incluir dias_trabajo

    def create(self, validated_data):
        dias_trabajo_data = validated_data.pop('dias_trabajo', [])
        veterinario = Veterinario.objects.create(**validated_data)
        
        # Asociar los días de trabajo si se proporcionaron
        for dia_data in dias_trabajo_data:
            DiaTrabajo.objects.create(veterinario=veterinario, dia=dia_data['dia'])
        
        return veterinario

    def update(self, instance, validated_data):
        dias_trabajo_data = validated_data.pop('dias_trabajo', [])
        
        # Actualiza el veterinario
        instance.trabajador = validated_data.get('trabajador', instance.trabajador)
        instance.especialidad = validated_data.get('especialidad', instance.especialidad)
        instance.save()
        
        # Actualizar los días de trabajo si se proporcionaron (puedes borrarlos y crear nuevos)
        if dias_trabajo_data:
            instance.dias_trabajo.all().delete()
            for dia_data in dias_trabajo_data:
                DiaTrabajo.objects.create(veterinario=instance, dia=dia_data['dia'])
        
        return instance


class TipoDocumentoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = TipoDocumento
        fields = ['id', 'nombre', 'estado']


# Serializador para el modelo Servicio
class ServicioSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'precio', 'estado']

class ProductoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'proveedor', 
                  'tipo', 'subtipo','stock','precio_compra','precio_venta','fecha_vencimiento','estado']


class CitaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Cita.
    Relaciona veterinario y servicio mediante su ID (PK).
    """
    veterinario = serializers.PrimaryKeyRelatedField(queryset=Veterinario.objects.all())
    servicio = serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all())
    mascota = serializers.PrimaryKeyRelatedField(queryset=Mascota.objects.all())
    #Obtner la mombre del veterinario
    nombreVeterinario = serializers.SerializerMethodField()
    #Obtener el nombre del servicio
    nombreServicio = serializers.CharField(source='servicio.nombre', read_only=True)
    #Obtener el nombre de la mascota
    nombreMascota = serializers.CharField(source='mascota.nombreMascota', read_only=True)
    #Obtener el nombre del propietario
    nombrePropietario = serializers.SerializerMethodField()  # 👈 Nuevo campo

    class Meta:
        model = Cita
        fields = [
            'id',
            'fecha',
            'hora',
            'mascota',
            'nombreMascota',
            'nombrePropietario',  # 👈 Nuevo campo

            'veterinario',
            'nombreVeterinario',
            'servicio',
            'nombreServicio',
            'estado',
            'notas'
        ]
        read_only_fields = ['id']
    def get_nombreVeterinario(self, obj):
        nombres = getattr(obj.veterinario.trabajador, 'nombres', '')
        apellidos = getattr(obj.veterinario.trabajador, 'apellidos', '')
        especialidad = getattr(obj.veterinario, 'especialidad', 'Sin especialidad')
        return f"{nombres} {apellidos} (Especialidad: {especialidad})"
    def get_nombrePropietario(self, obj):
        # Obtener el nombre completo del propietario de la mascota
        try:
            mascota = Mascota.objects.get(id=obj.mascota.id)
            return f"{mascota.responsable.nombres} {mascota.responsable.apellidos}"
        except Mascota.DoesNotExist:
            return "Propietario no encontrado"
        
class ConsultorioSerializer(serializers.ModelSerializer):
    disponible = serializers.ChoiceField(
        choices=Disponibilidad.DISPONIBILIDAD_CHOICES,
        required=False,
        default=Disponibilidad.ABIERTO
    )

    class Meta:
        model = Consultorio
        fields = ['id', 'nombre', 'ubicacion', 'disponible']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['rol'] = user.rol
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'usuario_id': str(self.user.id),
            'email': self.user.email,
            'rol': self.user.rol,
        })
        if hasattr(self.user, 'trabajador'):
            data['trabajador_id'] = str(self.user.trabajador.id)
            data['nombres'] = self.user.trabajador.nombres
            data['apellidos'] = self.user.trabajador.apellidos
        return data