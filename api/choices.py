class Estado:
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    ESTADO_CHOICES = [
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    ]
class Disponibilidad:
    ABIERTO = "Abierto"
    CERRADO = "Cerrado"
    DISPONIBILIDAD_CHOICES = [
        (ABIERTO, 'Abierto'),
        (CERRADO, 'Cerrado'),
    ]
class Rol:
    RECEPCIONISTA = 'recepcionista'
    VETERINARIO = 'veterinario'
    VETERINARIO_EXTERNO = 'veterinario_externo'
    RESPONSABLE = 'Responsable'  # Dueño de mascota (legacy - mantener por compatibilidad)
    INVENTARIO = 'inventario'
    ADMINISTRADOR = 'administrador'

    ROL_CHOICES = [
        (RECEPCIONISTA, 'Recepcionista'),
        (VETERINARIO, 'Veterinario'),
        (VETERINARIO_EXTERNO, 'Veterinario Externo'),
        (RESPONSABLE, 'Responsable/Dueño'),  # Solo para usuarios de clientes
        (INVENTARIO, 'Inventario'),
        (ADMINISTRADOR, 'Administrador'),
    ]

class EstadoCita:
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"
    REPROGRAMADA = "reprogramada"

    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADA, 'Confirmada'),
        (COMPLETADA, 'Completada'),
        (CANCELADA, 'Cancelada'),
        (REPROGRAMADA, 'Reprogramada'),
    ]