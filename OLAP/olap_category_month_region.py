import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'smart_sales.db'))
conn = sqlite3.connect(db_path)

# Database path
DB_PATH = "smart_sales.db"

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# SQL Query: Join sales, product, customer, extract month
query = """
SELECT 
    p.category AS category,
    c.Region AS region,
    strftime('%m', s.SaleDate) AS month,
    SUM(s.SaleAmount) AS total_sales
FROM sale s
JOIN product p ON s.ProductID = p.productid
JOIN customer c ON s.CustomerID = c.CustomerID
GROUP BY p.category, c.Region, strftime('%m', s.SaleDate)
ORDER BY total_sales DESC;
"""

# Run query
df = pd.read_sql_query(query, conn)
conn.close()

# Print result table
print("\nGrouped OLAP Result:")
print(df.head())

# 📊 Create bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x="category", y="total_sales", hue="region")
plt.title("Total Sales by Product Category and Region")
plt.xlabel("Product Category")
plt.ylabel("Total Sales")
plt.legend(title="Region", loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot to a file in OLAP/images/
output_path = "images/total_sales_by_product_category_and_region"
plt.savefig(output_path)

# Optional: still show it
plt.show()

