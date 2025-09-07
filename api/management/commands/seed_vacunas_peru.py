# 🇵🇪 COMANDO PARA SEED DE VACUNAS ESTÁNDAR PERÚ
from django.core.management.base import BaseCommand
from api.models import Vacuna

class Command(BaseCommand):
    help = 'Crea las vacunas estándar según protocolos peruanos (SENASA)'

    def handle(self, *args, **options):
        # Vacunas para PERROS según protocolos SENASA Perú
        vacunas_perros = [
            {
                'nombre': 'Quíntuple (DHPP)',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 6,
                'enfermedad_previene': 'Distemper, Hepatitis, Parvovirus, Parainfluenza, Adenovirus',
                'dosis_total': 3,
                'intervalo_dosis_semanas': 3,
                'estado': 'Activo'
            },
            {
                'nombre': 'Séxtuple (DHPPI+L)',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 6,
                'enfermedad_previene': 'Distemper, Hepatitis, Parvovirus, Parainfluenza, Adenovirus, Leptospirosis',
                'dosis_total': 3,
                'intervalo_dosis_semanas': 3,
                'estado': 'Activo'
            },
            {
                'nombre': 'Antirrábica Canina',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 16,
                'enfermedad_previene': 'Rabia',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0,
                'estado': 'Activo'
            },
            {
                'nombre': 'Bordetella (Tos de las Perreras)',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Bordetella bronchiséptica, Tos de las perreras',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0,
                'estado': 'Activo'
            },
            {
                'nombre': 'Parvovirus (Refuerzo)',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 4,
                'enfermedad_previene': 'Parvovirus canino',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0,
                'estado': 'Activo'
            }
        ]

        # Vacunas para GATOS según protocolos peruanos
        vacunas_gatos = [
            {
                'nombre': 'Triple Felina (FVRCP)',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 6,
                'enfermedad_previene': 'Rinotraqueítis, Calicivirus, Panleucopenia',
                'dosis_total': 3,
                'intervalo_dosis_semanas': 3,
                'estado': 'Activo'
            },
            {
                'nombre': 'Cuádruple Felina (FVRCP+C)',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 6,
                'enfermedad_previene': 'Rinotraqueítis, Calicivirus, Panleucopenia, Clamidiosis',
                'dosis_total': 3,
                'intervalo_dosis_semanas': 3,
                'estado': 'Activo'
            },
            {
                'nombre': 'Antirrábica Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 16,
                'enfermedad_previene': 'Rabia',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0,
                'estado': 'Activo'
            },
            {
                'nombre': 'Leucemia Felina (FeLV)',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Leucemia Felina',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 3,
                'estado': 'Activo'
            }
        ]

        # Vacunas para AMBAS ESPECIES
        vacunas_mixtas = [
            {
                'nombre': 'Antirrábica Multiespecies',
                'especies': ['Perro', 'Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 16,
                'enfermedad_previene': 'Rabia',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0,
                'estado': 'Activo'
            }
        ]

        # Crear vacunas
        vacunas_creadas = 0
        
        for lista_vacunas in [vacunas_perros, vacunas_gatos, vacunas_mixtas]:
            for data_vacuna in lista_vacunas:
                vacuna, created = Vacuna.objects.get_or_create(
                    nombre=data_vacuna['nombre'],
                    defaults=data_vacuna
                )
                
                if created:
                    vacunas_creadas += 1
                    especies_str = ', '.join(data_vacuna['especies'])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Creada: {data_vacuna["nombre"]} ({especies_str})'
                        )
                    )
                else:
                    especies_str = ', '.join(data_vacuna['especies'])
                    self.stdout.write(
                        self.style.WARNING(
                            f'Ya existe: {data_vacuna["nombre"]} ({especies_str})'
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nProceso completado: {vacunas_creadas} vacunas nuevas creadas'
            )
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Total de vacunas en sistema: {Vacuna.objects.count()}'
            )
        )
        
        self.stdout.write('\nSistema de vacunacion listo segun protocolos peruanos (SENASA)')