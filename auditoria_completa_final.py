#!/usr/bin/env python3
"""
AUDITORIA COMPLETA Y FINAL DEL SISTEMA VETERINARIO
Verifica TODOS los casos posibles - No mas problemas
"""

import requests
import json
import uuid
from datetime import date, timedelta
import time
import random

class AuditoriaCompletaFinal:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api"
        self.resultados = []
        self.mascotas_creadas = []
        self.vacunaciones_realizadas = []

    def log_resultado(self, test_name, success, details=""):
        """Registra resultado de test"""
        resultado = {
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': time.strftime("%H:%M:%S")
        }
        self.resultados.append(resultado)
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {test_name}")
        if details:
            print(f"      -> {details}")
        return success

    def test_1_servidor_funcionando(self):
        """Verificar que el servidor Django responda"""
        try:
            response = requests.get(f"{self.base_url}/vacunas/", timeout=5)
            return self.log_resultado(
                "Servidor Django funcionando",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            return self.log_resultado("Servidor Django funcionando", False, str(e))

    def test_2_crear_mascota_simple(self):
        """Crear mascota sin vacunas - caso basico"""
        try:
            # Obtener responsable existente
            resp_responsables = requests.get(f"{self.base_url}/responsables/")
            responsables = resp_responsables.json()
            if not responsables:
                return self.log_resultado("Crear mascota simple", False, "No hay responsables disponibles")

            responsable_id = responsables[0]['id']

            mascota_data = {
                "nombreMascota": f"TestMascota_{random.randint(1000, 9999)}",
                "especie": "Perro",
                "raza": "Golden Retriever",
                "fechaNacimiento": "2023-01-15",
                "genero": "Macho",
                "peso": 25.5,
                "color": "Dorado",
                "responsable": responsable_id
            }

            response = requests.post(f"{self.base_url}/mascotas/", json=mascota_data)

            if response.status_code == 201:
                mascota = response.json()
                self.mascotas_creadas.append(mascota)
                return self.log_resultado(
                    "Crear mascota simple",
                    True,
                    f"Mascota creada: {mascota['nombreMascota']}"
                )
            else:
                return self.log_resultado(
                    "Crear mascota simple",
                    False,
                    f"Error {response.status_code}: {response.text}"
                )

        except Exception as e:
            return self.log_resultado("Crear mascota simple", False, str(e))

    def test_3_vacuna_dosis_individual_normal(self):
        """Aplicar dosis individual normal (caso tipico)"""
        if not self.mascotas_creadas:
            return self.log_resultado("Vacuna dosis individual", False, "No hay mascotas para testear")

        try:
            # Usar mascota creada
            mascota = self.mascotas_creadas[0]

            # Obtener vacuna estandar (2-3 dosis)
            resp_vacunas = requests.get(f"{self.base_url}/vacunas/")
            vacunas = resp_vacunas.json()['data']

            vacuna_normal = None
            for v in vacunas:
                if v['dosis_total'] <= 3 and v['estado'] == 'Activo':
                    vacuna_normal = v
                    break

            if not vacuna_normal:
                return self.log_resultado("Vacuna dosis individual", False, "No hay vacunas normales disponibles")

            # Obtener veterinario
            resp_vet = requests.get(f"{self.base_url}/veterinario-externo/")
            vet_data = resp_vet.json()

            # Aplicar primera dosis
            datos_vacuna = {
                "mascota_id": mascota['id'],
                "fecha_aplicacion": date.today().isoformat(),
                "dosis_numero": 1,
                "aplicar_protocolo_completo": False,
                "veterinario_id": vet_data['veterinario_id'],
                "observaciones": "Primera dosis - Test auditoria",
                "lote": "AUDIT_001"
            }

            response = requests.post(
                f"{self.base_url}/vacunas/{vacuna_normal['id']}/aplicar/",
                json=datos_vacuna
            )

            if response.status_code == 201:
                resultado = response.json()
                self.vacunaciones_realizadas.append({
                    'mascota': mascota['nombreMascota'],
                    'vacuna': vacuna_normal['nombre'],
                    'dosis': 1,
                    'resultado': resultado
                })
                return self.log_resultado(
                    "Vacuna dosis individual",
                    True,
                    f"Dosis 1 de {vacuna_normal['nombre']} aplicada"
                )
            else:
                return self.log_resultado(
                    "Vacuna dosis individual",
                    False,
                    f"Error {response.status_code}: {response.text}"
                )

        except Exception as e:
            return self.log_resultado("Vacuna dosis individual", False, str(e))

    def test_4_vacuna_dosis_9_de_10(self):
        """CASO ESPECIFICO: Dosis 9 de vacuna con 10 dosis total"""
        if not self.mascotas_creadas:
            return self.log_resultado("Vacuna dosis 9 de 10", False, "No hay mascotas para testear")

        try:
            mascota = self.mascotas_creadas[0]

            # Buscar vacuna con 10 dosis
            resp_vacunas = requests.get(f"{self.base_url}/vacunas/")
            vacunas = resp_vacunas.json()['data']

            vacuna_10_dosis = None
            for v in vacunas:
                if v['dosis_total'] == 10:
                    vacuna_10_dosis = v
                    break

            if not vacuna_10_dosis:
                return self.log_resultado("Vacuna dosis 9 de 10", False, "No hay vacuna con 10 dosis")

            # Obtener veterinario
            resp_vet = requests.get(f"{self.base_url}/veterinario-externo/")
            vet_data = resp_vet.json()

            # Aplicar dosis 9 (el caso problemático original)
            datos_vacuna = {
                "mascota_id": mascota['id'],
                "fecha_aplicacion": date.today().isoformat(),
                "dosis_numero": 9,  # CASO CRITICO
                "aplicar_protocolo_completo": False,
                "veterinario_id": vet_data['veterinario_id'],
                "observaciones": "Dosis 9 de 10 - Caso que antes fallaba",
                "lote": "AUDIT_DOSIS9"
            }

            response = requests.post(
                f"{self.base_url}/vacunas/{vacuna_10_dosis['id']}/aplicar/",
                json=datos_vacuna
            )

            if response.status_code == 201:
                resultado = response.json()
                return self.log_resultado(
                    "Vacuna dosis 9 de 10",
                    True,
                    f"EXITO: Dosis 9 de {vacuna_10_dosis['nombre']} aplicada correctamente"
                )
            else:
                return self.log_resultado(
                    "Vacuna dosis 9 de 10",
                    False,
                    f"FALLO: {response.status_code} - {response.text}"
                )

        except Exception as e:
            return self.log_resultado("Vacuna dosis 9 de 10", False, str(e))

    def test_5_vacuna_protocolo_largo(self):
        """Crear y testear vacuna con protocolo muy largo (15+ dosis)"""
        try:
            # Crear vacuna con protocolo largo
            nueva_vacuna = {
                "nombre": f"TEST_Protocolo_Largo_{random.randint(100, 999)}",
                "especies": ["Perro", "Gato"],
                "frecuencia_meses": 6,
                "es_obligatoria": False,
                "edad_minima_semanas": 8,
                "enfermedad_previene": "Protocolo de inmunizacion extensivo",
                "dosis_total": 15,  # PROTOCOLO LARGO
                "intervalo_dosis_semanas": 2,
                "estado": "Activo"
            }

            resp_create = requests.post(f"{self.base_url}/vacunas/", json=nueva_vacuna)

            if resp_create.status_code != 201:
                return self.log_resultado("Vacuna protocolo largo", False, f"No se pudo crear vacuna: {resp_create.text}")

            vacuna_larga = resp_create.json()['data']

            # Testear dosis 12 de 15
            if not self.mascotas_creadas:
                return self.log_resultado("Vacuna protocolo largo", False, "No hay mascotas para testear")

            mascota = self.mascotas_creadas[0]

            resp_vet = requests.get(f"{self.base_url}/veterinario-externo/")
            vet_data = resp_vet.json()

            # Aplicar dosis 12 de 15
            datos_vacuna = {
                "mascota_id": mascota['id'],
                "fecha_aplicacion": date.today().isoformat(),
                "dosis_numero": 12,  # DOSIS ALTA PERO VALIDA
                "aplicar_protocolo_completo": False,
                "veterinario_id": vet_data['veterinario_id'],
                "observaciones": "Dosis 12 de 15 - Protocolo largo",
                "lote": "AUDIT_LARGO"
            }

            response = requests.post(
                f"{self.base_url}/vacunas/{vacuna_larga['id']}/aplicar/",
                json=datos_vacuna
            )

            if response.status_code == 201:
                return self.log_resultado(
                    "Vacuna protocolo largo",
                    True,
                    f"Dosis 12 de 15 aplicada - {vacuna_larga['nombre']}"
                )
            else:
                return self.log_resultado(
                    "Vacuna protocolo largo",
                    False,
                    f"Error dosis 12: {response.status_code} - {response.text}"
                )

        except Exception as e:
            return self.log_resultado("Vacuna protocolo largo", False, str(e))

    def test_6_registro_con_multiples_vacunas(self):
        """Registrar mascota nueva con multiples vacunas atomicamente"""
        try:
            # Obtener responsable
            resp_responsables = requests.get(f"{self.base_url}/responsables/")
            responsables = resp_responsables.json()
            if not responsables:
                return self.log_resultado("Registro multiple vacunas", False, "No hay responsables")

            responsable_id = responsables[0]['id']

            # 1. Crear mascota
            mascota_data = {
                "nombreMascota": f"MultiVacuna_{random.randint(1000, 9999)}",
                "especie": "Perro",
                "raza": "Pastor Aleman",
                "fechaNacimiento": "2024-01-01",
                "genero": "Hembra",
                "peso": 30.0,
                "color": "Negro",
                "responsable": responsable_id
            }

            resp_mascota = requests.post(f"{self.base_url}/mascotas/", json=mascota_data)

            if resp_mascota.status_code != 201:
                return self.log_resultado("Registro multiple vacunas", False, f"Error creando mascota: {resp_mascota.text}")

            mascota = resp_mascota.json()
            self.mascotas_creadas.append(mascota)

            # 2. Aplicar multiple vacunas
            resp_vacunas = requests.get(f"{self.base_url}/vacunas/")
            vacunas = resp_vacunas.json()['data']

            resp_vet = requests.get(f"{self.base_url}/veterinario-externo/")
            vet_data = resp_vet.json()

            vacunas_aplicadas = 0
            errores = []

            # Seleccionar 3 vacunas diferentes
            vacunas_seleccionadas = [v for v in vacunas if v['estado'] == 'Activo'][:3]

            for i, vacuna in enumerate(vacunas_seleccionadas):
                datos_vacuna = {
                    "mascota_id": mascota['id'],
                    "fecha_aplicacion": date.today().isoformat(),
                    "dosis_numero": 1,
                    "aplicar_protocolo_completo": False,
                    "veterinario_id": vet_data['veterinario_id'],
                    "observaciones": f"Vacuna #{i+1} en registro multiple",
                    "lote": f"MULTI_{i+1}"
                }

                response = requests.post(
                    f"{self.base_url}/vacunas/{vacuna['id']}/aplicar/",
                    json=datos_vacuna
                )

                if response.status_code == 201:
                    vacunas_aplicadas += 1
                else:
                    errores.append(f"{vacuna['nombre']}: {response.status_code}")

            if vacunas_aplicadas == len(vacunas_seleccionadas):
                return self.log_resultado(
                    "Registro multiple vacunas",
                    True,
                    f"Mascota + {vacunas_aplicadas} vacunas aplicadas exitosamente"
                )
            else:
                return self.log_resultado(
                    "Registro multiple vacunas",
                    False,
                    f"Solo {vacunas_aplicadas}/{len(vacunas_seleccionadas)} vacunas. Errores: {errores}"
                )

        except Exception as e:
            return self.log_resultado("Registro multiple vacunas", False, str(e))

    def test_7_casos_extremos_validacion(self):
        """Testear casos extremos que DEBEN fallar"""
        if not self.mascotas_creadas:
            return self.log_resultado("Casos extremos", False, "No hay mascotas para testear")

        try:
            mascota = self.mascotas_creadas[0]

            resp_vacunas = requests.get(f"{self.base_url}/vacunas/")
            vacunas = resp_vacunas.json()['data']
            vacuna = vacunas[0]

            resp_vet = requests.get(f"{self.base_url}/veterinario-externo/")
            vet_data = resp_vet.json()

            casos_extremos = [
                {
                    "nombre": "Dosis 0 (inválida)",
                    "dosis": 0,
                    "debe_fallar": True
                },
                {
                    "nombre": "Dosis negativa",
                    "dosis": -1,
                    "debe_fallar": True
                },
                {
                    "nombre": "Dosis extrema (50)",
                    "dosis": 50,
                    "debe_fallar": True
                },
                {
                    "nombre": "Fecha futura",
                    "dosis": 1,
                    "fecha": (date.today() + timedelta(days=1)).isoformat(),
                    "debe_fallar": True
                }
            ]

            casos_exitosos = 0

            for caso in casos_extremos:
                datos_vacuna = {
                    "mascota_id": mascota['id'],
                    "fecha_aplicacion": caso.get("fecha", date.today().isoformat()),
                    "dosis_numero": caso["dosis"],
                    "aplicar_protocolo_completo": False,
                    "veterinario_id": vet_data['veterinario_id'],
                    "observaciones": f"Test caso extremo: {caso['nombre']}",
                    "lote": "EXTREMO"
                }

                response = requests.post(
                    f"{self.base_url}/vacunas/{vacuna['id']}/aplicar/",
                    json=datos_vacuna
                )

                # Si debe fallar y falla, o si no debe fallar y no falla = éxito
                caso_exitoso = (caso["debe_fallar"] and response.status_code != 201) or \
                              (not caso["debe_fallar"] and response.status_code == 201)

                if caso_exitoso:
                    casos_exitosos += 1

            return self.log_resultado(
                "Casos extremos",
                casos_exitosos == len(casos_extremos),
                f"{casos_exitosos}/{len(casos_extremos)} validaciones correctas"
            )

        except Exception as e:
            return self.log_resultado("Casos extremos", False, str(e))

    def test_8_alertas_dashboard(self):
        """Verificar que el dashboard de alertas funcione"""
        try:
            response = requests.get(f"{self.base_url}/dashboard/alertas-vacunacion/")

            if response.status_code == 200:
                alertas = response.json()
                return self.log_resultado(
                    "Dashboard alertas",
                    True,
                    f"Dashboard responde - {alertas.get('estadisticas', {}).get('total_alertas', 0)} alertas"
                )
            else:
                return self.log_resultado("Dashboard alertas", False, f"Error {response.status_code}")

        except Exception as e:
            return self.log_resultado("Dashboard alertas", False, str(e))

    def test_9_integridad_base_datos(self):
        """Verificar integridad de la base de datos"""
        try:
            # Verificar que todos los endpoints principales respondan
            endpoints = [
                "mascotas", "vacunas", "responsables", "veterinarios",
                "historial-vacunacion", "productos"
            ]

            endpoints_ok = 0

            for endpoint in endpoints:
                try:
                    response = requests.get(f"{self.base_url}/{endpoint}/", timeout=5)
                    if response.status_code == 200:
                        endpoints_ok += 1
                except:
                    pass

            return self.log_resultado(
                "Integridad base datos",
                endpoints_ok == len(endpoints),
                f"{endpoints_ok}/{len(endpoints)} endpoints funcionando"
            )

        except Exception as e:
            return self.log_resultado("Integridad base datos", False, str(e))

    def ejecutar_auditoria_completa(self):
        """Ejecutar toda la auditoría"""
        print("AUDITORIA COMPLETA DEL SISTEMA VETERINARIO")
        print("=" * 60)
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Ejecutar todos los tests
        tests = [
            self.test_1_servidor_funcionando,
            self.test_2_crear_mascota_simple,
            self.test_3_vacuna_dosis_individual_normal,
            self.test_4_vacuna_dosis_9_de_10,
            self.test_5_vacuna_protocolo_largo,
            self.test_6_registro_con_multiples_vacunas,
            self.test_7_casos_extremos_validacion,
            self.test_8_alertas_dashboard,
            self.test_9_integridad_base_datos
        ]

        tests_exitosos = 0

        for test in tests:
            if test():
                tests_exitosos += 1
            time.sleep(0.5)  # Pequeña pausa entre tests

        # Resumen final
        print("\n" + "=" * 60)
        print("RESUMEN FINAL DE LA AUDITORIA")
        print("=" * 60)

        porcentaje_exito = (tests_exitosos / len(tests)) * 100

        print(f"Tests ejecutados: {len(tests)}")
        print(f"Tests exitosos: {tests_exitosos}")
        print(f"Tests fallidos: {len(tests) - tests_exitosos}")
        print(f"Porcentaje de éxito: {porcentaje_exito:.1f}%")

        if tests_exitosos == len(tests):
            print("\nSISTEMA 100% OPERATIVO - NO HAY PROBLEMAS")
        else:
            print(f"\nSISTEMA TIENE {len(tests) - tests_exitosos} PROBLEMAS DETECTADOS:")
            for resultado in self.resultados:
                if not resultado['success']:
                    print(f"  - {resultado['test']}: {resultado['details']}")

        print(f"\nMascotas creadas durante testing: {len(self.mascotas_creadas)}")
        print(f"Vacunaciones realizadas: {len(self.vacunaciones_realizadas)}")

        return tests_exitosos == len(tests)

if __name__ == "__main__":
    auditoria = AuditoriaCompletaFinal()
    auditoria.ejecutar_auditoria_completa()