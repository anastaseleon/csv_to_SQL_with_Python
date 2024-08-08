import pandas as pd
import json
import os

def load_bank_statement(filename, encoding='utf-8'):
    df = pd.read_csv(filename, encoding=encoding)
    transactions = df.to_dict(orient='records')
    for idx, transaction in enumerate(transactions):
        transaction['id'] = idx
        transaction['category'] = ''
    return transactions

def save_transactions(transactions, filename):
    data_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(data_path, 'w') as f:
        json.dump(transactions, f, indent=4)

def import_statement(filename, encoding='utf-8'):
    transactions = load_bank_statement(filename, encoding)
    save_transactions(transactions, 'transactions.json')
    uncategorized = [t for t in transactions if t['category'] == '']
    save_transactions(uncategorized, 'uncategorized.json')
