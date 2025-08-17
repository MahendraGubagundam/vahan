import pandas as pd
import sqlite3

def build_database(csv_file="data/vahan-manufacturer-vehicle-category.csv", db_file="vahan.db"):
    # Load CSV
    df = pd.read_csv(csv_file)

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Ensure date is parsed
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Ensure required columns exist
    required_cols = ["maker_company", "vehicle_type_simplified", "registrations", "state_name"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"CSV must have '{col}' column.")

    # Normalize categories (2W, 3W, 4W, Others)
    df["vehicle_type_simplified"] = df["vehicle_type_simplified"].str.upper().replace({
        "TWO WHEELER": "2W",
        "THREE WHEELER": "3W",
        "FOUR WHEELER": "4W",
        "LIGHT MOTOR VEHICLE": "4W",
        "LIGHT GOODS VEHICLE": "4W",
        "OTHER": "OTHERS"
    })

    # Connect to SQLite DB
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Drop table if exists
    cur.execute("DROP TABLE IF EXISTS vahan_data")

    # Create table including state
    cur.execute("""
        CREATE TABLE vahan_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            state_name TEXT,
            manufacturer TEXT,
            vehicle_category TEXT,
            registrations INTEGER
        )
    """)

    # Rename columns to match DB
    df.rename(columns={
        "maker_company": "manufacturer",
        "vehicle_type_simplified": "vehicle_category"
    }, inplace=True)

    # Insert data
    df_to_insert = df[["date", "state_name", "manufacturer", "vehicle_category", "registrations"]]
    df_to_insert.to_sql("vahan_data", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()
    print(f"✅ Database built successfully: {db_file}")


if __name__ == "__main__":
    build_database()
