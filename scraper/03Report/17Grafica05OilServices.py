import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Verificar si existe la carpeta "graficas", de lo contrario se crea.
if not os.path.exists("scraper/03Report/graficas"):
    os.makedirs("scraper/03Report/graficas")

# Cargar el archivo CSV ubicado en "./historicalDatabase/04OilServicesHistoricalSemana.csv"
csv_path = "scraper/01HistoricalDatabase/04OilServicesHistoricalSemana.csv"
df = pd.read_csv(csv_path)

# Convertir la columna "Time" a tipo datetime y ordenar (en caso de que no lo esté)
df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%y')
df.sort_values('Time', inplace=True)

# Crear la figura y la gráfica de línea en color rojo con el label "OSX"
plt.figure(figsize=(10, 5.5))
plt.plot(df['Time'], df['Last'], color='red', label='OSX')

# Configurar los intervalos del eje Y: de 0 a 120 en pasos de 20
plt.yticks(range(0, 121, 20))
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
    plt.text(df.loc[idx, 'Time'], 100, str(df.loc[idx, 'Time'].year),
             rotation=90, verticalalignment='bottom', fontsize=8)
    
    # Anotación con el valor "Last" y la fecha del dato
    plt.annotate(f"({df.loc[idx, 'Time'].strftime('%m/%d/%y')}) {df.loc[idx, 'Last']}", 
                 xy=(df.loc[idx, 'Time'], df.loc[idx, 'Last']),
                 xytext=(df.loc[idx, 'Time'], df.loc[idx, 'Last'] - 10),
                 arrowprops=dict(facecolor='green', arrowstyle='->'),
                 fontsize=9)

# Resaltar el primer dato de la gráfica con su valor y fecha
if len(df) > 0:
    plt.annotate(f"({df.iloc[0]['Time'].strftime('%m/%d/%y')}) {df.iloc[0]['Last']}", 
                 xy=(df.iloc[0]['Time'], df.iloc[0]['Last']),
                 xytext=(df.iloc[0]['Time'], df.iloc[0]['Last'] + 5),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=9)
    
# Resaltar el último dato de la gráfica con su valor y fecha
if len(df) > 0:
    plt.annotate(f"({df.iloc[-1]['Time'].strftime('%m/%d/%y')}) {df.iloc[-1]['Last']}", 
                 xy=(df.iloc[-1]['Time'], df.iloc[-1]['Last']),
                 xytext=(df.iloc[-1]['Time'], df.iloc[-1]['Last'] + 5),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=9)

# Colocar la leyenda en la esquina inferior izquierda
plt.legend(loc='lower left')

# Agregar el texto "finance.yahoo.com \n ^OSX" en la esquina inferior derecha de la gráfica
plt.text(1, 0, "finance.yahoo.com \n ^OSX", transform=plt.gca().transAxes,
         ha='right', va='bottom', fontsize=9)

plt.tight_layout()

# Guardar la gráfica en la carpeta "graficas" con el nombre "04OilServices.png"
plt.savefig("scraper/03Report/graficas/04OilServices.png")
plt.close()
