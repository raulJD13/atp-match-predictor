# 1.  imagen de Python ligera y oficial (Linux)
FROM python:3.10-slim

# 2. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de dependencias primero (para aprovechar la caché de Docker)
COPY requirements.txt .

# 4. Instalamos las dependencias
# --no-cache-dir ayuda a que la imagen pese menos
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código del backend
# Copiamos la carpeta app y models
COPY app ./app
COPY models ./models

# 6. Exponemos el puerto 8000 (donde vive FastAPI)
EXPOSE 8000

# 7. El comando para arrancar el servidor cuando el contenedor se inicie
# --host 0.0.0.0 es OBLIGATORIO en Docker (significa "escucha en todas las direcciones")
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]