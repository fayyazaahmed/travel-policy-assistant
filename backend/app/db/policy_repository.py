from app.db.database import get_connection
from app.models.policy import Policy


class PolicyRepository:
    """Handle database operations for travel policies."""

    def add_policy(self, policy: Policy) -> None:
        """Insert a policy if an identical policy does not already exist."""
        connection = get_connection()

        existing_policy = connection.execute(
            """
            SELECT id
            FROM policies
            WHERE category = ?
            AND region = ?
            AND daily_limit_usd = ?
            AND currency = ?
            """,
            (
                (
                policy.category,
                policy.region,
                policy.daily_limit_usd,
                policy.currency,
)
            ),
        ).fetchone()

        if existing_policy is None:
            connection.execute(
                """
                INSERT INTO policies (
                    category,
                    region,
                    daily_limit_usd,
                    currency,
                    notes
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    policy.category,
                    policy.region,
                    policy.daily_limit_usd,
                    policy.currency,
                    policy.notes,
                ),
            )

            connection.commit()

        connection.close()

    def get_all_policies(self) -> list[Policy]:
        """Return all policies stored in the database."""
        connection = get_connection()

        rows = connection.execute(
            """
            SELECT
                id,
                category,
                region,
                daily_limit_usd,
                currency,
                notes
            FROM policies
            """
        ).fetchall()

        connection.close()

        return [
            Policy(
                id=row["id"],
                category=row["category"],
                region=row["region"],
                daily_limit_usd=row["daily_limit_usd"],
                currency=row["currency"],
                notes=row["notes"],
            )
            for row in rows
        ]