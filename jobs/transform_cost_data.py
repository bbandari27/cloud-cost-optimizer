import os
import pandas as pd

RAW_PATH = "data/raw/cost_data.csv"
PROCESSED_PATH = "data/processed/optimized_cost_data.csv"

def transform_cost_data():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"{RAW_PATH} not found")

    df = pd.read_csv(RAW_PATH)

    df["waste_cost"] = df.apply(
        lambda row: row["cost"] if row["status"] in ["idle", "unused"] or row["usage_hours"] < 24 else 0,
        axis=1
    )

    df["recommendation"] = df.apply(
        lambda row: (
            f"Consider rightsizing or deleting {row['resource_id']}"
            if row["waste_cost"] > 0 else "No action needed"
        ),
        axis=1
    )

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"Processed file created: {PROCESSED_PATH}")
    return PROCESSED_PATH

if __name__ == "__main__":
    transform_cost_data()
