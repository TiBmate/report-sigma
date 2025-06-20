import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def crear_tabla_datos_semana(WTI, NaturalGas, GasolineGas, OilService, NaturalGasStorage, NorthAmericanRig, USPetroleum):
    # Lista de archivos y nombres asociados
    archivos = [WTI, NaturalGas, GasolineGas, OilService, NaturalGasStorage, NorthAmericanRig, USPetroleum]
    nombres = ["WTI Crude Oil", "Natural Gas", "Gasoline Prices", "Oil Service Sector Index", "Natural Gas Storage", "North American Rig Count", "US Petroleum Stocks (MB)"]
    sources = ["www.barchart.com", "www.barchart.com", "www.eia.gov", "www.finance.yahoo.com", "www.eia.gov", "www.bakerhughes.com", "www.eia.gov"]
    
    # Lista para almacenar las filas resultantes
    filas = []
    
    # Se itera sobre cada archivo CSV y se extraen los valores según lo solicitado
    for i, archivo in enumerate(archivos):
        df = pd.read_csv(archivo)

        # Extraemos el primer valor de la columna "Week"
        primer_week = df["Week"].iloc[0]
        # Buscamos la siguiente fila que coincida con ese valor
        indices_week = df.index[df["Week"] == primer_week].tolist()
        if len(indices_week) > 1:
            indice_encontrado = indices_week[1]
        else:
            # Si no se encuentra la siguiente coincidencia, se usa la fila 52 (índice 51) como fallback
            indice_encontrado = 51
        # Se toma el valor de "Last" de la fila encontrada
        last_year_val = df["Last"].iloc[indice_encontrado]
        last_year_time = df["Time"].iloc[indice_encontrado]
    
        # Fila 1: datos de "Last" y "Change" utilizando el nuevo valor encontrado para "Last Year"
        year_change_fila1 = df["Last"].iloc[0] - last_year_val
        fila1 = {
            "Weekly Statistic": nombres[i],
            "Current Value": df["Last"].iloc[0],
            "Week Change": df["Change"].iloc[0],
            "Previous Week": df["Last"].iloc[1],
            "Year Change": round(year_change_fila1, 2),
            "Last Year": last_year_val
        }

        # Fila 2: datos de "Time", "%Chg" y la operación modificada para "Year Change"
        if last_year_val != 0:
            year_change_fila2 = ((df["Last"].iloc[0] - last_year_val) * 100) / last_year_val
        else:
            year_change_fila2 = None  # Evitar división por cero

        week_change = f"{df['%Chg'].iloc[0]}%"
        year_change = f"{round(year_change_fila2, 1) if year_change_fila2 is not None else None}%"
        fila2 = {
            "Weekly Statistic": sources[i],
            "Current Value": df["Time"].iloc[0],
            "Week Change": week_change,
            "Previous Week": df["Time"].iloc[1],
            "Year Change": year_change,
            "Last Year": last_year_time
        }

        filas.append(fila1)
        filas.append(fila2)

    # Se crea el DataFrame con las columnas especificadas
    columnas = ["Weekly Statistic", "Current Value", "Week Change", "Previous Week", "Year Change", "Last Year"]
    tabla = pd.DataFrame(filas, columns=columnas)

    # Verifica si la carpeta "csvPDF-Page2" existe, si no, la crea
    carpeta_salida = "scraper/03Report/csvPDF-Page2"
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Guarda la tabla en un archivo CSV dentro de la carpeta creada
    ruta_salida = os.path.join(carpeta_salida, "csvSemanal.csv")
    tabla.to_csv(ruta_salida, index=False)

    # Imprime la tabla en consola
    print(tabla)
    print("Archivo guardado en:", ruta_salida)

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

def obtener_fecha_base():
    """
    Lee el primer valor de las columnas "Anio" y "Mes" del archivo base y construye una fecha.
    """
    df = pd.read_csv("./scraper/01HistoricalDatabase/10InternationalRigMensual.csv", dtype=str)
    anio = df["Anio"].iloc[0]
    mes = df["Mes"].iloc[0]
    dt = datetime(int(anio), int(mes), 1)
    return dt.strftime("%Y-%m-%d")  # Ej: "2025-02-01"

def crear_tabla_datos_mes(International, NorthAmerica, WorldWide):
    # Obtener fecha base desde archivo
    fecha_str = obtener_fecha_base()
    fecha_base = datetime.strptime(fecha_str, "%Y-%m-%d")

    # Generar encabezados dinámicos
    mes_actual = fecha_base.strftime("%b %Y")         # Ej: "Feb 2025"
    mes_anterior = (fecha_base - relativedelta(months=1)).strftime("%b %Y")   # Ej: "Jan 2025"
    mismo_mes_ano_pasado = (fecha_base - relativedelta(years=1)).strftime("%b %Y")  # Ej: "Feb 2024"

    # Lista de archivos y nombres asociados
    archivos = [International, NorthAmerica, WorldWide]
    nombres = ["International Rig Count", "North American Rig Count", "World Wide Rig Count"]
    sources = ["www.bakerhughes.com", "www.bakerhughes.com", "www.bakerhughes.com"]
    
    # Lista para almacenar las filas resultantes
    filas = []
    
    # Se itera sobre cada archivo CSV y se extraen los valores según lo solicitado
    for i, archivo in enumerate(archivos):
        df = pd.read_csv(archivo)
        
        # Fila 1: datos extraídos del archivo mensualmente
        # Se asume que "fila 13" corresponde a la posición 12 (contando desde 0)
        last = int(df["Last"].iloc[0])
        fila1 = {
            "Monthly Statistic": nombres[i],
            mes_actual: last,
            "Month Change": df["Change"].iloc[0],
            mes_anterior: df["Last"].iloc[1],
            "Year Change": df["YearChange"].iloc[0],
            mismo_mes_ano_pasado: df["Last"].iloc[12]
        }
        
        # Fila 2: datos de la fuente y otros valores
        # Agregar el símbolo "%" al valor extraído"
        month_change = f"{df['%Chg'].iloc[0]}%"
        year_change = f"{df['Year%Chg'].iloc[0]}%"
        fila2 = {
            "Monthly Statistic": sources[i],
            mes_actual: "-",
            "Month Change": month_change,
            mes_anterior: "-",
            "Year Change": year_change,
            mismo_mes_ano_pasado: "-"
        }
        
        filas.append(fila1)
        filas.append(fila2)
    
    # Se crea el DataFrame con las columnas especificadas
    columnas = ["Monthly Statistic", mes_actual, "Month Change", mes_anterior, "Year Change", mismo_mes_ano_pasado]
    tabla = pd.DataFrame(filas, columns=columnas)
    
    # Verifica si la carpeta "csvPDF-Page2" existe, si no, la crea
    carpeta_salida = "scraper/03Report/csvPDF-Page2"
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    
    # Guarda la tabla en un archivo CSV dentro de la carpeta creada
    ruta_salida = os.path.join(carpeta_salida, "csvMensual.csv")
    tabla.to_csv(ruta_salida, index=False)
    
    # Imprime la tabla en consola
    print("\n", tabla)
    print("Archivo guardado en:", ruta_salida)


# Ejemplo de uso:
if __name__ == "__main__":
    # Archivos para la tabla semanal
    WTI = "scraper/01HistoricalDatabase/01WTICrudeHistoricalSemana.csv"
    NaturalGas = "scraper/01HistoricalDatabase/02NaturalGasCashHistoricalSemana.csv"
    GasolineGas = "scraper/01HistoricalDatabase/03GasolinePricesHistoricalSemana.csv"
    OilService = "scraper/01HistoricalDatabase/04OilServicesHistoricalSemana.csv"
    NaturalGasStorage = "scraper/01HistoricalDatabase/05NaturalGasStorageHistoricalSemana.csv"
    NorthAmericanRig = "scraper/01HistoricalDatabase/06NorthAmericanRigHistoricalSemana.csv"
    USPetroleum = "scraper/01HistoricalDatabase/07USPetroleumStockHistoricalSemana.csv"
    
    crear_tabla_datos_semana(WTI, NaturalGas, GasolineGas, OilService, NaturalGasStorage, NorthAmericanRig, USPetroleum)
    
    # Archivos para la tabla mensual
    International = "scraper/01HistoricalDatabase/10InternationalRigMensual.csv"
    NorthAmerica = "scraper/01HistoricalDatabase/11NorthAmericaRigMensual.csv"
    WorldWide = "scraper/01HistoricalDatabase/12WorldWideRigMensual.csv"
    
    crear_tabla_datos_mes(International, NorthAmerica, WorldWide)
