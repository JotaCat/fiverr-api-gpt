# Usa una imagen oficial de Python
FROM python:3.11-slim

# Instala dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    curl gnupg unzip fonts-liberation libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libdrm2 libgtk-3-0 libnspr4 libnss3 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libxss1 libxtst6 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
RUN pip install --no-cache-dir flask gunicorn playwright

# Instala navegadores para Playwright
RUN playwright install --with-deps

# Establece el directorio de trabajo
WORKDIR /app

# Copia todos los archivos del proyecto
COPY . .

# Expone el puerto que usará Flask
ENV PORT=10000
EXPOSE $PORT

# Usa Gunicorn para producción
CMD ["gunicorn", "-b", "0.0.0.0:10000", "main:app"]


