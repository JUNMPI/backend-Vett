@echo off
echo ========================================
echo Activando entorno virtual...
echo ========================================
call env_veterinaria\Scripts\activate.bat

echo.
echo ========================================
echo Creando migraciones...
echo ========================================
python manage.py makemigrations --name="mejorar_sistema_slots"

echo.
echo ========================================
echo Aplicando migraciones...
echo ========================================
python manage.py migrate

echo.
echo ========================================
echo Migraciones completadas
echo ========================================
pause
