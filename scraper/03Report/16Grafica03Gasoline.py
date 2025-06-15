import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Verificar si existe la carpeta "graficas", de lo contrario se crea.
if not os.path.exists("graficas"):
    os.makedirs("graficas")

# Cargar el archivo CSV ubicado en "./historicalDatabase/03GasolinePricesHistoricalSemana.csv"
csv_path = "scraper/01HistoricalDatabase/03GasolinePricesHistoricalSemana.csv"
df = pd.read_csv(csv_path)

# Convertir la columna "Time" a tipo datetime y ordenar (en caso de que no lo esté)
df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%y')
df.sort_values('Time', inplace=True)

# Crear la figura y la gráfica de línea en color rojo con el label "$/gallon"
plt.figure(figsize=(10, 5.5))
plt.plot(df['Time'], df['Last'], color='red', label='$/gallon')

# Configurar los intervalos del eje Y: de 0 a 6 en pasos de 1
plt.yticks(range(0, 7, 1))
plt.grid(axis='y', color='grey', linestyle='--', linewidth=0.5)

# Configurar el eje X para usar las fechas del CSV, mostrando de a una cada tres
ax = plt.gca()
ticks = df['Time'][::3]
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
plt.xticks(rotation=90, fontsize=9)

# Dibujar líneas verticales en los cambios de año y agregar etiquetas con el año
years = df['Time'].dt.year
year_change_indices = df.index[years.diff().fillna(0) != 0].tolist()

for idx in year_change_indices:
    # Dibujar la línea vertical en el cambio de año
    plt.axvline(x=df.loc[idx, 'Time'], color='black', linestyle='--', linewidth=1)
    
    # Agregar etiqueta con el año sobre la línea
    plt.text(df.loc[idx, 'Time'], 4.5, str(df.loc[idx, 'Time'].year),
             rotation=90, verticalalignment='bottom', fontsize=8)
    
    # Anotación con el valor "Last" y la fecha del dato
    plt.annotate(f"({df.loc[idx, 'Time'].strftime('%m/%d/%y')}) {df.loc[idx, 'Last']}", 
                 xy=(df.loc[idx, 'Time'], df.loc[idx, 'Last']),
                 xytext=(df.loc[idx, 'Time'], df.loc[idx, 'Last'] - 0.5),
                 arrowprops=dict(facecolor='green', arrowstyle='->'),
                 fontsize=9)

# Resaltar el primer dato de la gráfica con su valor y fecha
if len(df) > 0:
    plt.annotate(f"({df.iloc[0]['Time'].strftime('%m/%d/%y')}) {df.iloc[0]['Last']}", 
                 xy=(df.iloc[0]['Time'], df.iloc[0]['Last']),
                 xytext=(df.iloc[0]['Time'], df.iloc[0]['Last'] + 0.3),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=9)
    
# Resaltar el último dato de la gráfica con su valor y fecha
if len(df) > 0:
    plt.annotate(f"({df.iloc[-1]['Time'].strftime('%m/%d/%y')}) {df.iloc[-1]['Last']}", 
                 xy=(df.iloc[-1]['Time'], df.iloc[-1]['Last']),
                 xytext=(df.iloc[-1]['Time'], df.iloc[-1]['Last'] + 0.3),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=9)

# Colocar la leyenda en la esquina inferior izquierda
plt.legend(loc='lower left')

# Agregar el texto en la esquina inferior derecha
plt.text(1, 0, "www.eia.gov \n Weekly U.S. Regular All Formulations Retail Gasoline Prices (Dollars per Gallon)", 
         transform=plt.gca().transAxes, ha='right', va='bottom', fontsize=9)

plt.tight_layout()

# Guardar la gráfica en la carpeta "graficas" con el nombre "03Gasoline.png"
plt.savefig("graficas/03Gasoline.png")
plt.close()
