# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Instala dependencias necesarias del sistema para Playwright
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    libglu1-mesa \
    libpango-1.0-0 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    libappindicator3-1 \
    lsb-release \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Crea directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Instala Playwright y su navegador Chromium
RUN playwright install chromium

# Expone el puerto que Render espera
ENV PORT=10000
EXPOSE 10000

# Ejecuta la aplicación con Gunicorn
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:10000"]

