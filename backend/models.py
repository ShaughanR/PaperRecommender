from pydantic import BaseModel
from datetime import datetime


class Paper(BaseModel):
    arxiv_id: str
    title: str
    authors: list[str]
    abstract: str
    published_at: datetime
    updated_at: datetime
    doi: str | None
    categories: list[str]
    pdf_url: str | None