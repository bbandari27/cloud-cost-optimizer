import os
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

PROCESSED_PATH = "data/processed/optimized_cost_data.csv"

def get_connection():
    required = [
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
    ]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise ValueError(f"Missing Snowflake environment variables: {', '.join(missing)}")

    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

def load_to_snowflake():
    if not os.path.exists(PROCESSED_PATH):
        raise FileNotFoundError(f"{PROCESSED_PATH} not found")

    df = pd.read_csv(PROCESSED_PATH)
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS CLOUD_COST_OPTIMIZATION (
                RESOURCE_ID STRING,
                RESOURCE_TYPE STRING,
                USAGE_HOURS FLOAT,
                COST FLOAT,
                STATUS STRING,
                REGION STRING,
                WASTE_COST FLOAT,
                RECOMMENDATION STRING
            )
        """)

        insert_sql = """
            INSERT INTO CLOUD_COST_OPTIMIZATION
            (RESOURCE_ID, RESOURCE_TYPE, USAGE_HOURS, COST, STATUS, REGION, WASTE_COST, RECOMMENDATION)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        for _, row in df.iterrows():
            cur.execute(insert_sql, (
                row["resource_id"],
                row["resource_type"],
                float(row["usage_hours"]),
                float(row["cost"]),
                row["status"],
                row["region"],
                float(row["waste_cost"]),
                row["recommendation"],
            ))

        conn.commit()
        print("Loaded data into Snowflake successfully")
        return len(df)

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    load_to_snowflake()
