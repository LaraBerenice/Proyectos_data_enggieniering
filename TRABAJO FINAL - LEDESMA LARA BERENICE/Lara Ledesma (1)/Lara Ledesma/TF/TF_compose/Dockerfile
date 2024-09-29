
FROM apache/airflow:2.7.0

USER root

RUN  apt-get update

USER airflow

ENV PYTHONPATH "{$PYTHONPATH}:/opt/airflow/"

COPY requirements.txt .

COPY parametros_API2.json .

RUN pip install -r librerias.txt

COPY  . . 



