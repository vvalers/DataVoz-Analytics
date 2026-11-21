
# 1. Crear carpeta principal
mkdir DataVoz_Analytics

# 2. Entrar a la carpeta
cd DataVoz_Analytics

# 3. Crear archivos Python
New-Item app.py -ItemType File
New-Item analisis.py -ItemType File
New-Item validacion.py -ItemType File
New-Item test_analisis.py -ItemType File
New-Item requirements.txt -ItemType File
New-Item README.md -ItemType File

# 4. Crear carpeta data
mkdir data

# 5. Crear CSV
New-Item data\encuestas.csv -ItemType File

# 6. Crear entorno virtual
python -m venv .venv

# 7. Activar entorno
.\.venv\Scripts\Activate.ps1

# 8. Instalar librerías
python -m pip install pandas streamlit plotly pytest openpyxl

# 9. Abrir proyecto en VS Code
code .
