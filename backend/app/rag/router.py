"""Lightweight RAG entrypoints embedded in the FastAPI backend."""
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth.auth import fastapi_users

router = APIRouter(prefix="/rag", tags=["rag"])
get_current_user = fastapi_users.current_user()


class RagQuery(BaseModel):
    query: str
    top_k: int = 5


class RagResult(BaseModel):
    query: str
    answers: List[str]


@router.post("/query", response_model=RagResult)
async def run_rag_query(
    payload: RagQuery,
    user=Depends(get_current_user),
):
    _ = user  # Reserved for future personalization
    # Placeholder implementation to keep the surface area stable.
    answers = [
        f"Stubbed answer for '{payload.query}' (result {idx + 1})"
        for idx in range(payload.top_k)
    ]
    return RagResult(query=payload.query, answers=answers)
