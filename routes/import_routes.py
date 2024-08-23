from flask import Blueprint, request, jsonify
from tools.importer import import_statement
import os
from models.database import get_db_connection  # Import the database connection utility

bp = Blueprint('import_routes', __name__)

@bp.route('/import', methods=['POST'])
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

    import_statement(file_path, encoding, conn, 'Transactions', 'ImportedFiles', filename=file.filename)
    conn.close()
    return jsonify({"message": f"Imported transactions from {file.filename} with encoding {encoding}"}), 200