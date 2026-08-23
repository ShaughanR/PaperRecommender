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

class PaperSearchResponse(BaseModel):
    papers: list[Paper]
    next_arxiv_start: int


class CreateUserRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class UserInteraction(BaseModel):
    paper_id: str
    interaction_type: str

class UserCategory(BaseModel):
    category_id: int