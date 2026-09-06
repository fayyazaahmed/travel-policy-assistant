from dataclasses import dataclass


@dataclass(frozen=True)
class Policy:
    id: int
    category: str
    region: str
    daily_limit_usd: float
    currency: str
    notes: str