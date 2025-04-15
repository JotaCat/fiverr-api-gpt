# Usa una imagen de Python con dependencias de navegador
FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

# Crea un directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias
RUN pip install -r requirements.txt

# Expón el puerto que usa Flask
EXPOSE 3000

# Comando para iniciar la app
CMD ["python", "main.py"]
