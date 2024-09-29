#----------------------------------------------------------------------------------

import psycopg2
import pandas as pd
from datetime import datetime
import json
import configparser
import sqlalchemy as sa
import requests
from sqlalchemy import create_engine

#-----------------------------------------------------------------------------

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

#  lista de diccionarios con la nueva columna "FechaConsulta"

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

#-------------------------------------------------------------------------------------------- 

tablaName1= 'clima_actual_tablaprincipal'.lower()

CONSULTA1 = f'''
    CREATE TABLE IF NOT EXISTS {tablaName1} (
        
        FechaConsulta    TIMESTAMP PRIMARY KEY,
        temp             DECIMAL(10, 2),
        feels_like       DECIMAL(10, 2),
        temp_min         DECIMAL(10, 2),
        temp_max         DECIMAL(10, 2),
        pressure         DECIMAL(10, 2),
        humidity         DECIMAL(5, 2)
    )
    DISTSTYLE ALL
    SORTKEY (FechaConsulta );
'''

def crear_nueva_tabla(consulta, tabla_name1):
    with Con.connect() as connection:
        connection.execute(consulta)
        print('Si la tabla principal existía, se mantuvo. Si no, se ha creado una nueva.')

crear_nueva_tabla(CONSULTA1, tablaName1)


#---------------------------------------------------------------------------------------------

nombre_tabla2 = 'clima_actual_staging'.lower()


CONSULTA2 = f'''
    BEGIN TRANSACTION;
    CREATE TABLE IF NOT EXISTS "{nombre_tabla2}" (

        FechaConsulta    TIMESTAMP PRIMARY KEY,
        temp             DECIMAL(10, 2),
        feels_like       DECIMAL(10, 2),
        temp_min         DECIMAL(10, 2),
        temp_max         DECIMAL(10, 2),
        pressure         DECIMAL(10, 2),
        humidity         DECIMAL(5, 2)
    )
    DISTSTYLE ALL
    SORTKEY (FechaConsulta);
    END TRANSACTION;
'''


def cargar_tabla_staging(consulta2, tabla_name2, data):
    
    with Con.connect() as connection:
        connection.execute(consulta2)
        print("si la tabla steging no existe se creará, si exite se cargará.")


        data.to_sql(
            name=tabla_name2,
            con=Con, 
            index=False,
            method='multi',
            if_exists='append'
        )

        print('Cargando la tabla staging en Redshift... ')

cargar_tabla_staging(CONSULTA2, nombre_tabla2, data)


print("Todo el código ha corrido exitosamente.")
