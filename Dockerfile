# Imagen oficial con Chromium ya preinstalado y listo para Playwright
FROM mcr.microsoft.com/playwright/python:v1.42.0-focal

# Establece el directorio de trabajo
WORKDIR /app

# Copia todo tu código al contenedor
COPY . .

# Instala tus dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto que usará Flask
ENV PORT=10000
EXPOSE $PORT

# Ejecuta la app con Gunicorn (mejor que usar Flask directamente en producción)
CMD ["gunicorn", "-b", "0.0.0.0:10000", "main:app"]


