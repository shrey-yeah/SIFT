from typing import Literal
from pydantic import BaseModel


class Citation(BaseModel):
    document: str
    page: str
    quote: str
    chunk_id: str


class Answer(BaseModel):
    answer: str
    confidence: Literal["high", "medium", "low"]
    citations: list[Citation]
    caveats: list[str]
    abstained: bool
