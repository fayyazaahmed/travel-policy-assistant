from app.db.policy_repository import PolicyRepository
from app.models.policy import Policy
from app.services.retrieval_service import RetrievalService


class PolicyService:
    """Provide application-level operations for travel policies."""

    def __init__(self, repository: PolicyRepository):
        self.repository = repository
        self.policies = repository.get_all_policies()
        self.retrieval_service = RetrievalService(self.policies)

    def get_all_policies(self) -> list[Policy]:
        """Return all available travel policies."""
        return self.policies

    def get_policy_value(self, query: str) -> str:
        """Return the allowance when the query identifies a supported policy."""

        detected_category = self.retrieval_service._detect_category(query)

        if detected_category is None:
            return "The travel expense policy does not cover this question."

        results = self.retrieval_service.search(query, top_k=2)

        if not results:
            return "The travel expense policy does not cover this question."

        if len(results) > 1:
            best_score = results[0][1]
            second_score = results[1][1]

            if best_score - second_score < 0.1:
                return (
                    "The question matches multiple travel policies. "
                    "Please provide more specific details."
                )

        policy, _ = results[0]

        return (
            f"${policy.daily_limit_usd:.0f} {policy.currency} "
            f"{policy.notes.lower()}."
        )