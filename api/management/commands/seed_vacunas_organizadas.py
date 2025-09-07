# seed_vacunas_organizadas.py
from django.core.management.base import BaseCommand
from api.models import Vacuna
from api.choices import Estado

class Command(BaseCommand):
    help = 'Crea 10 vacunas por especie (Perro, Gato, Ave) con datos organizados'

    def handle(self, *args, **options):
        # VACUNAS PARA PERROS (10)
        vacunas_perros = [
            {
                'nombre': 'Quintuple Canina',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Distemper, Hepatitis, Parainfluenza, Parvovirus, Adenovirus',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Antirrabica Canina',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 12,
                'enfermedad_previene': 'Rabia',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0
            },
            {
                'nombre': 'Sextuple Canina',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Distemper, Hepatitis, Parainfluenza, Parvovirus, Adenovirus, Coronavirus',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Tos de las Perreras',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 6,
                'enfermedad_previene': 'Bordetella bronchiseptica, Parainfluenza canina',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0
            },
            {
                'nombre': 'Leptospirosis Canina',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Leptospirosis (multiple serovares)',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 3
            },
            {
                'nombre': 'Parvovirus Canina',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 6,
                'enfermedad_previene': 'Parvovirus canino',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 3
            },
            {
                'nombre': 'Giardia Canina',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Giardia lamblia',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Distemper Canina',
                'especies': ['Perro'],
                'frecuencia_meses': 36,
                'es_obligatoria': True,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Moquillo canino (Distemper)',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Hepatitis Canina',
                'especies': ['Perro'],
                'frecuencia_meses': 36,
                'es_obligatoria': True,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Hepatitis infecciosa canina (Adenovirus tipo 1)',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Coronavirus Canina',
                'especies': ['Perro'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Coronavirus canino',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 3
            }
        ]

        # VACUNAS PARA GATOS (10)
        vacunas_gatos = [
            {
                'nombre': 'Triple Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Panleucopenia, Rinotraqueitis, Calicivirus',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Antirrabica Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 12,
                'enfermedad_previene': 'Rabia',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0
            },
            {
                'nombre': 'Leucemia Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Virus de la Leucemia Felina (FeLV)',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 3
            },
            {
                'nombre': 'Cuadruple Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Panleucopenia, Rinotraqueitis, Calicivirus, Clamidiosis',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Quintuple Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Panleucopenia, Rinotraqueitis, Calicivirus, Clamidiosis, Leucemia',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Panleucopenia Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 36,
                'es_obligatoria': True,
                'edad_minima_semanas': 6,
                'enfermedad_previene': 'Panleucopenia felina (Parvovirus felino)',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 3
            },
            {
                'nombre': 'Rinotraqueitis Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Herpesvirus felino tipo 1',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Calicivirus Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Calicivirus felino',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Clamidiosis Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 9,
                'enfermedad_previene': 'Chlamydia felis',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'PIF Felina',
                'especies': ['Gato'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 16,
                'enfermedad_previene': 'Peritonitis Infecciosa Felina',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 3
            }
        ]

        # VACUNAS PARA AVES (10)
        vacunas_aves = [
            {
                'nombre': 'Newcastle Aviar',
                'especies': ['Ave'],
                'frecuencia_meses': 6,
                'es_obligatoria': True,
                'edad_minima_semanas': 4,
                'enfermedad_previene': 'Enfermedad de Newcastle',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Viruela Aviar',
                'especies': ['Ave'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 6,
                'enfermedad_previene': 'Viruela aviar',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0
            },
            {
                'nombre': 'Bronquitis Infecciosa',
                'especies': ['Ave'],
                'frecuencia_meses': 6,
                'es_obligatoria': True,
                'edad_minima_semanas': 2,
                'enfermedad_previene': 'Bronquitis infecciosa aviar',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 3
            },
            {
                'nombre': 'Gumboro Aviar',
                'especies': ['Ave'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 3,
                'enfermedad_previene': 'Enfermedad de Gumboro',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 3
            },
            {
                'nombre': 'Influenza Aviar',
                'especies': ['Ave'],
                'frecuencia_meses': 6,
                'es_obligatoria': False,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Influenza aviar H5N1',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            },
            {
                'nombre': 'Laringotraqueitis Aviar',
                'especies': ['Ave'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 6,
                'enfermedad_previene': 'Laringotraqueitis infecciosa',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0
            },
            {
                'nombre': 'Coriza Infecciosa',
                'especies': ['Ave'],
                'frecuencia_meses': 6,
                'es_obligatoria': False,
                'edad_minima_semanas': 8,
                'enfermedad_previene': 'Haemophilus paragallinarum',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 3
            },
            {
                'nombre': 'Encefalomielitis Aviar',
                'especies': ['Ave'],
                'frecuencia_meses': 12,
                'es_obligatoria': True,
                'edad_minima_semanas': 4,
                'enfermedad_previene': 'Encefalomielitis aviar',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0
            },
            {
                'nombre': 'Sindrome Caida Postura',
                'especies': ['Ave'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 16,
                'enfermedad_previene': 'Sindrome de caida de postura',
                'dosis_total': 1,
                'intervalo_dosis_semanas': 0
            },
            {
                'nombre': 'Hepatitis Viral Patos',
                'especies': ['Ave'],
                'frecuencia_meses': 12,
                'es_obligatoria': False,
                'edad_minima_semanas': 4,
                'enfermedad_previene': 'Hepatitis viral de los patos',
                'dosis_total': 2,
                'intervalo_dosis_semanas': 4
            }
        ]

        # Crear todas las vacunas
        todas_vacunas = vacunas_perros + vacunas_gatos + vacunas_aves
        
        for vacuna_data in todas_vacunas:
            vacuna_data['estado'] = Estado.ACTIVO
            vacuna, created = Vacuna.objects.get_or_create(
                nombre=vacuna_data['nombre'],
                defaults=vacuna_data
            )
            if created:
                print(f'Creada: {vacuna.nombre} - {vacuna.especies}')
            else:
                print(f'Ya existe: {vacuna.nombre}')

        print(f'\nResumen:')
        print(f'Total vacunas creadas: {Vacuna.objects.count()}')
        print(f'Vacunas para Perros: {Vacuna.objects.filter(especies__contains=["Perro"]).count()}')
        print(f'Vacunas para Gatos: {Vacuna.objects.filter(especies__contains=["Gato"]).count()}')
        print(f'Vacunas para Aves: {Vacuna.objects.filter(especies__contains=["Ave"]).count()}')