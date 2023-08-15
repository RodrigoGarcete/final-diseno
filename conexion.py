import pymysql

# Configura tus credenciales de base de datos aquí
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'db': 'sistema_pw2',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

conexion = pymysql.connect(**db_config)
