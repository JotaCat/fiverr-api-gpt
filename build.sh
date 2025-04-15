#!/bin/bash

# Instala dependencias del sistema
apt-get update
apt-get install -y wget unzip curl gnupg

# Instala Playwright y sus navegadores
pip install playwright
playwright install chromium
