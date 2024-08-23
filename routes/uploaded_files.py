from flask import Blueprint, jsonify, request
from models.database import get_db_connection  # Import the database connection utility


bp = Blueprint('uploaded_files', __name__)

@bp.route('/uploaded_files', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM all_files')
    transactions = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in transactions]
    cursor.close()
    conn.close()
    return jsonify(results), 200