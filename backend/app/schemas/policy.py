from pydantic import BaseModel


class PolicyQueryRequest(BaseModel):
    question: str


class PolicyQueryResponse(BaseModel):
    answer: str