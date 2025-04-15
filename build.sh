#!/bin/bash

# Instalar dependencias del sistema necesarias para Chromium
apt-get update
apt-get install -y wget unzip curl gnupg

# Instalar las dependencias de Python
pip install -r requirements.txt

# Instalar Playwright y descargar Chromium
pip install playwright
playwright install chromium
