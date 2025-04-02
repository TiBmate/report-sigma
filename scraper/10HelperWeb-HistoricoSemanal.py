import pandas as pd
import os

def leer_csv(ruta):
    """
    Lee un archivo CSV y devuelve un DataFrame.
    """
    return pd.read_csv(ruta)

def calcular_valores(nuevo_actual, ultimo_last):
    """
    Calcula los valores de Change y %Chg.
      - Change se redondea a dos decimales.
      - %Chg se redondea a un decimal.
    """
    raw_change = nuevo_actual - ultimo_last
    raw_chg = (raw_change * 100) / ultimo_last
    return round(raw_change, 2), round(raw_chg, 1)

def actualizar_historico(ruta_datos, ruta_historico):
    """
    Procesa un par de archivos:
      - Lee el archivo de datos (con columnas 'TimeActual' y 'Actual').
      - Lee el archivo histórico (con columnas 'Time', 'Last', 'Change' y '%Chg').
      - Calcula Change = Actual - último valor de Last y %Chg = (Change * 100) / último Last.
      - Inserta la nueva fila al inicio del DataFrame histórico.
      - Guarda el DataFrame actualizado y elimina el archivo de datos.
    """
    # Leer archivos CSV
    df_datos = leer_csv(ruta_datos)
    df_hist = leer_csv(ruta_historico)
    
    # Extraer el primer registro del archivo de datos
    nuevo_time = df_datos.loc[0, "Time"]
    nuevo_actual = df_datos.loc[0, "Last"]
    
    # Convertir el nuevo Time a datetime y obtener el año
    nuevo_time_dt = pd.to_datetime(nuevo_time, format='%m/%d/%y')
    nuevo_year = nuevo_time_dt.year
    
    # Asegurarse de que la columna 'Time' del histórico esté en formato datetime
    if not df_hist.empty:
        df_hist["Time"] = pd.to_datetime(df_hist["Time"], format='%m/%d/%y', errors="coerce")
    
    # Si no existe la columna 'Week', se crea
    if "Week" not in df_hist.columns:
        df_hist["Week"] = pd.NA
    
    # Determinar el número de semana para el nuevo registro:
    # Filtrar registros del mismo año
    df_hist_same_year = df_hist[df_hist["Time"].dt.year == nuevo_year] if not df_hist.empty else pd.DataFrame()
    if not df_hist_same_year.empty and df_hist_same_year["Week"].notna().any():
        max_week = df_hist_same_year["Week"].dropna().max()
        new_week = max_week + 1
    else:
        new_week = 1
    
    # Obtener el primer valor de 'Last' del histórico (si existe)
    if not df_hist.empty:
        ultimo_last = df_hist.iloc[0]["Last"]
    else:
        ultimo_last = nuevo_actual
    
    # Calcular Change y %Chg
    change, chg = calcular_valores(nuevo_actual, ultimo_last)
    
    # Crear la nueva fila con columnas adicionales: Week
    nueva_fila = pd.DataFrame({
        "Time": [nuevo_time],
        "Last": [nuevo_actual],
        "Change": [change],
        "%Chg": [chg],
        "Week": [new_week]
    })
    
    # Insertar la nueva fila al inicio del DataFrame histórico
    df_hist_actualizado = pd.concat([nueva_fila, df_hist], ignore_index=True)

     # Convertir la columna "Time" al formato '%m/%d/%y' antes de guardar
    df_hist_actualizado["Time"] = pd.to_datetime(df_hist_actualizado["Time"], format='%m/%d/%y', errors="coerce").dt.strftime('%m/%d/%y')    
    
    # Guardar el DataFrame actualizado en el archivo histórico
    df_hist_actualizado.to_csv(ruta_historico, index=False)
    
    print(f"Archivo histórico '{ruta_historico}' actualizado.")

def actualizar_historico_naturalGas(ruta_datos, ruta_historico):
    """
    Actualiza el archivo histórico para Natural GasStorage con cálculos extra:
      - Se lee el archivo de datos (con columnas 'TimeActual' y 'Actual').
      - Se extrae el primer registro y se calcula Change y %Chg usando el último valor de 'Last'
        del histórico (o el valor actual si el histórico está vacío).
      - Se asigna un número consecutivo en la columna 'Week' basado en el año (se reinicia a 1 cada año).
      - Una vez insertada la nueva fila, se filtran los registros con la misma 'Week' y se toman los
        primeros cuatro para calcular:
            * totalMax: máximo valor de 'Last'
            * totalMin: mínimo valor de 'Last'
      - Se guarda el histórico actualizado y se elimina el archivo de datos.
    """
    # Leer archivos CSV
    df_datos = leer_csv(ruta_datos)
    df_hist = leer_csv(ruta_historico)
    
    # Extraer el primer registro del archivo de datos
    nuevo_time = df_datos.loc[0, "Time"]
    nuevo_actual = df_datos.loc[0, "Last"]
    
    # Convertir el nuevo Time a datetime y obtener el año
    nuevo_time_dt = pd.to_datetime(nuevo_time, format='%m/%d/%y')
    nuevo_year = nuevo_time_dt.year
    
    # Asegurarse de que la columna 'Time' del histórico esté en formato datetime
    if not df_hist.empty:
        df_hist["Time"] = pd.to_datetime(df_hist["Time"], format='%m/%d/%y', errors="coerce")
    
    # Si no existe la columna 'Week', se crea
    if "Week" not in df_hist.columns:
        df_hist["Week"] = pd.NA
    
    # Determinar el número de semana para el nuevo registro:
    # Filtrar registros del mismo año
    df_hist_same_year = df_hist[df_hist["Time"].dt.year == nuevo_year] if not df_hist.empty else pd.DataFrame()
    if not df_hist_same_year.empty and df_hist_same_year["Week"].notna().any():
        max_week = df_hist_same_year["Week"].dropna().max()
        new_week = max_week + 1
    else:
        new_week = 1
    
    # Obtener el primer valor de 'Last' del histórico (si existe)
    if not df_hist.empty:
        ultimo_last = df_hist.iloc[0]["Last"]
    else:
        ultimo_last = nuevo_actual
    
    # Calcular Change y %Chg
    change, chg = calcular_valores(nuevo_actual, ultimo_last)
    
    # Crear la nueva fila con columnas adicionales: Week, totalMax y totalMin (inicialmente None)
    nueva_fila = pd.DataFrame({
        "Time": [nuevo_time],
        "Last": [nuevo_actual],
        "Change": [change],
        "%Chg": [chg],
        "totalMax": [None],
        "totalMin": [None],
        "Week": [new_week]
    })
    
    # Insertar la nueva fila al inicio del DataFrame histórico
    df_hist_actualizado = pd.concat([nueva_fila, df_hist], ignore_index=True)
    
    # Filtrar registros con el mismo valor de Week que el nuevo registro
    df_same_week = df_hist_actualizado[df_hist_actualizado["Week"] == new_week]
    # Seleccionar los primeros cuatro registros para esta semana
    df_first_four = df_same_week.head(4)
    if not df_first_four.empty:
        total_max = df_first_four["Last"].max()
        total_min = df_first_four["Last"].min()
    else:
        total_max = None
        total_min = None
    
    # Actualizar la nueva fila (la primera del DataFrame) con totalMax y totalMin
    df_hist_actualizado.loc[0, "totalMax"] = total_max
    df_hist_actualizado.loc[0, "totalMin"] = total_min

     # Convertir la columna "Time" al formato '%m/%d/%y' antes de guardar
    df_hist_actualizado["Time"] = pd.to_datetime(df_hist_actualizado["Time"], format='%m/%d/%y', errors="coerce").dt.strftime('%m/%d/%y')    
    
    # Guardar el DataFrame actualizado en el archivo histórico
    df_hist_actualizado.to_csv(ruta_historico, index=False)

    
    print(f"Archivo histórico '{ruta_historico}' actualizado con cálculos extras.")

if __name__ == "__main__":
    # Definición de rutas para cada par de archivos

    # WTI Crude
    ruta_datos_wtiActual = "./02DatosSitiosWeb/csv/datos_01wtiCrude.csv"
    ruta_historico_wtiHistorical = "./01HistoricalDatabase/01WTICrudeHistoricalSemana.csv"

    # Natural Gas
    ruta_datos_naturalGasActual = "./02DatosSitiosWeb/csv/datos_02naturalGasCash.csv"
    ruta_historico_naturalGasHistorical = "./01HistoricalDatabase/02NaturalGasCashHistoricalSemana.csv"

    # Gasoline Prices
    ruta_datos_gasolinePricesActual = "./02DatosSitiosWeb/csv/datos_03gasolinePrices.csv"
    ruta_historico_gasolinePricesHistorical = "./01HistoricalDatabase/03GasolinePricesHistoricalSemana.csv"

    # Oil Services Crude
    ruta_datos_oilServicesActual = "./02DatosSitiosWeb/csv/datos_04oilServicesSector.csv"
    ruta_historico_oilServicesHistorical = "./01HistoricalDatabase/04OilServicesHistoricalSemana.csv"

    # Natural GasStorage (con cálculos extras)
    ruta_datos_NaturalGasStorageActual = "./02DatosSitiosWeb/csv/datos_05naturalGasStorage.csv"
    ruta_historico_NaturalGasStorageHistorical = "./01HistoricalDatabase/05NaturalGasStorageHistoricalSemana.csv"

    # North AmericanRig
    ruta_datos_NorthAmericanRigActual = "./02DatosSitiosWeb/csv/datos_06northAmericanRigs.csv"
    ruta_historico_NorthAmericanRigHistorical = "./01HistoricalDatabase/06NorthAmericanRigHistoricalSemana.csv"

    # US Rig
    ruta_datos_USRigActual = "./02DatosSitiosWeb/csv/datos_06usRigs.csv"
    ruta_historico_USRigHistorical = "./01HistoricalDatabase/06USRigHistoricalSemana.csv"

    # US Petroleum Stock
    ruta_datos_USPetroleumStockActual = "./02DatosSitiosWeb/csv/datos_07usCrudeOilInventory.csv"
    ruta_historico_USPetroleumStockHistorical = "./01HistoricalDatabase/07USPetroleumStockHistoricalSemana.csv"

    # Procesar cada par de archivos
    actualizar_historico(ruta_datos_wtiActual, ruta_historico_wtiHistorical)
    actualizar_historico(ruta_datos_naturalGasActual, ruta_historico_naturalGasHistorical)
    actualizar_historico(ruta_datos_gasolinePricesActual, ruta_historico_gasolinePricesHistorical)
    actualizar_historico(ruta_datos_oilServicesActual, ruta_historico_oilServicesHistorical)
    actualizar_historico_naturalGas(ruta_datos_NaturalGasStorageActual, ruta_historico_NaturalGasStorageHistorical)
    actualizar_historico(ruta_datos_NorthAmericanRigActual, ruta_historico_NorthAmericanRigHistorical)
    actualizar_historico(ruta_datos_USRigActual, ruta_historico_USRigHistorical)
    actualizar_historico(ruta_datos_USPetroleumStockActual, ruta_historico_USPetroleumStockHistorical)
