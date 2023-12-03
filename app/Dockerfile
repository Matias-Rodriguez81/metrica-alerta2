# Usa la imagen oficial de Python
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el código de la aplicación a la ubicación /app en el contenedor
COPY . /app

# Instala las dependencias de la aplicación
COPY requirements.txt .
RUN pip install -r requirements.txt
# Expone el puerto 8000 para la API
EXPOSE 8000


# Comando para iniciar la aplicación utilizando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
