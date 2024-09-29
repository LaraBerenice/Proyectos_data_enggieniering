
FROM apache/airflow:2.7.0

USER root

RUN apt-get update && apt-get install -y supervisor

USER airflow

WORKDIR /opt/airflow

COPY my_dag_python.py /opt/airflow/dags/my_dag_python.py
COPY airflow.cfg /opt/airflow/airflow.cfg
COPY config.ini /opt/airflow/config.ini
COPY librerias.txt /opt/airflow/librerias.txt
COPY parametros_API2.json /opt/airflow/parametros_API2.json

RUN airflow db init


RUN airflow users create \
    --username lara \
    --firstname Lara \
    --lastname Berenice \
    --role Admin \
    --email berenice.ledesma12345@gmail.com \
    --password lara


CMD ["airflow", "scheduler", "&", "airflow", "webserver"]
