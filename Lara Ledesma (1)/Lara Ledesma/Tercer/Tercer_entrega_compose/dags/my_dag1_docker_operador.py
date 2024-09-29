from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'berenice.ledesma12345@gmail.com',
    'start_date': datetime(2023, 9, 15),
    'end_date': datetime(2023, 9, 30),
    'retries': 5,
}

dag = DAG(
    'mi_dag_con_contenedor',
    default_args=default_args,
    description='Ejecutar un contenedor Docker en Airflow',
    schedule_interval="*/10 * * * *",  # Cada 10 minutos
)

# Define a task to build the Docker image
correr_image_task = BashOperator(
    task_id='build_image',
    bash_command='docker build -t imagen_compose3 ccba530a67f9:/opt/airflow/archivos . ',
    dag=dag,
)



run_container_task = DockerOperator(
    task_id='run_container',
    image='imagen_compose3',  # Nombre de la imagen Docker
    api_version='auto',  # Puedes configurar la versión de la API de Docker aquí
    auto_remove=True,  # Eliminar el contenedor después de la ejecución
    network_mode='bridge',  # Modo de red (ajusta según tus necesidades)
    dag=dag,
)


correr_image_task >> run_container_task


