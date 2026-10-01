import pandas as pd
import numpy as np

np.random.seed(42)

# Customers
customers = pd.DataFrame({
    "customer_id": range(1, 1001),
    "customer_name": [
        f"Customer_{i}" for i in range(1, 1001)
    ],
    "gender": np.random.choice(
        ["Male", "Female", "Other"],
        1000
    ),
    "age": np.random.randint(18, 65, 1000),
    "city": np.random.choice(
        ["Delhi", "Mumbai", "Bangalore", "Kolkata",
         "Ranchi", "Patna", "Hyderabad"],
        1000
    ),
    "signup_date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2023-01-01", "2025-01-01"),
            1000
        )
    )
})

products = pd.DataFrame({
    "product_id": range(1, 101),
    "product_name": [
        f"Product_{i}" for i in range(1, 101)
    ],
    "category": np.random.choice(
        ["Electronics", "Clothing", "Books",
         "Home", "Sports"],
        100
    ),
    "price": np.round(
        np.random.uniform(100, 5000, 100),
        2
    )
})

n = 10000

transactions = pd.DataFrame({
    "transaction_id": range(1, n + 1),

    "customer_id": np.random.randint(
        1, 1001, n
    ),

    "product_id": np.random.randint(
        1, 101, n
    ),

    "transaction_date": pd.to_datetime(
        np.random.choice(
            pd.date_range(
                "2024-01-01",
                "2025-12-31"
            ),
            n
        )
    ),

    "quantity": np.random.randint(
        1, 5, n
    ),

    "payment_method": np.random.choice(
        ["UPI", "Credit Card", "Debit Card", "Cash"],
        n
    )
})

transactions = transactions.merge(
    products[["product_id", "price"]],
    on="product_id",
    how="left"
)

transactions["amount"] = (
    transactions["quantity"] * transactions["price"]
)

transactions.drop(
    columns=["price"],
    inplace=True
)

customers.to_csv("../data/customers.csv", index=False)
products.to_csv("../data/products.csv", index=False)
transactions.to_csv("../data/transactions.csv", index=False)

print("Data generated successfully!")