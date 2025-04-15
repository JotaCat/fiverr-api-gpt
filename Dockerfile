# Usa una imagen oficial optimizada de Python
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Instala dependencias necesarias del sistema y herramientas
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Instala navegadores para Playwright
RUN python -m playwright install --with-deps

# Expone el puerto usado por Flask
EXPOSE ${PORT}

# Comando de inicio
CMD ["python", "main.py"]
