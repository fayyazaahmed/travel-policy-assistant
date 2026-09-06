import csv
from pathlib import Path

from app.db.database import initialize_database
from app.db.policy_repository import PolicyRepository
from app.models.policy import Policy


BASE_DIR = Path(__file__).resolve().parents[3]
CSV_PATH = BASE_DIR / "data" / "travel_expense_policy.csv"


def load_policies_from_csv() -> None:
    """Load policies from the source CSV into the SQLite database."""
    initialize_database()

    repository = PolicyRepository()

    with CSV_PATH.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            policy = Policy(
                id=0,
                category=row["category"].strip(),
                region=row["region"].strip(),
                daily_limit_usd=float(row["daily_limit_usd"]),
                currency=row["currency"].strip(),
                notes=row["notes"].strip(),
            )

            repository.add_policy(policy)