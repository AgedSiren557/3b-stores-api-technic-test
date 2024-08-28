# Seleccionamos la imagen base de Python 3.8
FROM python:3.8-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los requisitos de la aplicación
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiamos el código de la aplicación
COPY . .

# Establecemos la variable de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Ejecutamos el comando para iniciar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]