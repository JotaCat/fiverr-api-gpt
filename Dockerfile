FROM python:3.11-slim

# Instalar librerías necesarias para que Chromium funcione
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    libglib2.0-0 libnss3 libnspr4 libdbus-1-3 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxcb1 libxkbcommon0 libatspi2.0-0 libx11-6 \
    libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxrandr2 libgbm1 libpango-1.0-0 libcairo2 \
    libasound2 fonts-liberation libappindicator3-1 xdg-utils

# Crear carpeta del proyecto y copiarlo
WORKDIR /app
COPY . /app

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Playwright y Chromium
RUN pip install playwright
RUN playwright install chromium

# Exponer el puerto de Flask
EXPOSE 3000

# Comando para iniciar la app
CMD ["python", "main.py"]
