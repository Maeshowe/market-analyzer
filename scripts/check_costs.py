import pandas as pd
from pathlib import Path
from datetime import datetime

log_file = Path(__file__).parent.parent / "data" / "cost_log.csv"

def check_costs(warning_threshold=10.0):  # napi figyelmeztetési küszöb (USD)
    if not log_file.exists():
        print("Nincs költségadat még logolva.")
        return

    df = pd.read_csv(log_file, header=None, names=["date", "model", "input_tokens", "output_tokens", "cost"])
    df["date"] = pd.to_datetime(df["date"])
    df["cost"] = df["cost"].astype(float)

    today = datetime.now().date()
    todays_cost = df[df["date"].dt.date == today]["cost"].sum()

    print(f"📅 {today} eddigi költsége: ${todays_cost:.4f}")

    if todays_cost >= warning_threshold:
        print(f"⚠️ Figyelem: A mai költségek (${todays_cost:.2f}) meghaladták a figyelmeztetési küszöböt (${warning_threshold:.2f})!")

if __name__ == "__main__":
    check_costs()