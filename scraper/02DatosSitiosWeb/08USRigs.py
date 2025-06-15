from playwright.sync_api import sync_playwright, TimeoutError
import os
import logging
import urllib.parse
import requests

# Configuración de logging
webRegistro = "USRigs"
fileLog = f"08{webRegistro}.log"
pathLog = f"log/{fileLog}"
if not os.path.exists("log"):
    os.makedirs("log")
logging.basicConfig(
    filename=pathLog,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# URL de la página donde se encuentra el enlace de descarga
url = "https://bakerhughesrigcount.gcs-web.com/intl-rig-count"

# Selector del enlace de descarga del Excel
selector_excel = (
    "#block-nir-pid686-content > article > div > div.rig-content-fleft > div > div > "
    "div.block--tbl-ttl-date.block--nir-assets__widget.block--nir-assets__widget--23916."
    "block--slidergutter--nir-assets__widget.block--slidergutter--nir-assets__widget--23916."
    "block--77f2a73a-d100-4208-b756-fb6f6c11f9c5.block--77f2a73a-d100-4208-b756-fb6f6c11f9c5--23916."
    "block.block-nir-assets.block-nir-assets__widget > div > div > div > table > tbody > tr > "
    "td:nth-child(2) > div > div > article > div > div > div > div > "
    "span.file.file--mime-application-vnd-openxmlformats-officedocument-spreadsheetml-sheet."
    "file--x-office-spreadsheet > a"
)

logging.info("Iniciando proceso de descarga del archivo Excel")

with sync_playwright() as p:
    # Se habilita firefox y se deshabilita  HTTP/2
    browser = p.firefox.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-http2"]
    )
    # Se agrega ignore_https_errors para mayor robustez
    context = browser.new_context(
        ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/115.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
        locale="en-US",
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        }
    )
    page = context.new_page()

    try:
        logging.info("Navegando a la URL del reporte")

        # Se cambia el estado de espera a 'domcontentloaded'
        page.goto(url, wait_until="domcontentloaded", timeout=65000)
        logging.info("Página cargada correctamente")
    except TimeoutError:
        page.screenshot(path="goto_error.png")
        logging.error("Error: La navegación a la URL no se completó en el tiempo esperado. Revisa 'goto_error.png'")
        browser.close()
        exit(1)

    try:
        logging.info("Esperando el selector del enlace de descarga Excel")
        page.wait_for_selector(selector_excel, timeout=65000)
    except TimeoutError:
        page.screenshot(path="selector_error.png")
        logging.error("Error: El selector del enlace Excel no apareció en 60 segundos. Revisa 'selector_error.png'")
        browser.close()
        exit(1)

    try:
        logging.info("Extrayendo URL del enlace de descarga")
        link_element = page.query_selector(selector_excel)
        download_href = link_element.get_attribute("href")
        if not download_href:
            raise Exception("No se encontró el atributo href en el enlace.")

        # Convertir a URL absoluta en caso de que sea relativa
        download_url = urllib.parse.urljoin(url, download_href)
        logging.info(f"URL de descarga: {download_url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/115.0.0.0 Safari/537.36",
            "Referer": url,
            "Accept": "*/*"
        }

        # Intentar descargar usando context.request.get con timeout extendido (180 segundos)
        try:
            logging.info("Intentando descargar el archivo usando context.request.get con timeout extendido")
            response = context.request.get(download_url, timeout=180000, headers=headers)
            if response.status != 200:
                raise Exception(f"Error en la descarga. Status code: {response.status}")
            file_data = response.body()

        except Exception as e:
            logging.error(f"Fallo context.request.get: {e}. Se intentará con requests.")

            # Extraer cookies del contexto para usarlas en requests
            cookies_list = context.cookies(download_url)
            cookies = {cookie["name"]: cookie["value"] for cookie in cookies_list}
            logging.info("Intentando descargar el archivo usando requests con streaming")

            r = requests.get(download_url, headers=headers, cookies=cookies, stream=True, timeout=180)

            if r.status_code != 200:
                raise Exception(f"Error en la descarga con requests. Status code: {r.status_code}")
            file_data = b""

            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    file_data += chunk

        file_path = "scraper/02DatosSitiosWeb/originalRigs.xlsx"

        with open(file_path, "wb") as f:
            f.write(file_data)

        logging.info(f"Archivo descargado en: {file_path}")

    except Exception as e:
        logging.error(f"Error durante la descarga: {e}")
        browser.close()
        exit(1)

    browser.close()
