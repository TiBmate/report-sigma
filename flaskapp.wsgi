import sys
import os
import logging

# Configura la salida de log para errores
logging.basicConfig(stream=sys.stderr)

# Establecer el directorio de trabajo
os.chdir('/var/www/html')

# Agrega el directorio de la aplicación al path de Python
sys.path.insert(0, "/var/www/html")

# Importa la aplicación Flask
from app import app as application