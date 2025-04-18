import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
db_path = "C:/Projects/smart-store-albert/data/dw/smart_sales.db"
conn = sqlite3.connect(db_path)

# Query: Total sales grouped by day of the week
query = """
SELECT 
    strftime('%w',SaleDate) AS day_of_week,
    COUNT(*) AS num_orders,
    SUM(SaleAmount) AS total_sales
FROM sale
GROUP BY day_of_week
ORDER BY day_of_week;
"""

# Load query results into a DataFrame
df = pd.read_sql_query(query, conn)

# Map weekday numbers to names (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
day_map = {
    "0": "Sunday", "1": "Monday", "2": "Tuesday",
    "3": "Wednesday", "4": "Thursday", "5": "Friday", "6": "Saturday"
}
df["day_name"] = df["day_of_week"].map(day_map)

# Sort by actual weekday order
df["day_of_week"] = df["day_of_week"].astype(int)
df = df.sort_values("day_of_week")

# Plot total sales by weekday
plt.figure(figsize=(10, 6))
plt.bar(df["day_name"], df["total_sales"], color="skyblue")
plt.title("Total Sales by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Optional: print the DataFrame for reference
print(df)
