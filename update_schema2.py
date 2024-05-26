from sqlalchemy import create_engine, MetaData, Table, Column, String, Float

engine = create_engine('sqlite:///transactions.db')
metadata = MetaData()

# Drop the existing table using a connection
with engine.connect() as connection:
    connection.execute('DROP TABLE IF EXISTS transactions')

# Define the new schema
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

# Create the table
metadata.create_all(engine)
