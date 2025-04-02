# Proyecto de Scraping y Reporte Web

Este proyecto tiene como objetivo realizar el scraping de datos históricos de diversos sitios web, procesarlos y generar reportes visuales a través de una aplicación web desarrollada en Python y Flask.

---

## Estructura del Proyecto

La siguiente es la estructura completa del proyecto:

```
.
├── 01DatosSitiosWeb.sh         # Ejecuta los scripts de scraping y muestra los datos en la web.
├── LICENSE                     # Licencia del proyecto.
├── README.md                   # Este archivo.
├── app.py                      # Archivo principal de la aplicación Flask.
├── flaskapp.wsgi               # Configuración WSGI para despliegue en producción.
├── requirements.txt            # Archivo con las librerías necesarias para el proyecto.
├── scraper                   # Directorio que contiene scripts y datos de scraping.
│   ├── 01HistoricalDatabase  # Archivos CSV con datos históricos semanales y mensuales.
│   │   ├── 01WTICrudeHistoricalSemana.csv
│   │   ├── 02NaturalGasCashHistoricalSemana.csv
│   │   ├── 03GasolinePricesHistoricalSemana.csv
│   │   ├── 04OilServicesHistoricalSemana.csv
│   │   ├── 05NaturalGasStorageHistoricalSemana.csv
│   │   ├── 06NorthAmericanRigHistoricalSemana.csv
│   │   ├── 06USRigHistoricalSemana.csv
│   │   ├── 07USPetroleumStockHistoricalSemana.csv
│   │   ├── 10InternationalRigMensual.csv
│   │   ├── 11NorthAmericaRigMensual.csv
│   │   └── 12WorldWideRigMensual.csv
│   ├── 02DatosSitiosWeb       # Scripts de scraping para obtener datos de diferentes sitios web.
│   │   ├── 01WTICrude.py
│   │   ├── 02NaturalGasCash.py
│   │   ├── 03GasolinePrices.py
│   │   ├── 04OilServicesSector.py
│   │   ├── 05NaturalGasStorage.py
│   │   ├── 06NorthAmericanRig.py
│   │   ├── 06USRigs.py
│   │   ├── 07USCrudeOilInventory.py
│   │   ├── 08USRigs.py
│   │   ├── 09USRigsCsv.py
│   │   ├── csv                # Directorio para archivos CSV generados.
│   │   └── log                # Directorio para archivos de log de los scripts.
│   │       ├── 01wtiCrude.log
│   │       ├── 02naturalGasCash.log
│   │       ├── 03gasolinePrices.log
│   │       ├── 04oilServicesSector.log
│   │       ├── 05naturalGasStorage.log
│   │       ├── 06northAmericanRigs.log
│   │       ├── 06usRigs.log
│   │       └── 07usCrudeOilInventory.log
│   ├── 03Report               # Scripts y recursos para generar reportes y gráficos.
│   │   ├── 11HelperPDF-Page1.py
│   │   ├── 12HelperPDF-Page2.py
│   │   ├── 13HelperPDF-Page3.py
│   │   ├── 14Grafica01WTI.py
│   │   ├── 15Grafica02NaturalGas.py
│   │   ├── 16Grafica03Gasoline.py
│   │   ├── 17Grafica05OilServices.py
│   │   ├── csvPDF-Page1         # Archivos CSV para la generación de PDF (Página 1).
│   │   │   ├── csvMes.csv
│   │   │   └── csvSemanal.csv
│   │   ├── csvPDF-Page2         # Archivos CSV para la generación de PDF (Página 2).
│   │   │   ├── csvMensual.csv
│   │   │   └── csvSemanal.csv
│   │   └── graficas             # Gráficos generados para los reportes.
│   │       ├── 01WTI.png
│   │       ├── 02Natural.png
│   │       ├── 03Gasoline.png
│   │       └── 04OilServices.png
│   └── 10HelperWeb-HistoricoSemanal.py  # Script auxiliar para el manejo del histórico semanal en la web.
├── static                     # Recursos estáticos para la aplicación web.
│   ├── img                   # Imágenes utilizadas en la interfaz web.
│   │   ├── 01WTI.png
│   │   ├── 02Natural.png
│   │   ├── 03Gasoline.png
│   │   ├── 04OilServices.png
│   │   └── logo
│   │       ├── favicon.ico
│   │       └── logo-sigma.png
│   └── styles.css            # Archivo CSS para la apariencia de la web.
└── templates                 # Plantillas HTML de la aplicación web.
    └── index.html
```

---

## Instalación

Para instalar las dependencias del proyecto, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone <URL-del-repositorio>
   ```
2. **Acceder al directorio del proyecto:**
   ```bash
   cd <nombre-del-proyecto>
   ```
3. **Instalar las librerías necesarias:**
   ```bash
   pip install -r requirements.txt
   ```
   El archivo `requirements.txt` contiene todas las dependencias requeridas.

---

## Uso del Proyecto

### Ejecución del Scraping y Visualización

- **Script principal de scraping:**  
  El archivo `01DatosSitiosWeb.sh` se encarga de ejecutar los scripts de scraping ubicados en el directorio `scraper/02DatosSitiosWeb` y de mostrar los datos recopilados en el sitio web.

### Aplicación Web

- **Ejecución local:**  
  La aplicación web se ejecuta a través del archivo `app.py`, que utiliza Flask para levantar el servidor web.
  
- **Despliegue en producción:**  
  Para desplegar la aplicación en un servidor productivo se utiliza el archivo `flaskapp.wsgi`.

### Cambio de Versión en el Servidor Productivo

- **Script de cambio de versión:**  
  El archivo `switchVersion.sh` se utiliza para realizar el cambio de versión de la aplicación en el servidor productivo, facilitando el proceso de actualización.

---

## Contribuciones

Si deseas contribuir a este proyecto, por favor:
- Abre un *issue* para discutir tus ideas o reportar problemas.
- Envía un *pull request* con tus mejoras o correcciones.

---

## Licencia

Este proyecto se distribuye bajo los términos de la licencia especificada en el archivo [LICENSE](./LICENSE).

---

## Contacto

Para más información o consultas, por favor contacta al equipo de desarrollo.

---
