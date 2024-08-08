from flask import Flask, request, jsonify
from flask_cors import CORS
from bank_statement_tool.importer import import_statement
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

def get_data_path(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)

def load_transactions():
    data_path = get_data_path('transactions.json')
    with open(data_path, 'r') as f:
        return json.load(f)

def save_transactions(transactions):
    data_path = get_data_path('transactions.json')
    with open(data_path, 'w') as f:
        json.dump(transactions, f, indent=4)

def load_displayed_ids():
    path = get_data_path('displayed_ids.json')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def save_displayed_ids(displayed_ids):
    path = get_data_path('displayed_ids.json')
    with open(path, 'w') as f:
        json.dump(displayed_ids, f, indent=4)

@app.route('/import', methods=['POST'])
def import_transactions():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    encoding = request.form.get('encoding', 'utf-8')
    directory = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, file.filename)
    file.save(filename)
    import_statement(filename, encoding)
    return jsonify({"message": f"Imported transactions from {file.filename} with encoding {encoding}"}), 200

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = load_transactions()
    return jsonify(transactions), 200

@app.route('/transactions/uncategorized', methods=['GET'])
def get_uncategorized_transactions():
    transactions = load_transactions()
    displayed_ids = load_displayed_ids()
    
    today = datetime.today().strftime('%Y-%m-%d')
    
    if today not in displayed_ids:
        displayed_ids[today] = []
    
    uncategorized = [t for t in transactions if not t['category']]
    new_transactions = [t for t in uncategorized if t['id'] not in displayed_ids[today]]
    
    if len(displayed_ids[today]) < 10:
        to_display = new_transactions[:10 - len(displayed_ids[today])]
        displayed_ids[today].extend([t['id'] for t in to_display])
        save_displayed_ids(displayed_ids)
    else:
        to_display = []
    
    return jsonify(to_display), 200

@app.route('/transactions/categorize', methods=['POST'])
def categorize_transaction():
    transactions = load_transactions()
    transaction_id = request.json.get('id')
    category = request.json.get('category')
    
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transaction['category'] = category
            break
    
    save_transactions(transactions)
    
    return jsonify({"message": "Transaction categorized successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
