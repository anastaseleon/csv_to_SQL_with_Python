from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pyodbc
from datetime import datetime
from bank_statement_tool.importer import import_statement

app = Flask(__name__)
CORS(app)

# Access environment variables
server = os.getenv('SERVER')
database = 'App'
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
transactions_table_name = 'Transactions'
files_table_name = 'ImportedFiles'


def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        return conn
    except pyodbc.Error as ex:
        print("Database connection failed:", ex)
        return None

@app.route('/import', methods=['POST'])
def import_transactions():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    encoding = request.form.get('encoding', 'utf-8')

    directory = os.path.join(os.path.dirname(__file__), 'bank_statement_tool/data')
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file.filename)
    file.save(file_path)

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    import_statement(file_path, encoding, conn, transactions_table_name, files_table_name,filename=file.filename)
    conn.close()
    return jsonify({"message": f"Imported transactions from {file.filename} with encoding {encoding}"}), 200

@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {transactions_table_name}')
    transactions = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in transactions]
    cursor.close()
    conn.close()
    return jsonify(results), 200

@app.route('/transactions/uncategorized', methods=['GET'])
def get_uncategorized_transactions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute(f"SELECT TOP 10 * FROM {transactions_table_name} WHERE category = ''")
    transactions = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in transactions]
    cursor.close()
    conn.close()
    return jsonify(results), 200

@app.route('/transactions/categorize', methods=['POST'])
def categorize_transaction():
    data = request.json
    transaction_id = data.get('id')
    category = data.get('category')

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute(f"UPDATE {transactions_table_name} SET category = ? WHERE id = ?", category, transaction_id)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Transaction categorized successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)