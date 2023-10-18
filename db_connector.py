import mysql.connector

def conectar_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='asistente_virtual'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

def cerrar_db(conn):
    if conn:
        conn.close()
