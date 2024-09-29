# Utiliza la imagen base de Python
FROM python

# Establece el directorio de trabajo en el contenedor
WORKDIR /archivos/

# Copia todos los archivos y carpetas desde la carpeta actual (que contiene Dockerfile) en tu sistema local al contenedor
COPY . /archivos/

# Instala las dependencias desde el archivo "requirements.txt"
RUN pip install -r /archivos/librerias.txt

# Expone el puerto 5439 (si es necesario)
EXPOSE 5439

CMD ["python", "/archivos/script_completo_ultimo_definitivo.py"]

