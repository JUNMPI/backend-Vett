#!/usr/bin/env python3
"""
Script para corregir la indentación del método aplicar
"""

def fix_views_indentation():
    file_path = r"C:\Users\ASUS\Downloads\Veterinaria-Backend-Django (2)\Veterinaria-Backend-Django\api\views.py"

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Encontrar las líneas que necesitan corrección
    start_line = None
    end_line = None

    for i, line in enumerate(lines):
        if "# 🔍 DEBUG: Validar que la vacuna existe y tiene datos correctos" in line:
            start_line = i
        elif "def _aplicar_protocolo_completo_integrado" in line:
            end_line = i
            break

    if start_line is not None and end_line is not None:
        # Agregar 4 espacios de indentación a todas las líneas entre start_line y end_line
        for i in range(start_line, end_line):
            if lines[i].strip():  # No indentar líneas vacías
                # Si la línea ya empieza con espacios, agregar 4 más
                if lines[i].startswith('            '):
                    lines[i] = '    ' + lines[i]

        # Escribir el archivo corregido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(f"✅ Indentación corregida desde línea {start_line+1} hasta {end_line}")
    else:
        print("❌ No se encontraron las líneas de referencia")

if __name__ == "__main__":
    fix_views_indentation()