# Proyecto OULAD: ETL y Análisis Exploratorio de Datos (EDA)

## Descripción

Este proyecto implementa un flujo completo de ETL (Extracción, Transformación y Carga) y Análisis Exploratorio de Datos sobre el dataset OULAD (EDA). El objetivo es limpiar, transformar y analizar los datos para obtener insights relevantes.

## Tecnologías Utilizadas

| Componente        | Tecnología                   |
|-------------------|------------------------------|
| Lenguaje          | Python 3.12                  |
| Visualizaciones   | Matplotlib, Seaborn          |
| Machine Learning  | Scikit-Learn                 |
| Base de Datos     | MySQL                        |
| IDE               | VS Code                      |

---

## Clonar el Proyecto

Para obtener una copia local del repositorio, ejecuta:

```bash
git clone https://github.com/bcuevas-dev/oulad_etl_eda.git
cd oulad_etl_eda
```

---

## Descarga del Dataset OULAD

Para trabajar con este proyecto, necesitas descargar los archivos CSV originales del dataset OULAD:

1. Accede a la página oficial del dataset:  
      [Open University Learning Analytics Dataset (OULAD)](https://analyse.kmi.open.ac.uk/open_dataset)
2. Descarga el archivo ZIP que contiene los datos.
3. Extrae los archivos CSV del ZIP descargado.
4. Copia todos los archivos CSV extraídos en la carpeta `data/original/` del proyecto.


## Estructura del Proyecto

```
data/
      ├─ original/         # Archivos CSV originales
      └─ cleaned/          # Archivos CSV limpios tras ETL
outputs/
      ├─ figures/          # Gráficos generados por EDA
      └─ reports/          # Reportes y documentos finales
src/
      ├─ etl/              # Scripts Python para ETL
      ├─ eda/              # Scripts Python para EDA
      ├─ db/               # Scripts para carga a MySQL y manejo de base de datos
      └─ config/           # Configuración del proyecto (settings.py)
sql/                       # Scripts SQL para creación de base de datos/tablas
requirements.txt           # Dependencias del proyecto
README.md                  # Documentación y guía de uso
```

---

## Instalación de Dependencias

Instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

---

## Configuración de la Base de Datos

1. Crea la base de datos en MySQL:
       ```sql
       CREATE DATABASE oulad_db;
       USE oulad_db;
       ```
2. Ejecuta el script `create_oulad.sql` desde la carpeta `sql/` usando MySQL Workbench u otro cliente.

3. Configuración de conexión utilizada en el proyecto (ver [`src/config/settings.py`](src/config/settings.py)):
    ```python
    DB_CONFIG = {
         'user': 'root',
         'password': 'A.123456',
         'host': 'localhost',
         'database': 'oulad_db'
    }

    SQLALCHEMY_URL = (
         f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
    )
    ```
    > **Nota:** Modifica estos valores según tu entorno local antes de ejecutar los scripts.

---

## Ejecución del ETL

1. Coloca los archivos CSV originales en `data/original/`.
2. Ejecuta el script de ETL:
       ```bash
       python src/etl/etl_oulad.py
       ```
       - Limpia datos nulos y transforma valores categóricos a ordinales.
       - Crea nuevos campos (ordinales, booleanos).
       - Guarda los archivos limpios en `data/cleaned/`.

---

## Carga de Datos a MySQL

Ejecuta:
```bash
python src/db/load_to_mysql.py
```
- Crea las tablas si no existen.
- Carga los archivos limpios a MySQL.
- Mantiene la integridad referencial (PK y FK).

---

## Análisis Exploratorio de Datos (EDA)

Ejecuta:
```bash
python src/eda/eda_oulad.py
```
- Genera matrices de correlación y confusión.
- Crea histogramas, boxplots y gráficos de dispersión.
- Analiza variables como `final_result`, `age_band`, `disability`, entre otras.
- Guarda los gráficos en `outputs/figures/`.

También puedes explorar los datos y resultados en los notebooks de la carpeta `notebooks/`.

---

## Resultados y Reportes

- Revisa los gráficos en `outputs/figures/`.
- Consulta los reportes generados en `outputs/reports/`.

---

## Contacto

Para dudas o sugerencias, puedes contactar al equipo del proyecto:

- **Bienvenido Cuevas**
- **Ana Esther Segura Reyes**
- **Ayzel Lavinia Mateo Luciano**

