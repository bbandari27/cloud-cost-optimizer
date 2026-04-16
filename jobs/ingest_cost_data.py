import os
import pandas as pd

RAW_PATH = "data/raw/cost_data.csv"

def ingest_cost_data():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"{RAW_PATH} not found")

    df = pd.read_csv(RAW_PATH)
    print(f"Ingested rows: {len(df)}")
    print(df.head())
    return df.to_dict(orient="records")

if __name__ == "__main__":
    ingest_cost_data()
