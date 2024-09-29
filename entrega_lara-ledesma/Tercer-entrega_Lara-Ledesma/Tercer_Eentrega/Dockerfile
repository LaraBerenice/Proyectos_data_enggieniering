# Use la imagen base oficial de Apache Airflow
FROM apache/airflow:2.1.2

# Configura la variable de entorno AIRFLOW_HOME
ENV AIRFLOW_HOME=/opt/airflow

# Crea el directorio "dags" dentro del directorio de trabajo de Airflow
RUN mkdir -p $AIRFLOW_HOME/dags/

# Copia tus archivos DAG y dependencias
COPY my_dag_bash_operador.py $AIRFLOW_HOME/dags/
COPY librerias.txt $AIRFLOW_HOME/
COPY config.ini $AIRFLOW_HOME/
COPY parametros_API2.json $AIRFLOW_HOME/
COPY script_completo_ultimo_definitivo.py $AIRFLOW_HOME/

# Instala las dependencias de Python
RUN pip install -r $AIRFLOW_HOME/librerias.txt

# Expone el puerto 8080 para el servidor web de Airflow
EXPOSE 8080

# Inicializa la base de datos de Airflow (SQLite)
RUN airflow db init

# Crea la carpeta para almacenar las contraseñas
RUN mkdir -p /opt/airflow/secrets/

# Crea la contraseña aleatoria para el servidor web de Airflow
ENV AIRFLOW_USER_PASSWORD_FILE=/opt/airflow/secrets/airflow-user-password
RUN openssl rand -base64 32 > $AIRFLOW_USER_PASSWORD_FILE

# Crea un usuario de Airflow con el nombre de usuario "lara" y el rol de "Admin"
# Establece la contraseña de forma no interactiva
RUN airflow users create \
  --email berenice.ledesma12345@gmail.com \
  --firstname Lara \
  --lastname Ledesma \
  --role Admin \
  --username lara \
  --password $(cat $AIRFLOW_USER_PASSWORD_FILE)


# Inicia el scheduler de Airflow
CMD ["airflow", "scheduler"]

# Inicia el servidor web de Airflow en segundo plano
CMD ["airflow", "webserver"]

#docker exec -it etl_entrega3 cat /opt/airflow/secrets/airflow-user-password -- para ver la contrasena --