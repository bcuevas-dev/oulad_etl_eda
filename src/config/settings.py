import os

# Ruta base del proyecto (por si necesitas usarla después)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuración de conexión MySQL
DB_CONFIG = {
    'user': 'root',
    'password': 'A.123456',
    'host': 'localhost',
    'database': 'oulad_db2'
}

# Cadena de conexión SQLAlchemy (para usar en EDA con create_engine)
SQLALCHEMY_URL = (
    f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
)
