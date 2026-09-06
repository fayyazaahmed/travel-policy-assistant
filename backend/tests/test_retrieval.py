from app.models.policy import Policy
from app.services.retrieval_service import RetrievalService


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


def test_category_alias_is_detected():
    service = RetrievalService(create_policies())

    assert service._detect_category("What is the meal allowance?") == "Meals"


def test_region_alias_is_detected():
    service = RetrievalService(create_policies())

    assert service._detect_region("What is the hotel allowance in UK?") == "United Kingdom"


def test_category_and_region_filtering():
    service = RetrievalService(create_policies())

    results = service.search(
        "What is the hotel allowance in India?",
        top_k=3,
    )

    assert len(results) == 1
    assert results[0][0].category == "Hotel"
    assert results[0][0].region == "India"
    assert results[0][0].daily_limit_usd == 120


def test_global_policy_is_considered_for_specific_region():
    service = RetrievalService(create_policies())

    results = service.search(
        "How much can I spend on incidentals in India?",
        top_k=3,
    )

    assert len(results) == 1
    assert results[0][0].category == "Incidentals"
    assert results[0][0].region == "Global"


def test_airfare_query_returns_both_airfare_policies():
    service = RetrievalService(create_policies())

    results = service.search(
        "What is the airfare allowance?",
        top_k=3,
    )

    assert len(results) == 2
    assert all(policy.category == "Airfare" for policy, _ in results)


def test_specific_airfare_query_ranks_correct_policy_first():
    service = RetrievalService(create_policies())

    results = service.search(
        "What is the airfare allowance for an economy flight under 6 hours?",
        top_k=2,
    )

    assert results[0][0].daily_limit_usd == 90