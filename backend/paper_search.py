from datetime import datetime, timezone

from backend import database
from backend import arxiv_connector

from backend.recommender import recommend_by_tfidf


POSTGRES_CANDIDATE_MULTIPLIER = 5
ARXIV_BATCH_SIZE = 50
MAX_PAGE_SIZE = 50


def search_papers(
    cur,
    query=None,
    published_after=None,
    published_before=None,
    page_size=20,
    excluded_paper_ids=None,
    arxiv_start=0
):

    # ---------------------------------------------------------
    # Safety limit
    # ---------------------------------------------------------

    page_size = min(
        page_size,
        MAX_PAGE_SIZE
    )

    # ---------------------------------------------------------
    # Normalize excluded IDs
    # ---------------------------------------------------------

    if excluded_paper_ids is None:
        excluded_paper_ids = []
    else:
        excluded_paper_ids = list(
            excluded_paper_ids
        )

    excluded_paper_ids_set = set(
        excluded_paper_ids
    )

    # ---------------------------------------------------------
    # Step 1
    # Retrieve PostgreSQL candidates
    # ---------------------------------------------------------

    postgres_candidate_limit = max(
        page_size * POSTGRES_CANDIDATE_MULTIPLIER,
        100
    )

    database_papers = database.get_paper_queried_multiple(
        cur=cur,
        query=query,
        published_after=published_after,
        published_before=published_before,
        limit=postgres_candidate_limit,
        excluded_paper_ids=excluded_paper_ids
    )

    # ---------------------------------------------------------
    # Step 2
    # Remove anything already displayed
    # ---------------------------------------------------------

    database_papers = [
        paper
        for paper in database_papers
        if paper.arxiv_id not in excluded_paper_ids_set
    ]

    # ---------------------------------------------------------
    # Step 3
    # Track everything already encountered
    # ---------------------------------------------------------

    discovered_paper_ids = (
        excluded_paper_ids_set
        | {
            paper.arxiv_id
            for paper in database_papers
        }
    )

    # ---------------------------------------------------------
    # Step 4
    # Determine whether arXiv is needed
    # ---------------------------------------------------------

    arxiv_papers = []

    papers_needed = (
        page_size
        - len(database_papers)
    )

    # ---------------------------------------------------------
    # Step 5
    # Query arXiv in controlled batches
    # ---------------------------------------------------------

    while papers_needed > 0:

        arxiv_batch_size = ARXIV_BATCH_SIZE

        print(
            f"ARXIV SEARCH: "
            f"start={arxiv_start}, "
            f"batch_size={arxiv_batch_size}, "
            f"papers_needed={papers_needed}"
        )

        current_batch = list(
            arxiv_connector.search_papers(
                query=query,
                max_results=arxiv_batch_size,
                start=arxiv_start,
                published_after=published_after,
                published_before=published_before
            )
        )

        # -----------------------------------------------------
        # No more arXiv results
        # -----------------------------------------------------

        if not current_batch:
            break

        # -----------------------------------------------------
        # IMPORTANT:
        #
        # Advance by the number of arXiv results actually
        # consumed, regardless of how many were duplicates.
        # -----------------------------------------------------

        arxiv_start += len(
            current_batch
        )

        # -----------------------------------------------------
        # Compare arXiv results against everything encountered
        # -----------------------------------------------------

        for paper in current_batch:

            if paper.arxiv_id in discovered_paper_ids:
                continue

            discovered_paper_ids.add(
                paper.arxiv_id
            )

            arxiv_papers.append(
                paper
            )

            papers_needed = (
                page_size
                - len(database_papers)
                - len(arxiv_papers)
            )

            if papers_needed <= 0:
                break

        # -----------------------------------------------------
        # If arXiv returned fewer results than requested,
        # there are no more results available.
        # -----------------------------------------------------

        if len(current_batch) < arxiv_batch_size:
            break

    # ---------------------------------------------------------
    # Step 6
    # Store newly discovered arXiv papers
    # ---------------------------------------------------------

    for paper in arxiv_papers:

        database.insert_whole_paper(
            cur,
            paper
        )

    # ---------------------------------------------------------
    # Step 7
    # Combine PostgreSQL and arXiv candidates
    # ---------------------------------------------------------

    combined_papers = (
        database_papers
        + arxiv_papers
    )

    # ---------------------------------------------------------
    # Step 8
    # Rank candidates
    # ---------------------------------------------------------

    ranked_papers = rank_search_results(
        combined_papers,
        query
    )

    # ---------------------------------------------------------
    # Step 9
    # Verify requested page size
    # ---------------------------------------------------------

    final_results = ranked_papers[:page_size]

    if len(final_results) < page_size:

        print(
            f"WARNING: Requested {page_size} papers "
            f"but only found "
            f"{len(final_results)}."
        )

    return {
        "papers": final_results,
        "next_arxiv_start": arxiv_start
    }




def rank_search_results(
    papers,
    query
):

    if not papers:
        return []

    # ---------------------------------------------------------
    # No query:
    # newest papers first
    # ---------------------------------------------------------

    if not query or not query.strip():

        return sorted(
            papers,
            key=lambda paper: paper.published_at,
            reverse=True
        )

    # ---------------------------------------------------------
    # TF-IDF relevance
    # ---------------------------------------------------------

    tfidf_results = recommend_by_tfidf(
        papers,
        query.strip()
    )

    tfidf_scores = {
        paper.arxiv_id: score
        for paper, score in tfidf_results
    }

    # ---------------------------------------------------------
    # Calculate combined relevance + recency score
    # ---------------------------------------------------------

    scored_papers = []

    current_time = datetime.now(
        timezone.utc
    )

    for paper in papers:

        relevance_score = tfidf_scores.get(
            paper.arxiv_id,
            0.0
        )

        published_at = paper.published_at

        if published_at.tzinfo is None:
            published_at = published_at.replace(
                tzinfo=timezone.utc
            )

        age_days = max(
            (current_time - published_at).days,
            0
        )

        recency_score = 1 / (
            1 + age_days / 365
        )

        combined_score = (
            0.75 * relevance_score
            + 0.25 * recency_score
        )

        scored_papers.append(
            (
                paper,
                combined_score
            )
        )

    scored_papers.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return [
        paper
        for paper, score in scored_papers
    ]