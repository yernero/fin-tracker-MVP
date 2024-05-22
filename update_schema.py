from sqlalchemy import create_engine, MetaData, Table, Column, String, text

engine = create_engine('sqlite:///transactions.db')
metadata = MetaData()

# Reflect the existing transactions table
transactions = Table('transactions', metadata, autoload_with=engine)

# Check if the Account column exists, and add it if it does not
if not hasattr(transactions.c, 'Account'):
    with engine.connect() as conn:
        conn.execute(text('ALTER TABLE transactions ADD COLUMN Account VARCHAR'))
