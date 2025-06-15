import os
import pandas as pd

def crear_tabla_datos_semana(WTI, NaturalGas, GasolineGas, OilService, NorthAmericanRigs, UnitedStatesRigs, USCrudeOil):
    
    archivos = {
        "WTI Crude": WTI,
        "Natural Gas": NaturalGas,
        "Gasoline Prices": GasolineGas,
        "Oil Service Sector Index": OilService,
        "North American Rigs": NorthAmericanRigs,
        "United States Rigs": UnitedStatesRigs,
        "US Crude Oil Inventory": USCrudeOil
    }
    
    sources = ["Barchart", "Barchart", "EIA", "Yahoo", "Baker Hughes", "Baker Hughes", "EIA"]
    
    filas = []
    
    for idx, (nombre, ruta) in enumerate(archivos.items()):
        try:
            df = pd.read_csv(ruta)
            current = df["Last"].iloc[0]
            wk = df["Change"].iloc[0]
            change = df["%Chg"].iloc[0]
            # Agregar el símbolo "%" a la columna Change
            change = f"{change}%"
            
            # Formatear según el tipo de registro:
            if nombre in ["North American Rigs", "United States Rigs"]:
                # Para estos, convertir a entero y luego a cadena (sin decimales)
                current_formatted = str(int(round(current)))
                wk_formatted = str(int(round(wk)))
            else:
                # Para el resto, redondear a 2 decimales y formatear como cadena
                current_formatted = f"{round(current, 2):.2f}"
                wk_formatted = f"{round(wk, 2):.2f}"
            
            # Se utiliza el valor original de wk para determinar la tendencia
            try:
                numeric_change = float(wk) if isinstance(wk, (int, float)) else float(str(wk).replace('%', '').strip())
            except Exception:
                numeric_change = 0.0
            trend = "↑" if numeric_change > 0 else "↓" if numeric_change < 0 else "="
        except Exception as e:
            current_formatted, wk_formatted, change, trend = None, None, None, None
            print(f"Error al leer {ruta}: {e}")
            
        filas.append({
            "Statistic": nombre,
            "Current": current_formatted,
            "Wk": wk_formatted,
            "Trend": trend,
            "Change": change,
            "Source": sources[idx]
        })
    
    tabla = pd.DataFrame(filas, columns=["Statistic", "Current", "Wk", "Trend", "Change", "Source"])
    return tabla

def crear_tabla_datos_mes(International, NorthAmerica, WorldWide):
    
    archivos = {
        "International Rigs": International,
        "North American Rigs": NorthAmerica,
        "World Wide Rigs": WorldWide
    }
    
    filas = []
    
    for nombre, ruta in archivos.items():
        try:
            df = pd.read_csv(ruta)
            current = df["Last"].iloc[0]
            current = int(current)
            mo = df["Change"].iloc[0]
            mo = int(mo)
            change = df["%Chg"].iloc[0]
            # Agregar el símbolo "%" a la columna Change
            change = f"{change}%"
            try:
                numeric_change = float(mo) if isinstance(mo, (int, float)) else float(str(mo).replace('%', '').strip())
            except Exception:
                numeric_change = 0.0
            trend = "↑" if numeric_change > 0 else "↓" if numeric_change < 0 else "="
        except Exception as e:
            current, mo, change, trend = None, None, None, None
            print(f"Error al leer {ruta}: {e}")
            
        filas.append({
            "Statistic": nombre,
            "Current": current,
            "Mo": mo,
            "Trend": trend,
            "Change": change,
            "Source": "Baker Hughes"
        })
    
    tabla = pd.DataFrame(filas, columns=["Statistic", "Current", "Mo", "Trend", "Change", "Source"])
    return tabla

if __name__ == "__main__":
    # Crear tabla semanal
    tabla_resultante_semana = crear_tabla_datos_semana(
        "scraper/01HistoricalDatabase/01WTICrudeHistoricalSemana.csv",
        "scraper/01HistoricalDatabase/02NaturalGasCashHistoricalSemana.csv",
        "scraper/01HistoricalDatabase/03GasolinePricesHistoricalSemana.csv",
        "scraper/01HistoricalDatabase/04OilServicesHistoricalSemana.csv",
        "scraper/01HistoricalDatabase/06NorthAmericanRigHistoricalSemana.csv",
        "scraper/01HistoricalDatabase/06USRigHistoricalSemana.csv",
        "scraper/01HistoricalDatabase/07USPetroleumStockHistoricalSemana.csv"
    )
    
    print("Tabla Semanal:")
    print(tabla_resultante_semana)
    
    # Verificar o crear carpeta 'csvPDF'
    output_dir = "csvPDF-Page1"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Guardar tabla semanal en 'csvSemanal.csv'
    output_file_semanal = os.path.join(output_dir, "csvSemanal.csv")
    tabla_resultante_semana.to_csv(output_file_semanal, index=False)
    print(f"La tabla semanal ha sido guardada en '{output_file_semanal}'.")
    
    # Crear tabla mensual
    tabla_resultante_mes = crear_tabla_datos_mes(
        "../01HistoricalDatabase/10InternationalRigMensual.csv",
        "../01HistoricalDatabase/11NorthAmericaRigMensual.csv",
        "../01HistoricalDatabase/12WorldWideRigMensual.csv"
    )
    
    print("\nTabla Mensual:")
    print(tabla_resultante_mes)
    
    # Guardar tabla mensual en 'csvMes.csv'
    output_file_mensual = os.path.join(output_dir, "csvMes.csv")
    tabla_resultante_mes.to_csv(output_file_mensual, index=False)
    print(f"La tabla mensual ha sido guardada en '{output_file_mensual}'.")
