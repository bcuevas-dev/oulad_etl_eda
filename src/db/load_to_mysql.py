import pandas as pd
import numpy as np
import mysql.connector
import os
from sqlalchemy import create_engine

# Importamos la configuracion de mysql desde settings.py 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings

# Creamos el engine usando SQLAlchemy
engine = create_engine(settings.SQLALCHEMY_URL)

TABLES = [
    ('courses', 'courses_clean.csv'),
    ('studentInfo', 'student_info_clean.csv'),
    ('assessments', 'assessments_clean.csv'),
    ('studentAssessment', 'student_assessments_clean.csv'),
    ('vle', 'vle_clean.csv'),
    ('studentVle', 'student_vle_clean.csv'),
    ('studentRegistration', 'student_registration_clean.csv')
]

DATE_COLUMNS = {
    'studentRegistration': ['date_registration', 'date_unregistration'],
    'studentAssessment': ['date_submitted'],
    'studentVle': ['date']
}

def convert_dates(df, date_cols):
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            df[col] = df[col].dt.date
            df[col] = df[col].where(df[col].notnull(), None)
    return df

def insert_batch(cursor, sql, data, batch_size=1000):
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        cursor.executemany(sql, batch)

def load_csv_to_mysql(table_name, csv_path, conn):
    try:
        df = pd.read_csv(csv_path)

        df.columns = [str(col).strip() for col in df.columns]
        df = df.loc[:, df.columns.notna()]
        df = df.loc[:, ~df.columns.str.lower().isin(['nan', 'none', ''])]
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]

        df = df.replace({np.nan: None})

        if table_name in DATE_COLUMNS:
            df = convert_dates(df, DATE_COLUMNS[table_name])

        cursor = conn.cursor()
        print(f"Cargando {csv_path} en la tabla {table_name}...")

        columns = ', '.join(f"`{col}`" for col in df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        updates = ', '.join([f"`{col}` = VALUES(`{col}`)" for col in df.columns])
        sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {updates}"

        data = [tuple(row) for row in df.to_numpy()]
        insert_batch(cursor, sql, data)
        conn.commit()
        print(f"{len(data)} filas insertadas/actualizadas en {table_name}.\n")

    except Exception as e:
        print(f"Error al insertar datos en {table_name}: {e}")

def main():
    try:
        # Conexión desde el settings 
        conn = mysql.connector.connect(**settings.DB_CONFIG)
        print("Conectado a MySQL.")

        for table, filename in TABLES:
            path = os.path.join('data', 'cleaned', filename)
            if os.path.exists(path):
                load_csv_to_mysql(table, path, conn)
            else:
                print(f"Archivo no encontrado: {path}")

        conn.close()
        print("Carga finalizada correctamente.")

    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")

if __name__ == '__main__':
    main()
