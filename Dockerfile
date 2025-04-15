# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Instala dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
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
    && rm -rf /var/lib/apt/lists/*

# Crea y establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias del proyecto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Instala navegadores de Playwright
RUN playwright install --with-deps

# Expone el puerto que Render espera
ENV PORT=10000
EXPOSE 10000

# Ejecuta la app
CMD ["python", "main.py"]
