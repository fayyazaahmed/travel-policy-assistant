from sklearn.feature_extraction.text import TfidfVectorizer

from app.models.policy import Policy


CATEGORY_ALIASES = {
    "meal": "Meals",
    "meals": "Meals",
    "food": "Meals",
    "dining": "Meals",
    "hotel": "Hotel",
    "accommodation": "Hotel",
    "lodging": "Hotel",
    "taxi": "Taxi",
    "cab": "Taxi",
    "airfare": "Airfare",
    "flight": "Airfare",
    "flights": "Airfare",
    "incidentals": "Incidentals",
}

REGION_ALIASES = {
    "uk": "United Kingdom",
    "britain": "United Kingdom",
    "england": "United Kingdom",
    "us": "United States",
    "usa": "United States",
    "america": "United States",
    "uae": "United Arab Emirates",
    "emirates": "United Arab Emirates",
    "india": "India",
}

class RetrievalService:
    """Retrieve policies based on the user's question."""

    def __init__(self, policies: list[Policy]):
        self.policies = policies

        self.policy_texts = [
            f"{policy.category} {policy.region} "
            f"{policy.daily_limit_usd} {policy.currency} "
            f"{policy.notes}"
            for policy in policies
        ]

        self.vectorizer = TfidfVectorizer()
        self.policy_vectors = self.vectorizer.fit_transform(self.policy_texts)

    def _detect_category(self, query: str) -> str | None:
        """Detect a known expense category from the user's question."""
        words = query.lower().split()

        for word in words:
            normalized_word = word.strip(".,?!")
            if normalized_word in CATEGORY_ALIASES:
                return CATEGORY_ALIASES[normalized_word]

        return None

    def search(self, query: str, top_k: int = 3) -> list[tuple[Policy, float]]:
        """Return the most relevant applicable policies."""

        query_vector = self.vectorizer.transform([query])

        similarities = (
            self.policy_vectors @ query_vector.T
        ).toarray().flatten()

        detected_category = self._detect_category(query)
        detected_region = self._detect_region(query)

        candidates = self.policies

        # If the user specifies a category, restrict results to that category.
        if detected_category:
            candidates = [
                policy
                for policy in candidates
                if policy.category == detected_category
            ]

        # If the user specifies a region, keep policies for that region
        # and policies that apply globally.
        if detected_region:
            candidates = [
                policy
                for policy in candidates
                if policy.region in (detected_region, "Global")
            ]

        candidate_indices = [
            self.policies.index(policy)
            for policy in candidates
        ]

        ranked_indices = sorted(
            candidate_indices,
            key=lambda index: similarities[index],
            reverse=True,
        )[:top_k]

        return [
            (self.policies[index], float(similarities[index]))
            for index in ranked_indices
        ]

    def _detect_region(self, query: str) -> str | None:
        """Detect a known region from the user's question."""
        words = query.lower().split()

        for word in words:
            normalized_word = word.strip(".,?!")
            if normalized_word in REGION_ALIASES:
                return REGION_ALIASES[normalized_word]

        return None