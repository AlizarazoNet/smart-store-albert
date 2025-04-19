import os
import shutil
import sqlite3
import pandas as pd
print("🚀 Script is running...")


def main():
    print("🚀 Script is running...")

    # Dynamically get the base directory (one level up from OLAP folder)
    base_dir = os.path.dirname(os.path.dirname(__file__))  # go up from /OLAP
    source_db_path = os.path.join(base_dir, "data", "dw", "smart_sales.db")
    destination_folder = os.path.dirname(__file__)  # current folder: OLAP
    destination_db_path = os.path.join(destination_folder, "smart_sales.db")

    print("📁 Starting export...")

    if not os.path.exists(source_db_path):
        print(f"❌ Source DB not found: {source_db_path}")
        return

    shutil.copy(source_db_path, destination_db_path)
    print(f"✅ Copied to {destination_db_path}")
    
    ...

    # Test DB copy
    conn = sqlite3.connect(destination_db_path)
    query = "SELECT * FROM sale LIMIT 5"
    df = pd.read_sql_query(query, conn)
    print("✅ Sample data:")
    print(df)

if __name__ == "__main__":
    main()
