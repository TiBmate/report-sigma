#!/bin/bash

echo "Eliminando directorios"
rm -rf /var/www/html/scraper/
rm -rf /var/www/html/static/
rm -rf /var/www/html/templates/
rm /var/www/html/app.py

echo -e "\nCopiando directorios"
cp -r /home/it/Proyects/report-sigma/scraper/  /var/www/html/
cp -r /home/it/Proyects/report-sigma/static/  /var/www/html/
cp -r /home/it/Proyects/report-sigma/templates/  /var/www/html/
cp /home/it/Proyects/report-sigma/app.py /var/www/html/

echo -e "\nOtorgando permisos a carpetas"
chmod -R 777 /var/www/html/scraper/
chmod -R 777 /var/www/html/static/
chmod -R 777 /var/www/html/templates/
chmod -R 777 /var/www/html/app.py

echo -e "\nReiniciando servidor Apache2"
systemctl restart apache2