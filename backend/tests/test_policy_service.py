from app.models.policy import Policy
from app.services.policy_service import PolicyService


class FakeRepository:
    def __init__(self, policies: list[Policy]):
        self.policies = policies

    def get_all_policies(self) -> list[Policy]:
        return self.policies


def create_policies() -> list[Policy]:
    return [
        Policy(
            id=1,
            category="Meals",
            region="United Kingdom",
            daily_limit_usd=75,
            currency="USD",
            notes="Per day; includes tips",
        ),
        Policy(
            id=2,
            category="Hotel",
            region="India",
            daily_limit_usd=120,
            currency="USD",
            notes="Per night",
        ),
        Policy(
            id=3,
            category="Incidentals",
            region="Global",
            daily_limit_usd=25,
            currency="USD",
            notes="Per day; no receipt required",
        ),
        Policy(
            id=4,
            category="Airfare",
            region="Global",
            daily_limit_usd=90,
            currency="USD",
            notes="Economy only for flights under 6 hours",
        ),
        Policy(
            id=5,
            category="Airfare",
            region="Global",
            daily_limit_usd=70,
            currency="USD",
            notes="Business class permitted for flights over 6 hours",
        ),
    ]


def create_service() -> PolicyService:
    return PolicyService(FakeRepository(create_policies()))


def test_hotel_question_returns_correct_allowance():
    service = create_service()

    answer = service.get_policy_value(
        "What is the hotel allowance in India?"
    )

    assert answer == "$120 USD per night."


def test_meal_question_returns_correct_allowance():
    service = create_service()

    answer = service.get_policy_value(
        "What is the meal allowance in the UK?"
    )

    assert answer == "$75 USD per day; includes tips."


def test_incidental_question_returns_correct_allowance():
    service = create_service()

    answer = service.get_policy_value(
        "How much can I spend on incidentals?"
    )

    assert answer == "$25 USD per day; no receipt required."


def test_generic_airfare_question_is_ambiguous():
    service = create_service()

    answer = service.get_policy_value(
        "What is the airfare allowance?"
    )

    assert answer == (
        "The question matches multiple travel policies. "
        "Please provide more specific details."
    )


def test_specific_airfare_question_returns_correct_policy():
    service = create_service()

    answer = service.get_policy_value(
        "What is the airfare allowance for an economy flight under 6 hours?"
    )

    assert answer == "$90 USD economy only for flights under 6 hours."


def test_unsupported_question_is_rejected():
    service = create_service()

    answer = service.get_policy_value(
        "What is the company policy for maternity leave?"
    )

    assert answer == (
        "The travel expense policy does not cover this question."
    )