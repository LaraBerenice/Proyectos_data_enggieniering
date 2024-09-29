from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import psycopg2
import pandas as pd
from datetime import datetime
import json
import configparser
import sqlalchemy as sa
import requests
from sqlalchemy import create_engine

# Define una función que encapsula todo tu script
def ejecutar_script_completo():
    ruta_Archivo = "parametros_API2.json"
    url_base = "https://api.openweathermap.org/data/2.5/weather"
    with open(ruta_Archivo) as f:
        Parametros = json.load(f)

    # PEDIDO DE INFORMACION Y dataframe : -----------------------------------
    RESPUESTA = requests.get(url_base, params=Parametros)

    if RESPUESTA.status_code == 200:
        print("correcto es igual a 200")
    else:
        print(f"no es correcto es igual a {RESPUESTA.status_code}")

    # TRANSFORMACION DE DATOS:
    data_json = RESPUESTA.json()
    data = data_json["main"]
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # lista de diccionarios con la nueva columna "FechaConsulta"
    data_con_fecha = [{"FechaConsulta": fecha_actual, **data}]
    data = pd.DataFrame(data_con_fecha)
    print(data)

    # CONEXION A REDSHIFT -------------------------------------
    Archivo_Config = "config.ini"

    def Con_redshift(ruta_archivo):
        config = configparser.ConfigParser()
        config.read(ruta_archivo)
        conn_data = config['redshift']

        host = conn_data['host']
        port = conn_data['port']
        db = conn_data['db']
        user = conn_data['user']
        pws = conn_data['pws']
        schema = conn_data['user']

        conn_url = f"redshift+psycopg2://{user}:{pws}@{host}:{port}/{db}?sslmode=require"

        Con = sa.create_engine(conn_url, connect_args={"options": f"-csearch_path={schema}"})

        return Con

    Con = Con_redshift(Archivo_Config)

    # Crear tablas y cargar datos en Redshift aquí...

    # Puedes agregar más lógica y operaciones aquí según sea necesario.

# Configuración del DAG
default_args = {
    'owner': 'berenice.ledesma12345@gmail.com',
    'depends_on_past': True,
    'start_date': datetime(2023, 9, 14),
    'end_date': datetime(2023, 9, 14),
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mi_dag_python',
    default_args=default_args,
    description='Ejecutar un script en Airflow usando PythonOperator',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# Crea un PythonOperator que ejecutará la función "ejecutar_script_completo"
ejecutar_script_etl = PythonOperator(
    task_id='ejecutar_script',
    python_callable=ejecutar_script_completo,  # Llama a la función que contiene tu script ETL
    dag=dag,
)

# Define el orden de las tareas
ejecutar_script_etl 




