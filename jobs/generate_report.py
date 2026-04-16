import os
import pandas as pd

PROCESSED_PATH = "data/processed/optimized_cost_data.csv"
REPORT_PATH = "data/reports/final_report.txt"

def generate_report():
    if not os.path.exists(PROCESSED_PATH):
        raise FileNotFoundError(f"{PROCESSED_PATH} not found")

    df = pd.read_csv(PROCESSED_PATH)

    total_cost = df["cost"].sum()
    waste_cost = df["waste_cost"].sum()
    optimization_count = int((df["waste_cost"] > 0).sum())

    lines = [
        "CLOUD COST OPTIMIZATION REPORT",
        "================================",
        f"Total Monthly Cost: ${total_cost:.2f}",
        f"Potential Savings: ${waste_cost:.2f}",
        f"Resources Needing Action: {optimization_count}",
        "",
        "Recommendations:"
    ]

    action_rows = df[df["waste_cost"] > 0]
    if action_rows.empty:
        lines.append("- No optimization opportunities found")
    else:
        for _, row in action_rows.iterrows():
            lines.append(
                f"- {row['resource_id']} ({row['resource_type']}, {row['region']}): "
                f"save ${row['waste_cost']:.2f} | {row['recommendation']}"
            )

    os.makedirs("data/reports", exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Report created: {REPORT_PATH}")
    return REPORT_PATH

if __name__ == "__main__":
    generate_report()
