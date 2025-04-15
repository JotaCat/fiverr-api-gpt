# Imagen oficial con Playwright + Chromium listo para usar
FROM mcr.microsoft.com/playwright/python:v1.42.0-focal

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el código fuente al contenedor
COPY . .

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto que usará Flask
ENV PORT=10000
EXPOSE $PORT

# Inicia la app con Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:10000", "main:app"]
