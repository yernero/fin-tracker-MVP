from flask import Flask, request, jsonify, render_template
import pandas as pd
from sqlalchemy import create_engine, inspect

app = Flask(__name__)
# Database setup
engine = create_engine('sqlite:///transactions.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'account' not in request.form:
        return jsonify({"message": "No file or account specified"}), 400
    file = request.files['file']
    account = request.form['account']
    if file and account:
        df = pd.read_csv(file)
        df['Account'] = account
        
        # Check if the Account column exists, and add it if it does not
        inspector = inspect(engine)
        columns = inspector.get_columns('transactions')
        column_names = [column['name'] for column in columns]
        if 'Account' not in column_names:
            with engine.connect() as conn:
                conn.execute('ALTER TABLE transactions ADD COLUMN Account VARCHAR')
        
        df.to_sql('transactions', engine, if_exists='append', index=False)
        return jsonify({"message": "File uploaded and data saved to database"}), 200
    return jsonify({"message": "No file uploaded or account not specified"}), 400

@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = pd.read_sql('SELECT DISTINCT Account FROM transactions', engine)
    return jsonify(accounts['Account'].tolist())

@app.route('/transactions/<account>', methods=['GET'])
def get_transactions(account):
    transactions = pd.read_sql(f'SELECT * FROM transactions WHERE Account = "{account}"', engine)
    return transactions.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
