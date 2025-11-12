# Imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los archivos del microservicio al contenedor
COPY . .

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usa Flask
EXPOSE 5001

# Comando para ejecutar el microservicio
CMD ["python", "app.py"]
