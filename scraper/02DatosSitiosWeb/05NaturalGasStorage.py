from playwright.sync_api import sync_playwright, TimeoutError
import csv
import datetime
import os
import logging

# Nombre del sitio web del que se obtendrán los datos
webRegistro = f"naturalGasStorage"

# Nombre del archivo log
fileLog = f"05{webRegistro}.log"
pathLog = f"log/{fileLog}"

# Ruta donde se guarda el archivo CSV
pathCsv = f"scraper/02DatosSitiosWeb/csv"

# Nombre de archivo
fileCsv = f"{pathCsv}/datos_05{webRegistro}.csv"

# Crea la carpeta "log" si no existe
if not os.path.exists("log"):
    os.makedirs("log")

# Configuración del logger con la ruta del archivo en la carpeta "log"
logging.basicConfig(
    filename=pathLog,  # Ruta donde se guardará el archivo log
    level=logging.DEBUG,  # Nivel mínimo de log
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del log
    datefmt="%Y-%m-%d %H:%M:%S",  # Formato de fecha y hora
)

# URL y selectores
web = "https://ir.eia.gov/"
url = "https://ir.eia.gov/ngs/ngs.html"

logging.info("Estableciendo los selectores")
selector_fecha = "#innerX > div > div.pagecontent.mr_temp1 > div.main_col > table:nth-child(1) > tbody > tr:nth-child(3) > td:nth-child(2) > strong"
selector_valor = "#innerX > div > div.pagecontent.mr_temp1 > div.main_col > table:nth-child(1) > tbody > tr:nth-child(11) > td:nth-child(2) > strong"

# Crea de carpeta para almacenar el archivo CSV
if not os.path.exists(pathCsv):
    logging.info(f"Creación de carpeta {pathCsv}")
    os.makedirs(pathCsv)


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
            "Referer": web
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
    
    try:
        logging.info("Iniciando la espera del primer selector, fecha")
        page.wait_for_selector(selector_fecha, timeout=60000)
    except TimeoutError:
        page.screenshot(path="debug.png")
        logging.error(f"Error: El selector de fecha no apareció en 60 segundos. Revisa 'debug.png'.")
        print("Error: El selector de fecha no apareció en 60 segundos. Revisa 'debug.png'.")
        browser.close()
        exit(1)

    # Extraer los elementos
    logging.info("Inicio de extracción de elementos")
    fecha_element = page.query_selector(selector_fecha)
    valor_element = page.query_selector(selector_valor)
    
    # Obtener el texto de los elementos, controlando si existen
    logging.info("Obteniendo el texto de los elementos.")
    fecha = fecha_element.inner_text().strip() if fecha_element else "N/D"
    valor_str = valor_element.inner_text().strip() if valor_element else "N/D"
    
    browser.close()

# Función para convertir a float eliminando caracteres no deseados
def parse_float(value):
    try:
        # Se eliminan comas, símbolos de moneda
        logging.info("Eliminando simbolos especiales")
        cleaned = value.replace(",", "").replace("$", "").replace("s", "").replace("%", "").replace("(", "").replace(")", "").strip()
        return float(cleaned)
    except Exception as e:
        logging.error(f"Error: {e}")
        return None
        

# Transformar los datos
logging.info("Transformando datos a puntos flotantes")
valor = parse_float(valor_str)


# Mostrar los datos obtenidos
print("Time:", fecha)
print("Last:", valor)


# Guardar los datos en un archivo CSV, incluyendo el timestamp en el registro
logging.info("Creando archivo CSV")
with open(fileCsv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Time", "Last"])
    writer.writerow([fecha, valor])

logging.info("Fin de ejecución del script")
logging.info("================================")
