import arxiv
import logging
from models import Paper

logging.basicConfig(level=logging.DEBUG)

def get_base_arxiv_id(entry_id):
    arxiv_id = entry_id.rstrip("/").split("/")[-1]
    return arxiv_id.rsplit("v", 1)[0]


def paper_transformer(result) -> Paper:
    return Paper(
        arxiv_id=get_base_arxiv_id(result.entry_id),
        title=result.title,
        authors=[author.name for author in result.authors],
        abstract=result.summary,
        published_at=result.published,
        updated_at=result.updated,
        doi=result.doi,
        categories=result.categories,
        pdf_url=result.pdf_url
    )

def search_papers(query: str, max_results: int):
    client = arxiv.Client(
        page_size=10,
        delay_seconds=5,
        num_retries=3
    )

    search = arxiv.Search(
        query= query,
        max_results = max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    for result in client.results(search):
        yield paper_transformer(result)
