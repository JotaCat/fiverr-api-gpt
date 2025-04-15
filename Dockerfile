# Usa una imagen oficial de Python
FROM python:3.11-slim

# Instala dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    curl gnupg unzip \
    && rm -rf /var/lib/apt/lists/*

# Instala Playwright y navegadores
RUN pip install --no-cache-dir playwright flask gunicorn
RUN playwright install --with-deps

# Crea directorio para el código
WORKDIR /app

# Copia todo el código
COPY . .

# Expone el puerto que usará Flask
ENV PORT=10000
EXPOSE $PORT

# Comando para arrancar la app con Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:10000", "main:app"]

