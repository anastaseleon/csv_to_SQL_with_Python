import pandas as pd
import pyodbc
import logging

def load_bank_statement(filename, encoding='utf-8'):
    transactions = pd.read_csv(filename, encoding=encoding)
    return transactions

def save_transactions(df, transactions_table_name, files_table_name, conn, filename):
    cursor = conn.cursor()
    
    try:
        # Create transactions table if it doesn't exist
        columns = ', '.join([f'[{col}] NVARCHAR(MAX)' if df[col].dtype == 'object' else f'[{col}] FLOAT' if df[col].dtype == 'float' else f'[{col}] INT' for col in df.columns])
        create_transactions_table_query = f'''
        IF OBJECT_ID(N'{transactions_table_name}', N'U') IS NULL
        BEGIN
            CREATE TABLE {transactions_table_name} (
                [id] INT IDENTITY(1,1) PRIMARY KEY,
                {columns},
                [filename] NVARCHAR(255),
                [category] NVARCHAR(255) DEFAULT ''
            )
        END
        '''
        cursor.execute(create_transactions_table_query)

        # Create files table if it doesn't exist
        create_files_table_query = f'''
        IF OBJECT_ID(N'{files_table_name}', N'U') IS NULL
        BEGIN
            CREATE TABLE {files_table_name} (
                [id] INT IDENTITY(1,1) PRIMARY KEY,
                [filename] NVARCHAR(255) UNIQUE
            )
        END
        '''
        cursor.execute(create_files_table_query)

        # Insert filename into the files table
        cursor.execute(f"INSERT INTO {files_table_name} (filename) VALUES (?)", filename)
        conn.commit()

        # Insert data into the transactions table
        insert_query = f'''
        INSERT INTO {transactions_table_name} ({', '.join([f'[{col}]' for col in df.columns])}, [filename], [category]) 
        VALUES ({', '.join(['?' for _ in df.columns])}, ?, '')
        '''
        for index, row in df.iterrows():
            cursor.execute(insert_query, *row, filename)
        conn.commit()

    except Exception as e:
        logging.error(f"Failed to save transactions: {e}")
        conn.rollback()
        raise

    finally:
        cursor.close()

def import_statement(file_path, encoding, conn, transactions_table_name, files_table_name, filename):
    try:
        transactions = load_bank_statement(file_path, encoding)
        save_transactions(transactions, transactions_table_name, files_table_name, conn, filename)
    except Exception as e:
        logging.error(f"Failed to import statement: {e}")
        raise
