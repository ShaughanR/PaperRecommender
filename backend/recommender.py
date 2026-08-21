from backend.models import Paper
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_by_category(papers: list[Paper], user_categories: list[str]) -> list[tuple[Paper, float]]:

    scored_papers = []

    for paper in papers:
        matching_categories = sum(category in user_categories for category in paper.categories)

        if paper.categories:
            score = matching_categories / len(paper.categories)
        else:
            score = 0.0

        scored_papers.append((paper, score))

    scored_papers.sort(key=lambda item: item[1], reverse=True)

    return scored_papers



def paper_to_text(paper):
    return f"{paper.title} {paper.abstract}"


def recommend_by_tfidf(papers: list[Paper], user_interest: str) -> list[tuple[Paper, float]]:

    documents = [user_interest] + [paper_to_text(paper) for paper in papers]

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(documents)

    user_vector = tfidf_matrix[0]
    paper_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(user_vector, paper_vectors)[0]

    return [(paper, score) for paper, score in zip(papers, similarities)]


INTERACTION_WEIGHTS = {
    "liked": 1.0,
    "saved": 0.8,
    "pdf_opened": 0.4,
    "viewed": 0.1,
    "disliked": -1.0
}

def recommend_by_feedback(
    papers: list[Paper],
    user_interactions: list[tuple[Paper, str]]
) -> list[tuple[Paper, float]]:

    if not user_interactions:
        return [(paper, 0.0) for paper in papers]

    interaction_papers = [
        paper
        for paper, _ in user_interactions
    ]

    all_documents = (
        [paper_to_text(paper) for paper in papers]
        + [paper_to_text(paper) for paper in interaction_papers]
    )

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        all_documents
    )

    candidate_count = len(papers)

    candidate_vectors = tfidf_matrix[
        :candidate_count
    ]

    interaction_vectors = tfidf_matrix[
        candidate_count:
    ]

    similarities = cosine_similarity(
        candidate_vectors,
        interaction_vectors
    )

    scored_papers = []

    for candidate_index, candidate in enumerate(papers):

        feedback_score = 0.0
        total_weight = 0.0

        for interaction_index, (_, interaction_type) in enumerate(
            user_interactions
        ):

            weight = INTERACTION_WEIGHTS.get(
                interaction_type,
                0.0
            )

            similarity = similarities[
                candidate_index,
                interaction_index
            ]

            feedback_score += similarity * weight
            total_weight += abs(weight)

        if total_weight > 0:
            feedback_score /= total_weight

        scored_papers.append(
            (candidate, feedback_score)
        )

    scored_papers.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return scored_papers


def calculate_combined_score(
    category_score,
    tfidf_score,
    feedback_score
):
    return (
        0.30 * category_score
        + 0.55 * tfidf_score
        + 0.15 * feedback_score
    )

def recommend_combined(
    papers: list[Paper],
    user_categories: list[str],
    user_interest: str,
    user_interactions: list[tuple[Paper, str]],
    n=5
):
    category_results = recommend_by_category(
        papers,
        user_categories
    )

    tfidf_results = recommend_by_tfidf(
        papers,
        user_interest
    )

    feedback_results = recommend_by_feedback(
        papers,
        user_interactions
    )

    category_scores = {
        paper.arxiv_id: score
        for paper, score in category_results
    }

    tfidf_scores = {
        paper.arxiv_id: score
        for paper, score in tfidf_results
    }

    feedback_scores = {
        paper.arxiv_id: score
        for paper, score in feedback_results
    }

    combined_results = []

    for paper in papers:

        category_score = category_scores.get(
            paper.arxiv_id,
            0.0
        )

        tfidf_score = tfidf_scores.get(
            paper.arxiv_id,
            0.0
        )

        feedback_score = feedback_scores.get(
            paper.arxiv_id,
            0.0
        )

        final_score = calculate_combined_score(
            category_score,
            tfidf_score,
            feedback_score
        )

        combined_results.append(
            (paper, final_score)
        )

    combined_results.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return combined_results[:n]
