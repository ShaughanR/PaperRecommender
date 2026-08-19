from models import Paper
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


def calculate_combined_score(category_score, tfidf_score):
    return (0.3 * category_score + 0.7 * tfidf_score)



def recommend_combined(papers: list[Paper], user_categories: list[str], user_interest: str, n=5):
    category_results = recommend_by_category(papers, user_categories)

    tfidf_results = recommend_by_tfidf(papers, user_interest)

    category_scores = {paper.arxiv_id: score for paper, score in category_results}

    tfidf_scores = {paper.arxiv_id: score for paper, score in tfidf_results}

    combined_results = []

    for paper in papers:
        category_score = category_scores[paper.arxiv_id]
        tfidf_score = tfidf_scores[paper.arxiv_id]

        final_score = calculate_combined_score(category_score,tfidf_score)

        combined_results.append((paper, final_score))

    combined_results.sort(key=lambda item: item[1],reverse=True)



    return combined_results[:n]