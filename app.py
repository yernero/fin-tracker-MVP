from flask import Flask, request, jsonify, render_template
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, Integer

app = Flask(__name__)
# Database setup
engine = create_engine('sqlite:///transactions.db')
metadata = MetaData()

# Define the transactions table schema
transactions = Table(
    'transactions', metadata,
    Column('Booking Date', String),
    Column('Amount', Float),
    Column('Credit Debit Indicator', String),
    Column('Type', String),
    Column('Type Group', String),
    Column('Reference', String),
    Column('Instructed Currency', String),
    Column('Currency Exchange Rate', Float),
    Column('Instructed Amount', Float),
    Column('Description', String),
    Column('Category', String),
    Column('Check Serial Number', String),
    Column('Card Ending', String),
    Column('Account', String)
)

# Create the table if it does not exist
metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    account = request.form.get('account')
    if file and account:
        df = pd.read_csv(file)
        df['Account'] = account
        
        # Print column names and first few rows for debugging
        print(df.columns)
        print(df.head())

        df.to_sql('transactions', engine, if_exists='append', index=False)
        return jsonify({"message": "File uploaded and data saved to database"}), 200
    return jsonify({"message": "No file uploaded or account not specified"}), 400

@app.route('/debug')
def debug():
    df = pd.read_sql('transactions', engine)
    return df.head().to_html()

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
