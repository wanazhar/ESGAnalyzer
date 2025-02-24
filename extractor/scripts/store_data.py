import json
import os
import sqlite3

DB_PATH = "database/esg_data.db"
INPUT_FOLDER = "classified_esg"

def create_table():
    """Creates an ESG classification table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS esg_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            subcategory TEXT,
            content TEXT,
            fiscal_year INTEGER
        )
    """)
    conn.commit()
    conn.close()

def store_data():
    """Stores classified ESG data into SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".json"):
            with open(os.path.join(INPUT_FOLDER, file), "r", encoding="utf-8") as f:
                data = json.load(f)

            for category, entries in data.items():
                for entry in entries:
                    cursor.execute("""
                        INSERT INTO esg_data (category, subcategory, content, fiscal_year)
                        VALUES (?, ?, ?, ?)
                    """, (category, entry["subcategory"], entry["sentence"], 2023))

    conn.commit()
    conn.close()
    print("ESG data stored successfully!")

# Run storage
create_table()
store_data()
