from fastapi import APIRouter

from app.db.policy_repository import PolicyRepository
from app.schemas.policy import PolicyQueryRequest, PolicyQueryResponse
from app.services.policy_service import PolicyService


router = APIRouter(prefix="/api/policy", tags=["policy"])

policy_service = PolicyService(PolicyRepository())


@router.post("/query", response_model=PolicyQueryResponse)
def query_policy(request: PolicyQueryRequest) -> PolicyQueryResponse:
    """Answer a user's travel policy question."""
    answer = policy_service.get_policy_value(request.question)

    return PolicyQueryResponse(answer=answer)