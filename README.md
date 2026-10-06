# Customer Transaction Analysis

An end-to-end customer analytics project using **Python, Pandas, SQL, and MySQL** to analyze transaction data, identify customer behavior patterns, and generate business insights.

## Features

* Customer and transaction data management using MySQL
* SQL-based revenue, customer, product, category, city, and payment analysis
* Data cleaning and analysis using Pandas
* RFM-based customer segmentation
* Revenue and customer trend visualizations
* Automated CSV and Excel reports

## Tech Stack

* **Python**
* **Pandas & NumPy**
* **MySQL & SQL**
* **Matplotlib**
* **SQLAlchemy**
* **OpenPyXL**

## Project Pipeline

```text
CSV Data
   ↓
Python / Pandas
   ↓
MySQL Database
   ↓
SQL Analysis
   ↓
Pandas & RFM Analysis
   ↓
Visualizations & Reports
```

## Key Metrics

The current dataset contains:

* **1,000 customers**
* **10,000 transactions**
* **₹69.23M total transaction value**
* **₹6,923 average transaction value**

## Project Structure

```text
customer-transaction-analysis/
├── data/
├── sql/
├── src/
│   ├── generate_data.py
│   ├── database.py
│   └── analysis.py
├── output/
└── README.md
```

## How to Run

### If you wish to generate data, do this:
```bash
pip install -r requirements.txt
python src/generate_data.py
python src/database.py
python src/analysis.py
```

### If you have pre-requisite data, do this: 
(Move the data to data/ folder first)
```bash
pip install -r requirements.txt
python src/database.py
python src/analysis.py
```

Generated reports and visualizations are saved in the `output/` directory.

## Future Improvements

* Interactive Power BI dashboard
* Customer retention analysis
* Predictive customer churn modelling
* Automated analytics reporting
