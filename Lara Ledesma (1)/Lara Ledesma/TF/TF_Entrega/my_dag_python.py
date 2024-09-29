from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

#----------------------------------------------------------------------

def extraccion_y_transf_datos():
    ruta_Archivo = "parametros_API2.json"
    url_base = "https://api.openweathermap.org/data/2.5/weather"
    with open(ruta_Archivo) as f:
        Parametros = json.load(f)

    RESPUESTA = requests.get(url_base, params=Parametros)

    if RESPUESTA.status_code == 200:
        print("Correcto, el código de estado es 200.")
    else:
        print(f"No es correcto, el código de estado es {RESPUESTA.status_code}")

    data_json = RESPUESTA.json()
    data = data_json["main"]
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_con_fecha = [{"FechaConsulta": fecha_actual, **data}]
    data = pd.DataFrame(data_con_fecha)
    return(data)

#------------------------------------------------------------------

default_args = {
    'owner': 'Lara_Ledesma',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

# Crea el objeto DAG
with DAG (
    default_args=default_args,
    dag_id="clima",
    start_date= datetime(2023, 9, 27),
    end_date =datetime(2023, 10, 30),
    schedule_interval="@daily",  
    ) as dag:

    # Define una conexión a la base de datos PostgreSQL
    postgres_conn_id = "postgres_default"

    # Crea una tarea PythonOperator para ejecutar el script completo
    run_python_script = PythonOperator(
        task_id='ejecutar_script_completo',
        python_callable= extraccion_y_transf_datos,
    )

    # Crea una tarea PostgresOperator para crear la tabla
    create_table_task = PostgresOperator(
        task_id="crea_tabla",
        sql="CREATE TABLE IF NOT EXISTS clima_actual(FechaConsulta TIMESTAMP PRIMARY KEY, temp DECIMAL(10, 2), feels_like DECIMAL(10, 2), temp_min DECIMAL(10, 2), temp_max DECIMAL(10, 2), pressure DECIMAL(10, 2), humidity DECIMAL(5, 2)) DISTSTYLE ALL SORTKEY (FechaConsulta);",
        postgres_conn_id=postgres_conn_id,
    )

    # Crea una tarea PostgresOperator para insertar los datos extraídos de la API
    insert_data_task = PostgresOperator(
        task_id="inserta_datos",
        sql="INSERT INTO clima_actual(FechaConsulta, temp, feels_like, temp_min, temp_max, pressure, humidity) VALUES (%s, %s, %s, %s, %s, %s, %s);",
        postgres_conn_id=postgres_conn_id,
        params=[(row["FechaConsulta"], row["temp"], row["feels_like"], row["temp_min"], row["temp_max"], row["pressure"], row["humidity"]) for row in extraccion_y_transf_datos().to_dict(orient="records")]
    )

    # Example of a task that sends an email
    send_email = EmailOperator(
        task_id='enviar_correo',
        to='berenice.ledesma12345@gmail.com',
        subject='TAREAS EJECUTADAS EXITOSAMENTE',
        html_content='<p>Todas las tareas se han ejecutado exitosamente.</p>',
    )

# Define the dependencies between tasks
    run_python_script >> create_table_task >> insert_data_task >> send_email
