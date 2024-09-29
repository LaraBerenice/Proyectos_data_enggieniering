import psycopg2
import pandas as pd
from datetime import datetime
import json
import configparser
import sqlalchemy as sa
import requests
from sqlalchemy import create_engine

#-----------------------------------------------------------------------------------
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from commonx.script_completo_ultimo_definitivo import main
from airflow.operators.email_operator import EmailOperator

#-----------------------------------------------------------------------------------

default_args = {
    "owner": "LaraBerenice",
    "retries": 5,
    "retry_delay": timedelta(minutes=3)
}

with DAG(
    default_args=default_args,
    dag_id="id_etl_task",
    description="etl_task",
    start_date= datetime(2023, 9, 27), 
    schedule_interval= "@daily", 
) as dag:
    etl_task = PythonOperator(
        task_id="etl_task",
        python_callable= main
    )
    send_email = EmailOperator(
        task_id='enviar_correo',
        to='berenice.ledesma12345@gmail.com',
        subject='TAREAS EJECUTADAS EXITOSAMENTE',
        html_content='<p>Todas las tareas se han ejecutado exitosamente.</p>',
    )

etl_task >> send_email
