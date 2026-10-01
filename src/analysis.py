import pandas as pd
import matplotlib

# Use a non-GUI backend so charts can be saved
# without requiring Tkinter.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import os


# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

engine = create_engine(
    "mysql+mysqlconnector://root:apurboroy@localhost/customer_analysis?charset=utf8"
)


# ============================================================
# 2. CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs("../output", exist_ok=True)


# ============================================================
# 3. BASIC BUSINESS KPIs
# ============================================================

kpi_query = """
SELECT
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue,
    AVG(amount) AS average_transaction_value,
    COUNT(DISTINCT customer_id) AS active_customers
FROM transactions;
"""

kpis = pd.read_sql(kpi_query, engine)

print("\n========== BUSINESS KPIs ==========")
print(kpis.to_string(index=False))


# ============================================================
# 4. MONTHLY REVENUE ANALYSIS
# ============================================================

monthly_query = """
SELECT
    YEAR(transaction_date) AS year,
    MONTH(transaction_date) AS month,
    SUM(amount) AS revenue,
    COUNT(transaction_id) AS transactions
FROM transactions
GROUP BY
    YEAR(transaction_date),
    MONTH(transaction_date)
ORDER BY
    year,
    month;
"""

monthly = pd.read_sql(monthly_query, engine)

monthly["date"] = pd.to_datetime(
    monthly["year"].astype(str)
    + "-"
    + monthly["month"].astype(str)
    + "-01"
)

print("\n========== MONTHLY REVENUE ==========")
print(monthly.to_string(index=False))

monthly.to_csv(
    "../output/monthly_revenue.csv",
    index=False
)


# ============================================================
# 5. TOP CUSTOMERS
# ============================================================

customer_query = """
SELECT
    c.customer_id,
    c.customer_name,
    c.gender,
    c.age,
    c.city,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_spending,
    AVG(t.amount) AS average_transaction_value,
    MIN(t.transaction_date) AS first_purchase,
    MAX(t.transaction_date) AS last_purchase
FROM customers c
LEFT JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.gender,
    c.age,
    c.city
ORDER BY
    total_spending DESC;
"""

customers = pd.read_sql(customer_query, engine)

print("\n========== TOP 10 CUSTOMERS ==========")
print(
    customers.head(10).to_string(index=False)
)

customers.to_csv(
    "../output/customer_summary.csv",
    index=False
)


# ============================================================
# 6. CATEGORY ANALYSIS
# ============================================================

category_query = """
SELECT
    p.category,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.quantity) AS units_sold,
    SUM(t.amount) AS total_revenue,
    AVG(t.amount) AS average_transaction_value
FROM transactions t
JOIN products p
    ON t.product_id = p.product_id
GROUP BY
    p.category
ORDER BY
    total_revenue DESC;
"""

category = pd.read_sql(category_query, engine)

print("\n========== CATEGORY ANALYSIS ==========")
print(category.to_string(index=False))

category.to_csv(
    "../output/category_analysis.csv",
    index=False
)


# ============================================================
# 7. PAYMENT METHOD ANALYSIS
# ============================================================

payment_query = """
SELECT
    payment_method,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue,
    AVG(amount) AS average_transaction_value
FROM transactions
GROUP BY
    payment_method
ORDER BY
    total_revenue DESC;
"""

payment = pd.read_sql(payment_query, engine)

print("\n========== PAYMENT METHOD ANALYSIS ==========")
print(payment.to_string(index=False))

payment.to_csv(
    "../output/payment_analysis.csv",
    index=False
)


# ============================================================
# 8. CITY ANALYSIS
# ============================================================

city_query = """
SELECT
    c.city,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_revenue,
    AVG(t.amount) AS average_transaction_value
FROM customers c
JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY
    c.city
ORDER BY
    total_revenue DESC;
"""

city = pd.read_sql(city_query, engine)

print("\n========== CITY ANALYSIS ==========")
print(city.to_string(index=False))

city.to_csv(
    "../output/city_analysis.csv",
    index=False
)


# ============================================================
# 9. RFM ANALYSIS
# ============================================================

rfm_query = """
SELECT
    customer_id,
    MAX(transaction_date) AS last_purchase,
    COUNT(transaction_id) AS frequency,
    SUM(amount) AS monetary
FROM transactions
GROUP BY customer_id;
"""

rfm = pd.read_sql(rfm_query, engine)

rfm["last_purchase"] = pd.to_datetime(
    rfm["last_purchase"]
)


# Use the latest transaction date in our dataset
# as the reference date.

reference_date = rfm["last_purchase"].max() + pd.Timedelta(days=1)

rfm["recency"] = (
    reference_date - rfm["last_purchase"]
).dt.days


# ============================================================
# 10. RFM SCORING
# ============================================================

# Recency:
# Lower number of days = better customer

rfm["R_score"] = pd.qcut(
    rfm["recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
)


# Frequency:
# Higher purchase frequency = better

rfm["F_score"] = pd.qcut(
    rfm["frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
)


# Monetary:
# Higher spending = better

rfm["M_score"] = pd.qcut(
    rfm["monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
)


rfm["R_score"] = rfm["R_score"].astype(int)
rfm["F_score"] = rfm["F_score"].astype(int)
rfm["M_score"] = rfm["M_score"].astype(int)


rfm["RFM_score"] = (
    rfm["R_score"]
    + rfm["F_score"]
    + rfm["M_score"]
)


# ============================================================
# 11. CUSTOMER SEGMENTATION
# ============================================================

def assign_segment(score):

    if score >= 13:
        return "High Value"

    elif score >= 10:
        return "Loyal"

    elif score >= 7:
        return "Potential"

    else:
        return "At Risk"


rfm["segment"] = rfm["RFM_score"].apply(
    assign_segment
)


print("\n========== CUSTOMER SEGMENTS ==========")
print(
    rfm["segment"]
    .value_counts()
    .to_string()
)


rfm.to_csv(
    "../output/customer_segments.csv",
    index=False
)


# ============================================================
# 12. VISUALIZATION 1: MONTHLY REVENUE
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    monthly["date"],
    monthly["revenue"],
    marker="o"
)

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "../output/monthly_revenue.png"
)

plt.close()


# ============================================================
# 13. VISUALIZATION 2: REVENUE BY CATEGORY
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    category["category"],
    category["total_revenue"]
)

plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "../output/category_revenue.png"
)

plt.close()


# ============================================================
# 14. VISUALIZATION 3: CUSTOMER SEGMENTS
# ============================================================

segment_counts = (
    rfm["segment"]
    .value_counts()
)

plt.figure(figsize=(8, 5))

plt.bar(
    segment_counts.index,
    segment_counts.values
)

plt.title("Customer Segmentation")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "../output/customer_segments.png"
)

plt.close()


# ============================================================
# 15. VISUALIZATION 4: PAYMENT METHODS
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    payment["payment_method"],
    payment["total_revenue"]
)

plt.title("Revenue by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Revenue")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "../output/payment_revenue.png"
)

plt.close()


# ============================================================
# 16. FINAL EXCEL REPORT
# ============================================================

with pd.ExcelWriter(
    "../output/customer_analysis_report.xlsx"
) as writer:

    kpis.to_excel(
        writer,
        sheet_name="KPIs",
        index=False
    )

    monthly.to_excel(
        writer,
        sheet_name="Monthly Revenue",
        index=False
    )

    customers.to_excel(
        writer,
        sheet_name="Customers",
        index=False
    )

    category.to_excel(
        writer,
        sheet_name="Categories",
        index=False
    )

    payment.to_excel(
        writer,
        sheet_name="Payments",
        index=False
    )

    city.to_excel(
        writer,
        sheet_name="Cities",
        index=False
    )

    rfm.to_excel(
        writer,
        sheet_name="RFM Analysis",
        index=False
    )


# ============================================================
# 17. FINISHED
# ============================================================

print("\n========================================")
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("========================================")

print("\nGenerated files:")

print(" - output/monthly_revenue.csv")
print(" - output/customer_summary.csv")
print(" - output/category_analysis.csv")
print(" - output/payment_analysis.csv")
print(" - output/city_analysis.csv")
print(" - output/customer_segments.csv")
print(" - output/customer_analysis_report.xlsx")

print("\nGenerated charts:")

print(" - output/monthly_revenue.png")
print(" - output/category_revenue.png")
print(" - output/customer_segments.png")
print(" - output/payment_revenue.png")