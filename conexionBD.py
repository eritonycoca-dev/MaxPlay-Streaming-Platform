import pyodbc

def obtener_conexion():
    try:
        conexion = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=.\\SQLEXPRESS;"
            "DATABASE=StreamingDB;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        return conexion
    except Exception as e:
        print("Error al conectar con la base de datos:", e)
        return None
    
