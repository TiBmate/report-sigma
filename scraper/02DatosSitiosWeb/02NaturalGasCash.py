from playwright.sync_api import sync_playwright, TimeoutError
import csv
import os
import logging
from bs4 import BeautifulSoup
import requests


# Crea la carpeta "log" si no existe
if not os.path.exists("scraper/02DatosSitiosWeb/log"):
    os.makedirs("scraper/02DatosSitiosWeb/log")

# Configuración del logger con la ruta del archivo en la carpeta "log"
logging.basicConfig(
    filename="scraper/02DatosSitiosWeb/log/02naturalGasCash.log",  # Ruta donde se guardará el archivo log
    level=logging.DEBUG,  # Nivel mínimo de log
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del log
    datefmt="%Y-%m-%d %H:%M:%S",  # Formato de fecha y hora
)

logging.info("Iniciando la ejecución del script")

# Crea de carpeta "wtiCrude" para almacenar el archivo CSV
if not os.path.exists("scraper/02DatosSitiosWeb/csv"):
    logging.info("scraper/02DatosSitiosWeb/Creación de carpeta csv")
    os.makedirs("scraper/02DatosSitiosWeb/csv")

logging.info("Estableciendo los selectores")

# URL y selectores
url = "https://www.barchart.com/futures/quotes/NGY00"
selector_fecha = "span.symbol-trade-time"
selector_valor = "span.last-change"

logging.info("Enviando cabeceras al sitio web")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
        locale="en-US",
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Referer": "https://www.barchart.com/"
        }
    )
    page = context.new_page()
    
    try:
        logging.info("Inicio de espera de carga de pagina web.")
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        logging.info("Termino de espera de carga de pagina web.")
    except TimeoutError:
        page.screenshot(path="goto_error.png")
        logging.error(f"Error: La navegación a la URL no se completó en el tiempo esperado. Revisa 'goto_error.png'")
        print("Error: La navegación a la URL no se completó en el tiempo esperado. Revisa 'goto_error.png'")
        browser.close()
        exit(1)
    html = page.content()
    browser.close()

# Procesar HTML con BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
fecha_element = soup.select_one(selector_fecha)
valor_element = soup.select_one(selector_valor)

# Extraer texto
fecha = fecha_element.text.strip() if fecha_element else "N/D"
valor_str = valor_element.text.strip() if valor_element else "N/D"


# Función para convertir a float eliminando caracteres no deseados
def parse_float(value):
    try:
        # Se eliminan comas, símbolos de moneda y de porcentaje
        logging.info("Eliminando simbolos especiales")
        cleaned = value.replace(",", "").replace("$", "").replace("s", "").replace("%", "").strip()
        return float(cleaned)
    except Exception as e:
        logging.error(f"Error: {e}")
        return None


# Transformar los datos
logging.info("Transformando datos a puntos flotantes")
# Convertir valor a float
valor = parse_float(valor_str)

# Mostrar resultados en consola
print("Time", fecha)
print("Last", valor)

# Registrar en log
logging.info(f"Fecha obtenida: {fecha}")
logging.info(f"Valor obtenido: {valor}")
logging.info("Fin de ejecución del script")

# Nombre del archivo con marca de tiempo
filename = f"scraper/02DatosSitiosWeb/csv/datos_02naturalGasCash.csv"

# Guardar los datos en un archivo CSV, incluyendo el timestamp en el registro
logging.info("Creando archivo CSV")
with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Time", "Last"])
    writer.writerow([fecha, valor])

logging.info("Fin de ejecución del script")
logging.info("================================")
