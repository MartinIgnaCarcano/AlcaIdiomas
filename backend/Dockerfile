FROM python:3.11-slim

# Crear el directorio de trabajo
WORKDIR /app

# Copiar los archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expone el puerto del servidor Flask
EXPOSE 5000

# Comando para correr la app
CMD ["python", "run.py"]