import pyodbc
import os

def get_db_connection():
    try:
        server = 'louverture'
        database = 'App'
        username ='app_user'
        password = 'password'

        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        return conn
    except pyodbc.Error as ex:
        print("Database connection failed:", ex)
        return None
