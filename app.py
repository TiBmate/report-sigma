from flask import Flask, render_template, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)

def agregar_hipervinculos(df, columna, urls=None, aplicar_en_filas_pares=False):
    """
    Transforma los valores de la columna especificada en hipervínculos.
    Si se proporciona una lista de URLs, se asume que el orden de las filas coincide.
    Si aplicar_en_filas_pares es True, solo se aplicará la transformación a las filas pares 
    (contando desde 1, es decir, fila 2, 4, 6, ...), utilizando las URLs de la lista de manera secuencial.
    """
    if columna in df.columns:
        url_index = 0
        for i in range(len(df)):
            if aplicar_en_filas_pares:
                if (i + 1) % 2 == 0:
                    if urls is not None:
                        if url_index < len(urls):
                            url = urls[url_index]
                            text = df.loc[i, columna]
                            df.loc[i, columna] = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'
                        else:
                            text = df.loc[i, columna]
                            df.loc[i, columna] = text
                    else:
                        df.loc[i, columna] = (f'<a href="{df.loc[i, columna]}" target="_blank" rel="noopener noreferrer">'
                                              f'{df.loc[i, columna]}</a>' 
                                              if pd.notnull(df.loc[i, columna]) else '')
                    url_index += 1
            else:
                if urls is not None:
                    if i < len(urls):
                        url = urls[i]
                        text = df.loc[i, columna]
                        df.loc[i, columna] = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'
                    else:
                        text = df.loc[i, columna]
                        df.loc[i, columna] = text
                else:
                    df.loc[i, columna] = (f'<a href="{df.loc[i, columna]}" target="_blank" rel="noopener noreferrer">'
                                          f'{df.loc[i, columna]}</a>' 
                                          if pd.notnull(df.loc[i, columna]) else '')
    return df

def generar_tabla_html(csv_path, source_urls=None, stat_col=None, stat_urls=None, stat_aplicar_en_filas_pares=False):
    # Lee el archivo CSV forzando todos los datos a cadena para evitar redondeos.
    df = pd.read_csv(csv_path, dtype=str)
    
    # Aplica hipervínculos a la columna "Source", si existe.
    df = agregar_hipervinculos(df, "Source", source_urls)
    
    # Aplica hipervínculos a una columna adicional, por ejemplo "Weekly Statistic" o "Monthly Statistic", si se especifica.
    if stat_col is not None:
        df = agregar_hipervinculos(df, stat_col, stat_urls, aplicar_en_filas_pares=stat_aplicar_en_filas_pares)
        
    return df.to_html(classes="data-table", index=False, escape=False)

def obtener_week_ending():
    """
    Lee el primer valor de la columna "Time" del archivo CSV ubicado en:
    ./scraper/01HistoricalDatabase/01WTICrude.csv, con formato MM/DD/YY,
    y lo transforma al formato "March 21, 2025".
    """
    df = pd.read_csv("./scraper/01HistoricalDatabase/01WTICrudeHistoricalSemana.csv", dtype=str)
    raw_date = df["Time"].iloc[0]
    dt = datetime.strptime(raw_date, "%m/%d/%y")
    week_ending = dt.strftime("%B %d, %Y")
    return week_ending

def obtener_month_ending():
    """
    Lee el primer valor de la columna "Anio" y "Mes" del archivo CSV ubicado en:
    ./scraper/01HistoricalDatabase/10InternationalRigMensual.csv, donde "Anio" está en formato YYYY y "Mes" en formato MM.
    Transforma estos valores al formato "March, 2025".
    """
    df = pd.read_csv("./scraper/01HistoricalDatabase/10InternationalRigMensual.csv", dtype=str)
    anio = df["Anio"].iloc[0]
    mes = df["Mes"].iloc[0]
    dt = datetime(int(anio), int(mes), 1)
    month_ending = dt.strftime("%B, %Y")
    return month_ending

@app.route('/')
def index():
    fecha_actual = datetime.now().strftime("%B %d, %Y")
    
    # Obtiene las fechas formateadas a partir de los CSV históricos.
    week_ending = obtener_week_ending()
    month_ending = obtener_month_ending()
    
    # Listas de URLs para cada tabla de la primera página
    urls_semanal = [
        "https://www.barchart.com/futures/quotes/CLY00",
        "https://www.barchart.com/futures/quotes/NGY00/performance",
        "https://www.eia.gov/petroleum/gasdiesel/",
        "https://finance.yahoo.com/quote/%5EOSX/history/?ltr=1",
        "https://bakerhughesrigcount.gcs-web.com/rig-count-overview?c=79687&p=irol-rigcountsoverview",
        "https://bakerhughesrigcount.gcs-web.com/rig-count-overview?c=79687&p=irol-rigcountsoverview",
        "https://www.eia.gov/dnav/pet/pet_sum_sndw_dcus_nus_w.htm"
    ]
    
    urls_mensual = [
        "https://bakerhughesrigcount.gcs-web.com/rig-count-overview?c=79687&p=irol-rigcountsoverview",
        "https://bakerhughesrigcount.gcs-web.com/rig-count-overview?c=79687&p=irol-rigcountsoverview",
        "https://bakerhughesrigcount.gcs-web.com/rig-count-overview?c=79687&p=irol-rigcountsoverview"
    ]
    
    # Listas de URLs para las columnas de estadísticas de la segunda página
    urls_semanal2 = [
        "https://www.barchart.com/futures/quotes/CLY00",
        "https://www.barchart.com/futures/quotes/NGY00/performance",
        "https://www.eia.gov/petroleum/gasdiesel/",
        "https://finance.yahoo.com/quote/%5EOSX/history/?ltr=1",
        "https://ir.eia.gov/ngs/ngs.html",
        "https://bakerhughesrigcount.gcs-web.com/rig-count-overview?c=79687&p=irol-rigcountsoverview",
        "https://www.eia.gov/dnav/pet/pet_sum_sndw_dcus_nus_w.htm"
    ]
    
    urls_mensual2 = [
        "https://bakerhughesrigcount.gcs-web.com/rig-count-overview?c=79687&p=irol-rigcountsoverview",
        "https://bakerhughesrigcount.gcs-web.com/rig-count-overview?c=79687&p=irol-rigcountsoverview",
        "https://bakerhughesrigcount.gcs-web.com/rig-count-overview?c=79687&p=irol-rigcountsoverview"
    ]
    
    # Se pasan las listas de URLs para las tablas correspondientes
    tabla_semanal = generar_tabla_html("./scraper/03Report/csvPDF-Page1/csvSemanal.csv", source_urls=urls_semanal)
    tabla_mensual = generar_tabla_html("./scraper/03Report/csvPDF-Page1/csvMes.csv", source_urls=urls_mensual)
    
    # Para las tablas de la segunda página, se agregan hipervínculos en las columnas de estadísticas
    # solo en las filas pares (fila 2, 4, 6, ...) utilizando todas las URLs de forma secuencial.
    tabla2_semanal = generar_tabla_html(
        "./scraper/03Report/csvPDF-Page2/csvSemanal.csv",
        stat_col="Weekly Statistic",
        stat_urls=urls_semanal2,
        stat_aplicar_en_filas_pares=True
    )
    tabla2_mensual = generar_tabla_html(
        "./scraper/03Report/csvPDF-Page2/csvMensual.csv",
        stat_col="Monthly Statistic",
        stat_urls=urls_mensual2,
        stat_aplicar_en_filas_pares=True
    )

    return render_template(
        'index.html',
        fecha_actual=fecha_actual,
        tabla_semanal=tabla_semanal,
        tabla_mensual=tabla_mensual,
        tabla2_semanal=tabla2_semanal,
        tabla2_mensual=tabla2_mensual,
        Week_ending=week_ending,
        Month_ending=month_ending
    )

if __name__ == '__main__':
    app.run(debug=True)
