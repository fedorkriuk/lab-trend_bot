from pydantic import BaseModel, Field
from typing import List

class PostDraftModel(BaseModel):
    platform: str = Field(pattern="^(twitter|linkedin)$")
    text: str = Field(min_length=5, max_length=1300)
    links: List[str] = Field(default_factory=list)