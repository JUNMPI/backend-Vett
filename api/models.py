from django.db import models
from django.forms import ValidationError
from .choices import *
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
import secrets

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

class Mascota(models.Model):
    GENERO_CHOICES = [
        ('Hembra', 'Hembra'),
        ('Macho', 'Macho'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreMascota = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=50)
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

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

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
        ('completado', 'Completado')  # 🆕 Para marcar vacunas reemplazadas/actualizadas
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
        help_text="Fecha real de aplicación"
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

    def save(self, *args, **kwargs):
        # Calcular automáticamente la próxima fecha
        if self.fecha_aplicacion and self.vacuna:
            from datetime import timedelta
            dias_proxima = self.vacuna.frecuencia_meses * 30  # Aproximación
            self.proxima_fecha = self.fecha_aplicacion + timedelta(days=dias_proxima)
        
        super().save(*args, **kwargs)

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


