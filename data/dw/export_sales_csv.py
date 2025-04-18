import sqlite3
import pandas as pd

# Connect to the data warehouse
conn = sqlite3.connect("data/dw/smart_sales.db")

# Run a SQL query to get sales data
query = """
SELECT * FROM sale
"""
df = pd.read_sql_query(query, conn)

# Make sure the output folder exists
import os
os.makedirs("data/prepared", exist_ok=True)

# Save as CSV
df.to_csv("data/prepared/sales.csv", index=False)

print("✅ sales.csv exported to data/prepared/")
