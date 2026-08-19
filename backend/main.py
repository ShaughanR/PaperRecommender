from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend import database
from backend.models import Paper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}

####paper stuff#####
@app.get("/api/papers", response_model=list[Paper])
def get_papers(limit: int = 20, cur=Depends(database.get_db)):
    return database.get_paper_multiple(cur, limit)


@app.get("/api/papers/search", response_model=list[Paper])
def search_papers(
    query: str | None = None,
    published_after: str | None = None,
    published_before: str | None = None,
    limit: int = 20,
    cur=Depends(database.get_db)
):
    return database.get_paper_queried_multiple(cur, query,  published_after, published_before, limit)

@app.get("/api/papers/{paper_id}", response_model=Paper)
def get_paper(paper_id: str, cur=Depends(database.get_db)):
    return database.get_paper_single(cur, paper_id)








