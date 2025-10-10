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
class TrabajadorSerializer(serializers.ModelSerializer):
    tipodocumento = serializers.PrimaryKeyRelatedField(queryset=TipoDocumento.objects.all())
    tipodocumento_nombre = serializers.CharField(source='tipodocumento.nombre', read_only=True)
    usuario = UsuarioSerializer()
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    # ✅ Email calculado desde Usuario (read-only para compatibilidad)
    email = serializers.EmailField(source='usuario.email', read_only=True)

    class Meta:
        model = Trabajador
        fields = [
            'id', 'nombres', 'apellidos', 'email', 'telefono',
            'tipodocumento', 'tipodocumento_nombre', 'documento', 'usuario', 'estado'
        ]

    def validate(self, attrs):
        """
        Validación completa: documento duplicado + formato según tipo (Perú)
        """
        import re
        from django.core.exceptions import ValidationError as CoreValidationError

        documento = attrs.get('documento')
        tipodocumento = attrs.get('tipodocumento')

        # Validar documento duplicado
        if documento and tipodocumento:
            # Verificar si ya existe otro trabajador con mismo documento y tipo
            query = Trabajador.objects.filter(
                documento=documento,
                tipodocumento=tipodocumento
            )
            if self.instance:
                query = query.exclude(id=self.instance.id)

            if query.exists():
                raise serializers.ValidationError({
                    "documento": "Ya existe un trabajador con este documento."
                })

            # Validar formato según tipo de documento (Perú)
            tipo = tipodocumento.nombre.upper()
            doc = documento.strip()

            # DNI: 8 dígitos exactos
            if tipo == 'DNI':
                if not re.match(r'^\d{8}$', doc):
                    raise serializers.ValidationError({
                        'documento': 'El DNI debe tener exactamente 8 dígitos.'
                    })

            # Carnet de Extranjería: 9 dígitos
            elif tipo in ['CE', 'CARNET DE EXTRANJERIA', 'CARNET DE EXTRANJERÍA']:
                if not re.match(r'^\d{9}$', doc):
                    raise serializers.ValidationError({
                        'documento': 'El Carnet de Extranjería debe tener 9 dígitos.'
                    })

            # Pasaporte: Alfanumérico, 9-12 caracteres
            elif tipo == 'PASAPORTE':
                if not re.match(r'^[A-Z0-9]{9,12}$', doc.upper()):
                    raise serializers.ValidationError({
                        'documento': 'El Pasaporte debe tener entre 9 y 12 caracteres alfanuméricos.'
                    })

            # RUC: 11 dígitos
            elif tipo == 'RUC':
                if not re.match(r'^\d{11}$', doc):
                    raise serializers.ValidationError({
                        'documento': 'El RUC debe tener exactamente 11 dígitos.'
                    })

        return attrs

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
            usuario_serializer = UsuarioSerializer(
                instance.usuario,
                data=usuario_data,
                partial=True
            )
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
    responsable_email = serializers.SerializerMethodField()
    historial_clinico = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Mascota
        fields = [
            'id', 'nombreMascota', 'especie', 'raza', 'fechaNacimiento',
            'genero', 'peso', 'color', 'observaciones',
            'responsable', 'nombrecompletoResponsable', 'responsable_email',
            'estado', 'historial_clinico'
        ]

    def get_nombrecompletoResponsable(self, obj):
        return f"{obj.responsable.nombres} {obj.responsable.apellidos}"

    def get_responsable_email(self, obj):
        return obj.responsable.email if obj.responsable and obj.responsable.email else None

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
    # ❌ ELIMINADO: usuario = UsuarioSerializer() (Responsable no tiene acceso al sistema)
    tipodocumento = serializers.PrimaryKeyRelatedField(queryset=TipoDocumento.objects.all())
    tipodocumento_nombre = serializers.CharField(source='tipodocumento.nombre', read_only=True)
    mascotas = MascotaSerializer(many=True, read_only=True)

    class Meta:
        model = Responsable
        fields = [
            'id', 'nombres', 'apellidos', 'email', 'telefono', 'direccion',
            'ciudad', 'documento', 'tipodocumento', 'tipodocumento_nombre',
            'emergencia', 'mascotas'
        ]

    def validate(self, attrs):
        """
        Validación completa: email único + documento duplicado + formato (Perú)
        """
        import re

        # Validar email único
        email = attrs.get('email')
        if email:
            query = Responsable.objects.filter(email=email)
            if self.instance:
                query = query.exclude(id=self.instance.id)

            if query.exists():
                raise serializers.ValidationError({
                    "email": "Este email ya está registrado por otro responsable."
                })

        # Validar documento único por tipo
        documento = attrs.get('documento')
        tipodocumento = attrs.get('tipodocumento')

        if documento and tipodocumento:
            query = Responsable.objects.filter(
                documento=documento,
                tipodocumento=tipodocumento
            )
            if self.instance:
                query = query.exclude(id=self.instance.id)

            if query.exists():
                raise serializers.ValidationError({
                    "documento": "Ya existe un responsable con este documento."
                })

            # Validar formato según tipo de documento (Perú)
            tipo = tipodocumento.nombre.upper()
            doc = documento.strip()

            # DNI: 8 dígitos exactos
            if tipo == 'DNI':
                if not re.match(r'^\d{8}$', doc):
                    raise serializers.ValidationError({
                        'documento': 'El DNI debe tener exactamente 8 dígitos.'
                    })

            # Carnet de Extranjería: 9 dígitos
            elif tipo in ['CE', 'CARNET DE EXTRANJERIA', 'CARNET DE EXTRANJERÍA']:
                if not re.match(r'^\d{9}$', doc):
                    raise serializers.ValidationError({
                        'documento': 'El Carnet de Extranjería debe tener 9 dígitos.'
                    })

            # Pasaporte: Alfanumérico, 9-12 caracteres
            elif tipo == 'PASAPORTE':
                if not re.match(r'^[A-Z0-9]{9,12}$', doc.upper()):
                    raise serializers.ValidationError({
                        'documento': 'El Pasaporte debe tener entre 9 y 12 caracteres alfanuméricos.'
                    })

            # RUC: 11 dígitos
            elif tipo == 'RUC':
                if not re.match(r'^\d{11}$', doc):
                    raise serializers.ValidationError({
                        'documento': 'El RUC debe tener exactamente 11 dígitos.'
                    })

        return attrs

    def create(self, validated_data):
        # ✅ Simplificado: No hay usuario
        responsable = Responsable.objects.create(**validated_data)
        return responsable

    def update(self, instance, validated_data):
        # ✅ Simplificado: Solo actualizar campos directos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def validate_email(self, value):
        """
        Validación adicional del campo email (por si acaso)
        """
        if value:
            # Verificar que el email sea único (excluyendo el instance actual en updates)
            if self.instance:
                # Es una actualización
                if Responsable.objects.filter(email=value).exclude(id=self.instance.id).exists():
                    raise serializers.ValidationError("Este email ya está registrado por otro responsable.")
            else:
                # Es una creación
                if Responsable.objects.filter(email=value).exists():
                    raise serializers.ValidationError("Este email ya está registrado.")

            # Validación adicional de formato (Django ya valida el formato básico)
            if len(value) > 254:
                raise serializers.ValidationError("El email es demasiado largo.")

        return value

class DiaTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaTrabajo
        fields = ['dia']

class VeterinarioSerializer(serializers.ModelSerializer):
    trabajador = serializers.PrimaryKeyRelatedField(queryset=Trabajador.objects.all())
    especialidad = serializers.PrimaryKeyRelatedField(queryset=Especialidad.objects.all())
    dias_trabajo = serializers.SerializerMethodField(read_only=True)  # Generado dinámicamente desde horarios_trabajo
    horarios_trabajo = serializers.SerializerMethodField(read_only=True)  # Sistema de horarios completo
    nombreEspecialidad = serializers.CharField(source='especialidad.nombre', read_only=True)
    trabajador_detalle = serializers.SerializerMethodField(read_only=True)
    especialidad_detalle = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Veterinario
        fields = ['id', 'trabajador', 'trabajador_detalle', 'especialidad', 'especialidad_detalle',
                  'nombreEspecialidad', 'dias_trabajo', 'horarios_trabajo']

    def get_dias_trabajo(self, obj):
        """
        Genera días_trabajo dinámicamente desde horarios_trabajo.
        Esto mantiene compatibilidad con frontend antiguo sin necesidad de tabla DiaTrabajo.
        """
        return obj.get_dias_trabajo_dinamicos()

    def get_horarios_trabajo(self, obj):
        """Obtener horarios de trabajo del veterinario"""
        horarios = obj.horarios_trabajo.filter(activo=True).order_by('dia_semana')
        return HorarioTrabajoSerializer(horarios, many=True).data

    def get_trabajador_detalle(self, obj):
        """Obtener detalle del trabajador"""
        return {
            'id': str(obj.trabajador.id),
            'nombres': obj.trabajador.nombres,
            'apellidos': obj.trabajador.apellidos,
            'email': obj.trabajador.email,
            'telefono': obj.trabajador.telefono,
            'documento': obj.trabajador.documento,
            'estado': obj.trabajador.estado
        }

    def get_especialidad_detalle(self, obj):
        """Obtener detalle de la especialidad"""
        if obj.especialidad:
            return {
                'id': str(obj.especialidad.id),
                'nombre': obj.especialidad.nombre,
                'estado': obj.especialidad.estado
            }
        return None

    # Ya no necesitamos create/update personalizados
    # dias_trabajo se genera automáticamente desde horarios_trabajo


class TipoDocumentoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = TipoDocumento
        fields = ['id', 'nombre', 'estado']


# Serializador para el modelo Servicio
class ServicioSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)
    categoria_display = serializers.CharField(source='get_categoria_display_custom', read_only=True)
    duracion_total = serializers.SerializerMethodField()
    permite_adicionales = serializers.SerializerMethodField()
    precio_fijo = serializers.SerializerMethodField()

    class Meta:
        model = Servicio
        fields = [
            'id', 'nombre', 'precio', 'estado', 'descripcion',
            'duracion_minutos', 'tiempo_preparacion', 'tiempo_limpieza',
            'prioridad', 'color', 'categoria', 'categoria_display',
            'duracion_total', 'permite_adicionales', 'precio_fijo',
            'requiere_consultorio_especial', 'permite_overlap'
        ]

    def get_duracion_total(self, obj):
        """Duración total incluyendo preparación y limpieza"""
        return obj.duracion_total_minutos()

    def get_permite_adicionales(self, obj):
        """Si este servicio permite agregar servicios/productos adicionales"""
        return obj.permite_servicios_adicionales()

    def get_precio_fijo(self, obj):
        """Si este servicio tiene precio fijo"""
        return obj.es_precio_fijo()

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

    def validate(self, attrs):
        """
        Validación personalizada que incluye validación de horarios de trabajo
        """
        # Crear instancia temporal para validar
        instance = Cita(**attrs)

        # Ejecutar validaciones del modelo (incluye validar_horario_trabajo)
        try:
            instance.full_clean()
        except Exception as e:
            # Convertir ValidationError de Django a DRF ValidationError
            from rest_framework import serializers as drf_serializers
            if hasattr(e, 'message_dict'):
                # Es un ValidationError con diccionario
                raise drf_serializers.ValidationError(e.message_dict)
            elif hasattr(e, 'messages'):
                # Es un ValidationError con lista de mensajes
                raise drf_serializers.ValidationError(e.messages[0] if e.messages else str(e))
            else:
                raise drf_serializers.ValidationError(str(e))

        return attrs

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


# 🐾 SERIALIZERS SISTEMA DE VACUNACIÓN

class VacunaSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)
    producto_inventario = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        required=False,
        allow_null=True
    )
    producto_inventario_info = serializers.SerializerMethodField()
    especies_aplicables = serializers.SerializerMethodField()
    
    class Meta:
        model = Vacuna
        fields = [
            'id', 'nombre', 'especies', 'especies_aplicables', 'frecuencia_meses', 'es_obligatoria',
            'edad_minima_semanas', 'enfermedad_previene', 'dosis_total',
            'intervalo_dosis_semanas', 'estado', 'producto_inventario',
            'producto_inventario_info', 'creado', 'actualizado',
            # 🆕 NUEVOS CAMPOS PARA PROTOCOLOS AVANZADOS
            'protocolo_dosis', 'max_dias_atraso', 'protocolo_cachorro'
        ]
    
    def get_especies_aplicables(self, obj):
        """Campo especies_aplicables que mapea al campo especies para compatibilidad con el frontend"""
        return obj.especies if obj.especies else []
    
    def get_producto_inventario_info(self, obj):
        """Información completa del producto de inventario relacionado"""
        if obj.producto_inventario:
            return {
                'id': str(obj.producto_inventario.id),
                'nombre': obj.producto_inventario.nombre,
                'stock': obj.producto_inventario.stock,
                'precio_venta': float(obj.producto_inventario.precio_venta) if obj.producto_inventario.precio_venta else None,
                'laboratorio': obj.producto_inventario.proveedor,
                'fecha_vencimiento': obj.producto_inventario.fecha_vencimiento
            }
        return None


class HistorialVacunacionSerializer(serializers.ModelSerializer):
    mascota = serializers.PrimaryKeyRelatedField(queryset=Mascota.objects.all())
    vacuna = serializers.PrimaryKeyRelatedField(queryset=Vacuna.objects.all())
    veterinario = serializers.PrimaryKeyRelatedField(queryset=Veterinario.objects.all())
    
    # Campos de solo lectura para mostrar información relacionada
    nombre_mascota = serializers.CharField(source='mascota.nombreMascota', read_only=True)
    nombre_vacuna = serializers.CharField(source='vacuna.nombre', read_only=True)
    nombre_veterinario = serializers.SerializerMethodField()
    esta_vencida = serializers.SerializerMethodField()
    dias_para_vencer = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()  # 🆕 Calcular estado dinámicamente
    
    class Meta:
        model = HistorialVacunacion
        fields = [
            'id', 'mascota', 'vacuna', 'fecha_aplicacion', 'proxima_fecha',
            'veterinario', 'lote', 'laboratorio', 'dosis_numero', 'observaciones',
            'estado', 'cita', 'creado', 'actualizado',
            # Campos de solo lectura
            'nombre_mascota', 'nombre_vacuna', 'nombre_veterinario',
            'esta_vencida', 'dias_para_vencer'
        ]
    
    def get_nombre_veterinario(self, obj):
        if obj.veterinario and obj.veterinario.trabajador:
            trabajador = obj.veterinario.trabajador
            return f"{trabajador.nombres} {trabajador.apellidos}"
        return "No asignado"
    
    def get_esta_vencida(self, obj):
        return obj.esta_vencida()
    
    def get_dias_para_vencer(self, obj):
        return obj.dias_para_vencer()

    def get_estado(self, obj):
        """
        🧠 CALCULAR ESTADO DINÁMICAMENTE según fechas actuales
        Garantiza que el estado siempre sea coherente con las fechas
        """
        from datetime import date

        # Si no hay próxima fecha, usar estado almacenado
        if not obj.proxima_fecha:
            return obj.estado

        today = date.today()
        dias_diferencia = (obj.proxima_fecha - today).days

        # 🔍 LÓGICA DE ESTADOS DINÁMICOS:

        # 1. VENCIDA: Próxima fecha ya pasó
        if dias_diferencia < 0:
            # Si está muy vencida (>60 días), podría necesitar reinicio
            if abs(dias_diferencia) > 60 and obj.vacuna.dosis_total > 1:
                return 'vencida_reinicio'
            return 'vencida'

        # 2. PRÓXIMA: Vence en los próximos 30 días
        elif 0 <= dias_diferencia <= 30:
            return 'proxima'

        # 3. VIGENTE: Vence en más de 30 días
        else:
            return 'vigente'


class HistorialMedicoSerializer(serializers.ModelSerializer):
    mascota = serializers.PrimaryKeyRelatedField(queryset=Mascota.objects.all())
    veterinario = serializers.PrimaryKeyRelatedField(queryset=Veterinario.objects.all())
    
    # Campos de solo lectura
    nombre_mascota = serializers.CharField(source='mascota.nombreMascota', read_only=True)
    nombre_veterinario = serializers.SerializerMethodField()
    
    class Meta:
        model = HistorialMedico
        fields = [
            'id', 'mascota', 'fecha', 'tipo', 'veterinario', 'motivo_consulta',
            'diagnostico', 'tratamiento_aplicado', 'medicamentos', 'proxima_cita',
            'peso_actual', 'temperatura', 'observaciones', 'cita', 'adjuntos',
            # Campos de solo lectura
            'nombre_mascota', 'nombre_veterinario'
        ]
    
    def get_nombre_veterinario(self, obj):
        if obj.veterinario and obj.veterinario.trabajador:
            trabajador = obj.veterinario.trabajador
            return f"{trabajador.nombres} {trabajador.apellidos}"
        return "No asignado"


# Serializer especializado para dashboard de vacunas
class VacunasAlertaSerializer(serializers.Serializer):
    """
    Serializer para alertas de vacunas en dashboard
    """
    mascota_id = serializers.UUIDField()
    nombre_mascota = serializers.CharField()
    vacuna_nombre = serializers.CharField()
    proxima_fecha = serializers.DateField()
    dias_vencimiento = serializers.IntegerField()
    estado = serializers.CharField()
    responsable_nombre = serializers.CharField()
    responsable_telefono = serializers.CharField()


# 🚀 SERIALIZERS PARA SISTEMA PROFESIONAL DE CITAS



class HorarioTrabajoSerializer(serializers.ModelSerializer):
    """
    Serializer para horarios de trabajo de veterinarios
    """
    veterinario_nombre = serializers.CharField(source='veterinario.__str__', read_only=True)
    dia_display = serializers.CharField(source='get_dia_semana_display', read_only=True)
    duracion_jornada = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HorarioTrabajo
        fields = [
            'id', 'veterinario', 'veterinario_nombre', 'dia_semana', 'dia_display',
            'hora_inicio', 'hora_fin', 'hora_inicio_descanso', 'hora_fin_descanso',
            'duracion_jornada', 'activo'
        ]
        read_only_fields = ['id']

    def get_duracion_jornada(self, obj):
        """Calcula la duración total de la jornada en horas"""
        from datetime import datetime, timedelta

        # Duración total del día
        inicio = datetime.combine(datetime.today(), obj.hora_inicio)
        fin = datetime.combine(datetime.today(), obj.hora_fin)
        duracion_total = (fin - inicio).total_seconds() / 3600

        # Restar descanso si existe
        if obj.hora_inicio_descanso and obj.hora_fin_descanso:
            descanso_inicio = datetime.combine(datetime.today(), obj.hora_inicio_descanso)
            descanso_fin = datetime.combine(datetime.today(), obj.hora_fin_descanso)
            duracion_descanso = (descanso_fin - descanso_inicio).total_seconds() / 3600
            duracion_total -= duracion_descanso

        return round(duracion_total, 2)

    def validate(self, data):
        """Validaciones personalizadas"""
        if data.get('hora_inicio') and data.get('hora_fin'):
            if data['hora_inicio'] >= data['hora_fin']:
                raise serializers.ValidationError({
                    'hora_fin': 'La hora de fin debe ser posterior a la hora de inicio'
                })

        # Validar horario de descanso
        if data.get('hora_inicio_descanso') and data.get('hora_fin_descanso'):
            if data['hora_inicio_descanso'] >= data['hora_fin_descanso']:
                raise serializers.ValidationError({
                    'hora_fin_descanso': 'La hora de fin del descanso debe ser posterior al inicio'
                })

            # El descanso debe estar dentro del horario laboral
            if (data['hora_inicio_descanso'] < data.get('hora_inicio', data['hora_inicio_descanso']) or
                data['hora_fin_descanso'] > data.get('hora_fin', data['hora_fin_descanso'])):
                raise serializers.ValidationError({
                    'hora_inicio_descanso': 'El descanso debe estar dentro del horario laboral'
                })

        return data


class SlotTiempoSerializer(serializers.ModelSerializer):
    """
    Serializer para slots de tiempo
    """
    veterinario_nombre = serializers.CharField(source='veterinario.__str__', read_only=True)
    disponible = serializers.BooleanField(read_only=True)
    cita_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SlotTiempo
        fields = [
            'id', 'veterinario', 'veterinario_nombre', 'fecha', 'hora_inicio', 'hora_fin',
            'disponible', 'cita_info', 'bloqueado', 'razon_bloqueo'
        ]
        read_only_fields = ['id']

    def get_cita_info(self, obj):
        """Información de la cita si el slot está ocupado"""
        if not obj.disponible and hasattr(obj, 'citas') and obj.citas.exists():
            cita = obj.citas.first()
            return {
                'id': cita.id,
                'mascota': cita.mascota.nombreMascota,
                'servicio': cita.servicio.nombre,
                'estado': cita.estado
            }
        return None


class CitaProfesionalSerializer(serializers.ModelSerializer):
    """
    Serializer extendido para citas con funcionalidades profesionales
    """
    mascota_nombre = serializers.CharField(source='mascota.nombreMascota', read_only=True)
    veterinario_nombre = serializers.CharField(source='veterinario.__str__', read_only=True)
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    tipo_cita_nombre = serializers.CharField(source='tipo_cita.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    # Campos calculados
    duracion_estimada = serializers.SerializerMethodField(read_only=True)
    tiempo_transcurrido = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cita
        fields = [
            'id', 'fecha', 'hora', 'mascota', 'mascota_nombre',
            'veterinario', 'veterinario_nombre', 'servicio', 'servicio_nombre',
            'estado', 'estado_display', 'notas'
        ]
        read_only_fields = ['id']

    def get_duracion_estimada(self, obj):
        """Duración estimada basada en el tipo de cita"""
        if hasattr(obj, 'tipo_cita') and obj.tipo_cita:
            return obj.tipo_cita.duracion_minutos
        return None

    def get_tiempo_transcurrido(self, obj):
        """Tiempo transcurrido desde la creación de la cita"""
        if hasattr(obj, 'fecha_creacion') and obj.fecha_creacion:
            from django.utils import timezone
            delta = timezone.now() - obj.fecha_creacion
            return delta.days
        return None


# 🛒 SERIALIZERS PARA SERVICIOS CATEGORIZADOS

class ServicioAdicionalSerializer(serializers.ModelSerializer):
    """
    Serializer para servicios/productos adicionales agregados a una cita
    """
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    tipo_item = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ServicioAdicional
        fields = [
            'id', 'cita', 'servicio', 'servicio_nombre',
            'producto', 'producto_nombre', 'tipo_item',
            'cantidad', 'precio_unitario', 'subtotal', 'notas', 'creado'
        ]
        read_only_fields = ['id', 'subtotal', 'creado']

    def get_tipo_item(self, obj):
        """Identifica si es un servicio o producto"""
        if obj.servicio:
            return 'servicio'
        elif obj.producto:
            return 'producto'
        return 'desconocido'


class DetalleCompletarCitaSerializer(serializers.ModelSerializer):
    """
    Serializer para detalles de completar cita específicos por categoría
    """
    categoria = serializers.CharField(source='cita.servicio.categoria', read_only=True)
    servicio_nombre = serializers.CharField(source='cita.servicio.nombre', read_only=True)
    mascota_nombre = serializers.CharField(source='cita.mascota.nombreMascota', read_only=True)
    veterinario_nombre = serializers.CharField(source='completado_por.__str__', read_only=True)
    servicios_adicionales = ServicioAdicionalSerializer(source='cita.servicios_adicionales', many=True, read_only=True)

    class Meta:
        model = DetalleCompletarCita
        fields = [
            'id', 'cita', 'categoria', 'servicio_nombre', 'mascota_nombre',
            # Campos específicos por categoría
            'indicaciones_bañado', 'tipo_pelaje', 'productos_especiales',
            'diagnostico', 'tratamiento_recomendado', 'observaciones_medicas',
            'proxima_cita_sugerida', 'observaciones_vacunacion',
            # Totales
            'subtotal_servicios', 'subtotal_productos', 'total_final',
            # Control
            'completado', 'completado_en', 'completado_por', 'veterinario_nombre',
            # Relaciones
            'servicios_adicionales',
            # Metadatos
            'creado', 'actualizado'
        ]
        read_only_fields = ['id', 'creado', 'actualizado']

    def validate(self, data):
        """Validación específica según categoría del servicio"""
        cita = data.get('cita')
        if cita:
            categoria = cita.servicio.categoria

            # Validaciones específicas por categoría
            if categoria == 'BAÑADO':
                if not data.get('tipo_pelaje'):
                    raise serializers.ValidationError({
                        'tipo_pelaje': 'El tipo de pelaje es requerido para servicios de baño.'
                    })

            elif categoria == 'CONSULTA':
                if not data.get('diagnostico'):
                    raise serializers.ValidationError({
                        'diagnostico': 'El diagnóstico es requerido para consultas médicas.'
                    })

        return data


# 🔄 SERIALIZER EXTENDIDO PARA CITAS

class CitaExtendidaSerializer(serializers.ModelSerializer):
    """
    Serializer extendido para citas con información de categorización
    """
    mascota_nombre = serializers.CharField(source='mascota.nombreMascota', read_only=True)
    veterinario_nombre = serializers.CharField(source='veterinario.__str__', read_only=True)
    servicio_info = ServicioSerializer(source='servicio', read_only=True)
    detalle = DetalleCompletarCitaSerializer(read_only=True)
    servicios_adicionales = ServicioAdicionalSerializer(many=True, read_only=True)

    # Campos calculados
    total_estimado = serializers.SerializerMethodField()
    puede_completar = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        fields = [
            'id', 'fecha', 'hora', 'mascota', 'mascota_nombre',
            'veterinario', 'veterinario_nombre', 'servicio', 'servicio_info',
            'estado', 'notas', 'detalle', 'servicios_adicionales',
            'total_estimado', 'puede_completar'
        ]

    def get_total_estimado(self, obj):
        """Calcula el total estimado incluyendo servicios adicionales"""
        total = obj.servicio.precio
        if hasattr(obj, 'servicios_adicionales'):
            total += sum(item.subtotal for item in obj.servicios_adicionales.all())
        return total

    def get_puede_completar(self, obj):
        """Determina si la cita puede ser completada"""
        return obj.estado in ['PENDIENTE', 'EN_PROCESO']


# ============================================
# SERIALIZERS PARA GESTIÓN DINÁMICA DE PERMISOS
# ============================================

class PermisoRolSerializer(serializers.ModelSerializer):
    """
    Serializer para gestión de permisos por rol.
    """
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)

    class Meta:
        model = PermisoRol
        fields = [
            'id', 'rol', 'rol_display', 'modulo', 'permisos',
            'descripcion_modulo', 'fecha_creacion', 'fecha_modificacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']

    def validate(self, data):
        """
        Validación personalizada:
        - Los permisos deben ser un diccionario
        - El rol debe existir en choices
        """
        if 'permisos' in data and not isinstance(data['permisos'], dict):
            raise serializers.ValidationError({
                'permisos': 'Los permisos deben ser un objeto JSON válido'
            })

        return data


class PermisoRolBulkUpdateSerializer(serializers.Serializer):
    """
    Serializer para actualización masiva de permisos.
    Permite actualizar múltiples permisos de un rol en una sola petición.
    """
    rol = serializers.ChoiceField(choices=Rol.ROL_CHOICES)
    permisos = serializers.ListField(
        child=serializers.DictField(),
        help_text="Lista de permisos a actualizar: [{'modulo': 'citas', 'permisos': {'ver': true}}, ...]"
    )

    def validate_permisos(self, value):
        """
        Validar que cada elemento tenga 'modulo' y 'permisos'
        """
        for item in value:
            if 'modulo' not in item or 'permisos' not in item:
                raise serializers.ValidationError(
                    "Cada permiso debe tener 'modulo' y 'permisos'"
                )
            if not isinstance(item['permisos'], dict):
                raise serializers.ValidationError(
                    "El campo 'permisos' debe ser un objeto JSON"
                )
        return value