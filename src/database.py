import pandas as pd
from sqlalchemy import create_engine

# Database connection
engine = create_engine(
    "mysql+mysqlconnector://root:apurboroy@localhost/customer_analysis?charset=utf8"
)

# Load CSV files
customers = pd.read_csv("../data/customers.csv")
products = pd.read_csv("../data/products.csv")
transactions = pd.read_csv("../data/transactions.csv")

# Convert dates
customers["signup_date"] = pd.to_datetime(
    customers["signup_date"]
)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

# Load data into MySQL
customers.to_sql(
    "customers",
    engine,
    if_exists="append",
    index=False
)

products.to_sql(
    "products",
    engine,
    if_exists="append",
    index=False
)

transactions.to_sql(
    "transactions",
    engine,
    if_exists="append",
    index=False
)

print("All data successfully loaded into MySQL!")