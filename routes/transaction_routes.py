from flask import Blueprint, jsonify, request
from models.database import get_db_connection  # Import the database connection utility
from datetime import datetime  


bp = Blueprint('transaction_routes', __name__)

@bp.route('/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Transactions')
    transactions = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in transactions]
    cursor.close()
    conn.close()
    return jsonify(results), 200

@bp.route('/transactions/uncategorized', methods=['GET'])
def get_uncategorized_transactions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT TOP 10 * FROM Transactions WHERE category = ''")
    transactions = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in transactions]
    cursor.close()
    conn.close()
    return jsonify(results), 200


@bp.route('/transactions/categorize', methods=['POST'])
def categorize_transaction():
    try:
        data = request.json
        transaction_id = data.get('id')
        category = data.get('category')

        if not transaction_id or not category:
            return jsonify({"error": "Missing transaction ID or category"}), 400

        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        date_categorized = datetime.now()  # Use datetime.now() correctly

        cursor.execute("UPDATE Transactions SET category = ?, date_categorized = ? WHERE id = ?",
                       (category, date_categorized, transaction_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Transaction categorized successfully"}), 200

    except Exception as e:
        print(f"Error occurred: {e}")  # Log the error to the console
        return jsonify({"error": "An error occurred"}), 500
