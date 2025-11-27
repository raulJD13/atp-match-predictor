# 1. Imagen base ligera
FROM python:3.10-slim

# 2. Directorio de trabajo
WORKDIR /app

# 3. Copiamos dependencias e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiamos TODO el código del frontend (incluyendo la carpeta data con el CSV)
COPY . .

# 5. Exponemos el puerto de Streamlit
EXPOSE 8501

# 6. Comando para arrancar
# address 0.0.0.0 es vital para que se vea desde fuera del contenedor
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]