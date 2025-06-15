#!/bin/bash

# Activar el entorno virtual report2

eval "$(conda shell.bash hook)"
conda activate /home/baltazarleon/anaconda3/envs/sigma-report

#!/bin/bash

echo -e "\n🔁 Activating Conda environment..."
# Properly initialize Conda, even from a standalone .sh
eval "$(conda shell.bash hook)"
conda activate sigma-report || {
    echo "❌ Error: Failed to activate the 'sigma-report' environment."
    exit 1
}

echo -e "\n🔍 Checking Playwright browser installation..."

# Check if browsers are installed (dry-run doesn't download anything)
if ! playwright install --with-deps --dry-run &> /dev/null; then
    echo "⚙️ Playwright browsers are missing. Installing now..."
    playwright install
else
    echo "✅ Playwright browsers already installed."
fi


# Elimnar la carpeta csv
echo -e "\n Eliminando carpeta CSV ..."
rm -rf ./scraper/02DatosSitiosWeb/csv



echo -e "\n====== Iniciando descarga de datos de sitios web ======"

# Ejecutar los scripts uno por uno mostrando mensajes en terminal
echo -e "\n Ejecutando 01WTICrude.py..."
python ./scraper/02DatosSitiosWeb/01WTICrude.py

echo -e "\n Ejecutando 02NaturalGasCash.py..."
python ./scraper/02DatosSitiosWeb/02NaturalGasCash.py

echo -e "\n Ejecutando 03GasolinePrices.py..."
python ./scraper/02DatosSitiosWeb/03GasolinePrices.py

echo -e "\n Ejecutando 04OilServicesSector.py..."
python ./scraper/02DatosSitiosWeb/04OilServicesSector.py

echo -e "\n Ejecutando 05NaturalGasStorage.py..."
python ./scraper/02DatosSitiosWeb/05NaturalGasStorage.py

echo -e "\n Ejecutando 06NorthAmericanRig.py..."
python ./scraper/02DatosSitiosWeb/06NorthAmericanRig.py

echo -e "\n Ejecutando 06USRigs.py..."
python ./scraper/02DatosSitiosWeb/06USRigs.py

echo -e "\n Ejecutando 07USCrudeOilInventory.py..."
python ./scraper/02DatosSitiosWeb/07USCrudeOilInventory.py



echo -e "\n====== Integrando los datos de sitios web con datos historicos ======"

# Ejecutar el helper de integración de datos de sitio web con datos historicos
python ./scraper/10HelperWeb-HistoricoSemanal.py



echo -e "\n====== Generando tablas de reportes ======"

# Tablas de reportes que se muestran en el sitio web y en el PDF (futuro desarrollo)
echo -e "\nTabla de reporte 1 ..."
python ./scraper/03Report/11HelperPDF-Page1.py

echo -e "\nTabla de reporte 2 ..."
python ./scraper/03Report/12HelperPDF-Page2.py



echo -e "\n====== Iniciando la geneación de gráficas ======"

echo -e "\nEliminando gráficas anteriores"
rm ./scraper/03Report/graficas/*.png
rm ./static/img/*.png

echo -e "\nNuevas gráficas"

echo -e "\nGráfica WTI ..."
python ./scraper/03Report/14Grafica01WTI.py

echo -e "\nGráfica NaturalGas ..."
python ./scraper/03Report/15Grafica02NaturalGas.py

echo -e "\nGráfica Gasoline ..."
python ./scraper/03Report/16Grafica03Gasoline.py

echo -e "\nGráfica OilServices ..."
python ./scraper/03Report/17Grafica05OilServices.py

cp -r ./scraper/03Report/graficas/*.png ./static/img/



# echo -e "\n====== Reiniciando servidor Apache2 para reflejar cambios ======"
# systemctl restart apache2

echo -e "\n====== Cambios realizados ======"


# Desactivar el entorno virtual al finalizar
deactivate
