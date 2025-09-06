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



