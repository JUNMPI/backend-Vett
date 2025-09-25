from django.db import models
from django.forms import ValidationError
from django.core.exceptions import ValidationError as CoreValidationError
from django.core.validators import RegexValidator
from .choices import *
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
from django.conf import settings
import secrets
import re

# Crear el modelo de Especialidad
class Especialidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )
    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# Crear el modelo de TipoDocumento
class TipoDocumento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=10, choices=Estado.ESTADO_CHOICES, default=Estado.ACTIVO)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# Definir los roles disponibles
class Rol(models.TextChoices):
    ADMINISTRADOR = 'Administrador'
    RECEPCIONISTA = 'Recepcionista'
    VETERINARIO = 'Veterinario'
    INVENTARIO = 'Inventario'
    RESPONSABLE = 'Responsable'


# Crear el modelo de Usuario
class Usuario(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)  # Usamos el correo como el identificador único
    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,  # Remove the parentheses here
        default=Rol.RECEPCIONISTA,  # Valor por defecto
    )
    
    # El campo 'username' no es necesario porque estamos usando el email
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No requerimos campos adicionales

    # Especificar `related_name` para evitar conflicto con el modelo por defecto `User`
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Cambiar el related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',  # Cambiar el related_name
        blank=True
    )

    def __str__(self):
        return f"{self.email} ({self.get_rol_display()})"

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['email']

# Crear el modelo de Trabajador
# En api/models.py, reemplaza la clase Trabajador existente

class Trabajador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    tipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, related_name='trabajadores')
    documento = models.CharField(max_length=20)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='trabajador')
    # 🆕 NUEVO CAMPO ESTADO
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )

    class Meta:
        ordering = ['nombres']

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
class Veterinario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trabajador = models.OneToOneField(Trabajador, on_delete=models.CASCADE, related_name='veterinario')
    especialidad = models.ForeignKey('Especialidad', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.trabajador.nombres} {self.trabajador.apellidos} - {self.especialidad.nombre}"
class DiaTrabajo(models.Model):
    DIA_CHOICES = [
        ('LUNES', 'Lunes'),
        ('MARTES', 'Martes'),
        ('MIERCOLES', 'Miércoles'),
        ('JUEVES', 'Jueves'),
        ('VIERNES', 'Viernes'),
        ('SABADO', 'Sábado'),
        ('DOMINGO', 'Domingo'),
    ]
    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE, related_name='dias_trabajo')
    dia = models.CharField(max_length=10, choices=DIA_CHOICES)

    class Meta:
        unique_together = ('veterinario', 'dia')
class Responsable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=254,
        unique=True,
        null=True,
        blank=True,
        help_text="Email del responsable",
        db_index=True  # Index para búsquedas rápidas
    )
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    tipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, related_name='responsables')
    emergencia = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='responsable')

    class Meta:
        ordering = ['nombres']

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# Validador de seguridad para nombres
def validate_safe_name(value):
    """
    Validador que previene SQL injection, XSS y otros ataques
    """
    if not value or not value.strip():
        raise CoreValidationError('El nombre no puede estar vacío.')

    # Longitud máxima
    if len(value) > 50:
        raise CoreValidationError('El nombre no puede exceder 50 caracteres.')

    # Patrones maliciosos
    malicious_patterns = [
        r'<script.*?>',  # XSS
        r'javascript:',  # XSS
        r'drop\s+table',  # SQL Injection
        r'delete\s+from',  # SQL Injection
        r'insert\s+into',  # SQL Injection
        r'update\s+set',  # SQL Injection
        r'union\s+select',  # SQL Injection
        r'--',  # SQL Comment
        r';.*drop',  # SQL Chain
        r'<.*>',  # HTML Tags
        r'eval\s*\(',  # Code injection
        r'exec\s*\(',  # Code injection
    ]

    value_lower = value.lower()
    for pattern in malicious_patterns:
        if re.search(pattern, value_lower, re.IGNORECASE):
            raise CoreValidationError(f'El nombre contiene contenido no permitido: {pattern}')

    # Solo permitir caracteres seguros
    safe_pattern = r'^[a-zA-Z0-9\s\-_.áéíóúÁÉÍÓÚñÑ]+$'
    if not re.match(safe_pattern, value):
        raise CoreValidationError('El nombre solo puede contener letras, números, espacios y caracteres básicos (-._)')

    return value

class Mascota(models.Model):
    GENERO_CHOICES = [
        ('Hembra', 'Hembra'),
        ('Macho', 'Macho'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreMascota = models.CharField(max_length=50, validators=[validate_safe_name])
    especie = models.CharField(max_length=100, validators=[validate_safe_name])
    raza = models.CharField(max_length=100, validators=[validate_safe_name])
    fechaNacimiento = models.DateField()
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=50, validators=[validate_safe_name])
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )
    responsable = models.ForeignKey(
        Responsable,
        on_delete=models.CASCADE,
        related_name='mascotas'
    )

    class Meta:
        ordering = ['nombreMascota']
        unique_together = ('nombreMascota', 'responsable')

    def clean(self):
        super().clean()

        # Validar fecha de nacimiento
        from datetime import date
        if self.fechaNacimiento:
            if self.fechaNacimiento > date.today():
                raise CoreValidationError({'fechaNacimiento': 'La fecha de nacimiento no puede ser futura.'})

            # No permitir fechas muy antiguas (más de 50 años)
            from datetime import timedelta
            fecha_limite = date.today() - timedelta(days=50*365)
            if self.fechaNacimiento < fecha_limite:
                raise CoreValidationError({'fechaNacimiento': 'La fecha de nacimiento es demasiado antigua.'})

        # Validar peso
        if self.peso is not None:
            if self.peso <= 0:
                raise CoreValidationError({'peso': 'El peso debe ser mayor a 0.'})
            if self.peso > 500:  # Peso máximo razonable
                raise CoreValidationError({'peso': 'El peso ingresado parece excesivo.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecutar validaciones antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombreMascota


class HistorialClinico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_historia = models.PositiveIntegerField(unique=True, editable=False)
    mascota = models.OneToOneField('Mascota', on_delete=models.CASCADE, related_name='historial_clinico')
    creado = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.numero_historia:
            self.numero_historia = self.generar_numero_historia()
        super().save(*args, **kwargs)

    def generar_numero_historia(self):
        for _ in range(10):  # Intentos para evitar colisión
            numero = secrets.randbelow(90000) + 10000  # entre 10000 y 99999
            if not HistorialClinico.objects.filter(numero_historia=numero).exists():
                return numero
        raise ValidationError("No se pudo generar un número de historia único.")

    def __str__(self):
        return f"Historial {self.numero_historia} - {self.mascota.nombreMascota}"

    class Meta:
        verbose_name = "Historial Clínico"
        verbose_name_plural = "Historias Clínicas"

class AtencionMedica(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    historial = models.ForeignKey(HistorialClinico, on_delete=models.CASCADE, related_name='atenciones')
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=255)
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField(blank=True, null=True)
    veterinario = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.fecha.date()} - {self.historial.mascota.nombreMascota}"

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Atención Médica"
        verbose_name_plural = "Atenciones Médicas"

class Vacunacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    historial = models.ForeignKey(
        HistorialClinico, 
        on_delete=models.CASCADE, 
        related_name='vacunas'
    )
    nombre_vacuna = models.CharField(max_length=100)
    fecha_aplicacion = models.DateField()
    proxima_dosis = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    veterinario = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre_vacuna} - {self.historial.mascota.nombreMascota}"

    class Meta:
        ordering = ['-fecha_aplicacion']
        verbose_name = "Vacunación"
        verbose_name_plural = "Vacunaciones"

class Producto(models.Model):
    CATEGORIAS = [
        ('medicamento', 'Medicamento'),
        ('vacuna', 'Vacuna'),
        ('higiene', 'Higiene y cuidado'),
        ('alimento', 'Alimento y suplemento'),
        ('venta', 'Producto para venta directa'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    proveedor = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=CATEGORIAS)
    subtipo = models.CharField(max_length=100, blank=True, null=True)
    stock = models.PositiveIntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )
    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# Crear el modelo de Servicio
class Servicio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )

    # 🚀 CAMPOS PROFESIONALES AGREGADOS
    descripcion = models.TextField(blank=True, help_text="Descripción detallada del servicio")

    # Configuración de tiempo
    duracion_minutos = models.IntegerField(
        default=30,
        help_text="Duración estimada en minutos"
    )
    tiempo_preparacion = models.IntegerField(
        default=5,
        help_text="Tiempo previo necesario para preparar (minutos)"
    )
    tiempo_limpieza = models.IntegerField(
        default=10,
        help_text="Tiempo posterior necesario para limpieza (minutos)"
    )

    # Configuración de prioridad y gestión
    prioridad = models.IntegerField(
        default=2,
        choices=[
            (1, 'Baja'),
            (2, 'Normal'),
            (3, 'Alta'),
            (4, 'Urgente'),
            (5, 'Crítica/Emergencia')
        ],
        help_text="Nivel de prioridad del servicio"
    )
    color = models.CharField(
        max_length=7,
        default='#3498db',
        help_text="Color hexadecimal para mostrar en calendario"
    )

    # Configuraciones adicionales
    requiere_consultorio_especial = models.BooleanField(
        default=False,
        help_text="Si requiere un consultorio específico (cirugías, etc.)"
    )
    permite_overlap = models.BooleanField(
        default=False,
        help_text="Si permite solapamiento con otras citas"
    )

    # 🎯 CATEGORIZACIÓN DE SERVICIOS
    CATEGORIA_CHOICES = [
        ('CONSULTA', 'Consulta Médica'),
        ('BAÑADO', 'Servicios de Baño'),
        ('VACUNACION', 'Vacunación'),
        ('CIRUGIA', 'Cirugía'),
        ('EMERGENCIA', 'Emergencia'),
    ]
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='CONSULTA',
        help_text="Categoría del servicio para flujo específico"
    )

    # Metadata
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return f"{self.nombre} (${self.precio} - {self.duracion_minutos}min)"

    def duracion_total_minutos(self):
        """Duración total incluyendo preparación y limpieza"""
        return self.duracion_minutos + self.tiempo_preparacion + self.tiempo_limpieza

    def es_emergencia(self):
        """Determina si es un servicio de emergencia"""
        return self.prioridad >= 4

    def get_categoria_display_custom(self):
        """Obtiene el display name de la categoría"""
        return dict(self.CATEGORIA_CHOICES).get(self.categoria, self.categoria)

    def permite_servicios_adicionales(self):
        """Determina si esta categoría permite agregar servicios adicionales"""
        return self.categoria in ['CONSULTA', 'VACUNACION']

    def es_precio_fijo(self):
        """Determina si el servicio tiene precio fijo (sin servicios adicionales)"""
        return self.categoria in ['BAÑADO']

class Consultorio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    disponible = models.CharField(
        max_length=10,
        choices=Disponibilidad.DISPONIBILIDAD_CHOICES,
        default=Disponibilidad.ABIERTO,
    )

    class Meta:
        verbose_name = 'Consultorio'
        verbose_name_plural = 'Consultorios'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"

class Cita(models.Model):
    """
    Modelo que representa una cita veterinaria.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField()
    hora = models.TimeField()
    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='citas'
    )

    # Relación con Veterinario (asumiendo que tu modelo Veterinario ya existe)
    veterinario = models.ForeignKey(
        'Veterinario',
        on_delete=models.CASCADE,
        related_name='citas'
    )
    # Relación con Servicio (asumiendo que tu modelo Servicio ya existe)
    servicio = models.ForeignKey(
        'Servicio',
        on_delete=models.CASCADE,
        related_name='citas'
    )

    estado = models.CharField(
        max_length=12,
        choices=EstadoCita.ESTADO_CHOICES,
        default=EstadoCita.PENDIENTE
    )
    notas = models.TextField(blank=True, null=True)


    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.fecha} {self.hora} — {self.mascota} ({self.get_estado_display()})"


# 🛒 MODELOS PARA SERVICIOS CATEGORIZADOS

class ServicioAdicional(models.Model):
    """
    Servicios/productos que se pueden agregar durante una cita
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='servicios_adicionales')

    # Puede ser un servicio o un producto del inventario
    servicio = models.ForeignKey(Servicio, null=True, blank=True, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', null=True, blank=True, on_delete=models.CASCADE)

    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(blank=True)

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Servicio Adicional'
        verbose_name_plural = 'Servicios Adicionales'
        ordering = ['-creado']

    def save(self, *args, **kwargs):
        """Calcula automáticamente el subtotal"""
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        if self.servicio:
            return f"{self.servicio.nombre} x{self.cantidad} = ${self.subtotal}"
        elif self.producto:
            return f"{self.producto.nombre} x{self.cantidad} = ${self.subtotal}"
        return f"Item adicional x{self.cantidad} = ${self.subtotal}"


class DetalleCompletarCita(models.Model):
    """
    Información específica al completar cada tipo de cita según su categoría
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name='detalle')

    # Para BAÑADO
    indicaciones_bañado = models.TextField(blank=True, help_text="Indicaciones especiales para el baño")
    tipo_pelaje = models.CharField(max_length=50, blank=True, help_text="Tipo de pelaje de la mascota")
    productos_especiales = models.TextField(blank=True, help_text="Productos especiales utilizados")

    # Para CONSULTA
    diagnostico = models.TextField(blank=True, help_text="Diagnóstico médico")
    tratamiento_recomendado = models.TextField(blank=True, help_text="Tratamiento recomendado")
    observaciones_medicas = models.TextField(blank=True, help_text="Observaciones médicas generales")

    # Para VACUNACIÓN
    proxima_cita_sugerida = models.DateField(null=True, blank=True, help_text="Próxima cita sugerida")
    observaciones_vacunacion = models.TextField(blank=True, help_text="Observaciones sobre vacunación")

    # Totales calculados
    subtotal_servicios = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal_productos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Control de completado
    completado = models.BooleanField(default=False)
    completado_en = models.DateTimeField(null=True, blank=True)
    completado_por = models.ForeignKey('Veterinario', null=True, blank=True, on_delete=models.SET_NULL)

    # Metadatos
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Detalle de Cita'
        verbose_name_plural = 'Detalles de Citas'
        ordering = ['-creado']

    def calcular_totales(self):
        """Calcula los totales basados en servicios adicionales"""
        servicios_adicionales = self.cita.servicios_adicionales.all()

        self.subtotal_servicios = sum([
            item.subtotal for item in servicios_adicionales if item.servicio
        ])

        self.subtotal_productos = sum([
            item.subtotal for item in servicios_adicionales if item.producto
        ])

        self.total_final = self.cita.servicio.precio + self.subtotal_servicios + self.subtotal_productos
        self.save()

    def __str__(self):
        return f"Detalle cita {self.cita.id} - {self.cita.servicio.categoria}"


# 🏥 SISTEMA DE CITAS PROFESIONAL - MODELOS AVANZADOS


class HorarioTrabajo(models.Model):
    """
    Horarios de trabajo por veterinario para gestión inteligente de agenda
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    veterinario = models.ForeignKey(
        'Veterinario',
        on_delete=models.CASCADE,
        related_name='horarios_trabajo'
    )

    # Configuración de días
    DIAS_SEMANA = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    dia_semana = models.IntegerField(
        choices=DIAS_SEMANA,
        help_text="Día de la semana (0=Lunes, 6=Domingo)"
    )

    # Horarios
    hora_inicio = models.TimeField(help_text="Hora de inicio de jornada")
    hora_fin = models.TimeField(help_text="Hora de fin de jornada")

    # Configuración de descansos
    tiene_descanso = models.BooleanField(
        default=False,
        help_text="¿Tiene descanso durante la jornada?"
    )
    hora_inicio_descanso = models.TimeField(
        null=True,
        blank=True,
        help_text="Hora de inicio del descanso"
    )
    hora_fin_descanso = models.TimeField(
        null=True,
        blank=True,
        help_text="Hora de fin del descanso"
    )

    # Control de actividad
    activo = models.BooleanField(
        default=True,
        help_text="¿Este horario está actualmente activo?"
    )
    fecha_inicio_vigencia = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha desde la cual es válido este horario"
    )
    fecha_fin_vigencia = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha hasta la cual es válido este horario"
    )

    # Metadatos
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['veterinario', 'dia_semana']
        ordering = ['veterinario', 'dia_semana']
        verbose_name = 'Horario de Trabajo'
        verbose_name_plural = 'Horarios de Trabajo'

    def __str__(self):
        return f"{self.veterinario} - {self.get_dia_semana_display()}: {self.hora_inicio}-{self.hora_fin}"


class SlotTiempo(models.Model):
    """
    Slots de tiempo disponibles para gestión inteligente de citas
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    veterinario = models.ForeignKey(
        'Veterinario',
        on_delete=models.CASCADE,
        related_name='slots_tiempo'
    )
    consultorio = models.ForeignKey(
        'Consultorio',
        on_delete=models.CASCADE,
        related_name='slots_tiempo',
        null=True,
        blank=True
    )

    # Tiempo
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    duracion_minutos = models.IntegerField(help_text="Duración calculada en minutos")

    # Disponibilidad
    disponible = models.BooleanField(default=True)
    motivo_no_disponible = models.CharField(
        max_length=200,
        blank=True,
        choices=[
            ('ocupado', 'Slot ocupado'),
            ('descanso', 'Tiempo de descanso'),
            ('mantenimiento', 'Mantenimiento de consultorio'),
            ('emergencia', 'Reservado para emergencias'),
            ('personal', 'Tiempo personal del veterinario'),
            ('otro', 'Otro motivo'),
        ]
    )

    # Configuración del slot
    servicio_permitido = models.ForeignKey(
        Servicio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Si se especifica, solo permite este tipo de servicio"
    )

    permite_emergencias = models.BooleanField(
        default=True,
        help_text="¿Este slot puede ser usado para emergencias?"
    )

    # Reserva temporal
    reservado_hasta = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Tiempo límite de reserva temporal (para evitar doble booking)"
    )

    # Metadatos
    generado_automaticamente = models.BooleanField(
        default=True,
        help_text="¿Este slot fue generado automáticamente?"
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['veterinario', 'consultorio', 'fecha', 'hora_inicio']
        ordering = ['fecha', 'hora_inicio']
        verbose_name = 'Slot de Tiempo'
        verbose_name_plural = 'Slots de Tiempo'
        indexes = [
            models.Index(fields=['fecha', 'disponible']),
            models.Index(fields=['veterinario', 'fecha']),
        ]

    def __str__(self):
        return f"{self.fecha} {self.hora_inicio}-{self.hora_fin} - {self.veterinario} ({'Disponible' if self.disponible else 'No disponible'})"


# 🐾 SISTEMA DE VACUNACIÓN - MODELOS PERÚ
class Vacuna(models.Model):
    """
    Catálogo de vacunas disponibles según protocolos peruanos (SENASA)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, help_text="Ej: Quíntuple, Antirrábica")
    especies = models.JSONField(
        default=list, 
        help_text="Especies aplicables: ['Perro', 'Gato']"
    )
    frecuencia_meses = models.IntegerField(
        help_text="Frecuencia en meses para refuerzo"
    )
    es_obligatoria = models.BooleanField(
        default=True, 
        help_text="¿Es obligatoria por ley peruana?"
    )
    edad_minima_semanas = models.IntegerField(
        default=6, 
        help_text="Edad mínima en semanas para primera aplicación"
    )
    enfermedad_previene = models.TextField(
        help_text="Enfermedades que previene"
    )
    dosis_total = models.IntegerField(
        default=1,
        help_text="Número total de dosis en el protocolo inicial"
    )
    intervalo_dosis_semanas = models.IntegerField(
        default=3,
        help_text="Semanas entre dosis del protocolo inicial"
    )
    
    # 🆕 PROTOCOLO EXTENSIBLE PARA CASOS COMPLEJOS
    protocolo_dosis = models.JSONField(
        default=list,
        blank=True,
        help_text="Protocolo detallado: [{'dosis': 1, 'semanas_siguiente': 3}, {'dosis': 2, 'semanas_siguiente': 4}] - Si está vacío, usa dosis_total e intervalo_dosis_semanas"
    )
    
    # 🆕 CONFIGURACIÓN DE DOSIS ATRASADAS  
    max_dias_atraso = models.IntegerField(
        default=14,
        help_text="Días máximos de atraso antes de reiniciar protocolo"
    )
    
    # 🆕 PROTOCOLO POR EDAD
    protocolo_cachorro = models.JSONField(
        default=dict,
        blank=True,
        help_text="Protocolo especial para cachorros: {'dosis_total': 4, 'intervalos': [3, 3, 4]} - Si está vacío, usa protocolo estándar"
    )
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )
    producto_inventario = models.ForeignKey(
        'Producto',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Relación con el producto en inventario"
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Vacuna'
        verbose_name_plural = 'Vacunas'

    def __str__(self):
        especies_str = ', '.join(self.especies) if self.especies else 'Todas'
        return f"{self.nombre} ({especies_str})"


class HistorialVacunacion(models.Model):
    """
    Historial individual de vacunación por mascota
    """
    ESTADO_CHOICES = [
        ('vigente', 'Vigente'),
        ('vencida', 'Vencida'),
        ('proxima', 'Próxima'),
        ('aplicada', 'Aplicada'),
        ('completado', 'Completado'),  # 🆕 Para marcar vacunas reemplazadas/actualizadas
        ('vencida_reinicio', 'Vencida - Protocolo Reiniciado')  # 🆕 Para dosis atrasadas que requieren reinicio
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mascota = models.ForeignKey(
        'Mascota',
        on_delete=models.CASCADE,
        related_name='historial_vacunacion'
    )
    vacuna = models.ForeignKey(
        'Vacuna',
        on_delete=models.CASCADE,
        related_name='aplicaciones'
    )
    fecha_aplicacion = models.DateField(
        null=True, blank=True,
        help_text="Fecha real de aplicación (NULL para dosis pendientes)"
    )
    proxima_fecha = models.DateField(
        help_text="Próxima fecha calculada automáticamente"
    )
    veterinario = models.ForeignKey(
        'Veterinario',
        on_delete=models.CASCADE,
        related_name='vacunas_aplicadas'
    )
    lote = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Lote de la vacuna aplicada"
    )
    laboratorio = models.CharField(
        max_length=100,
        blank=True,
        help_text="Laboratorio fabricante"
    )
    dosis_numero = models.IntegerField(
        default=1,
        help_text="Número de dosis en el protocolo (1ra, 2da, etc.)"
    )
    observaciones = models.TextField(
        blank=True,
        help_text="Observaciones del veterinario"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='aplicada'
    )
    cita = models.ForeignKey(
        'Cita',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Cita en la que se aplicó la vacuna"
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_aplicacion']
        verbose_name = 'Historial de Vacunación'
        verbose_name_plural = 'Historiales de Vacunación'

    def __str__(self):
        return f"{self.mascota} - {self.vacuna} ({self.fecha_aplicacion})"

    # NOTA: El cálculo de proxima_fecha se hace en views.py/aplicar() con lógica inteligente
    # No usar save() override para evitar conflictos con la lógica compleja

    def esta_vencida(self):
        """Verifica si la vacuna está vencida"""
        from datetime import date
        return self.proxima_fecha < date.today() if self.proxima_fecha else False

    def dias_para_vencer(self):
        """Días restantes para que venza la vacuna"""
        from datetime import date
        if self.proxima_fecha:
            delta = self.proxima_fecha - date.today()
            return delta.days
        return None


class HistorialMedico(models.Model):
    """
    Historial médico completo por mascota (consultas, tratamientos, etc.)
    """
    TIPO_CHOICES = [
        ('vacuna', 'Vacunación'),
        ('desparasitacion_interna', 'Desparasitación Interna'),
        ('desparasitacion_externa', 'Desparasitación Externa'),
        ('control_general', 'Control General'),
        ('tratamiento', 'Tratamiento Específico'),
        ('cirugia', 'Cirugía'),
        ('emergencia', 'Emergencia'),
        ('revision', 'Revisión de Rutina')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mascota = models.ForeignKey(
        'Mascota',
        on_delete=models.CASCADE,
        related_name='historial_medico'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
        default='control_general'
    )
    veterinario = models.ForeignKey(
        'Veterinario',
        on_delete=models.CASCADE,
        related_name='atenciones_realizadas'
    )
    motivo_consulta = models.TextField(
        help_text="Motivo de la consulta"
    )
    diagnostico = models.TextField(
        blank=True,
        help_text="Diagnóstico del veterinario"
    )
    tratamiento_aplicado = models.TextField(
        blank=True,
        help_text="Tratamiento o procedimiento realizado"
    )
    medicamentos = models.TextField(
        blank=True,
        help_text="Medicamentos recetados"
    )
    proxima_cita = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha recomendada para próxima cita"
    )
    peso_actual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Peso registrado durante la consulta"
    )
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Temperatura corporal en °C"
    )
    observaciones = models.TextField(
        blank=True,
        help_text="Observaciones adicionales"
    )
    cita = models.ForeignKey(
        'Cita',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Cita asociada a este registro"
    )
    adjuntos = models.JSONField(
        default=list,
        blank=True,
        help_text="URLs de archivos adjuntos (radiografías, análisis, etc.)"
    )

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Historial Médico'
        verbose_name_plural = 'Historiales Médicos'

    def __str__(self):
        return f"{self.mascota} - {self.get_tipo_display()} ({self.fecha.strftime('%d/%m/%Y')})"


