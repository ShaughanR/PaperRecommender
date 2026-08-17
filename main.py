from arxiv_connector import search_papers
from database import insert_whole_paper
from database import get_paper_multiple, get_connection
from recommender import recommend_combined
import textwrap


def display_paper(paper):
    print("=" * 80)
    print(f"Title: {paper.title}")
    print("\nAuthors:")
    print(textwrap.fill(", ".join(paper.authors), width=100))
    print(f"Categories: {', '.join(paper.categories)}")
    print(f"Published: {paper.published_at}")
    print(f"Updated: {paper.updated_at}")
    print(f"DOI: {paper.doi or 'N/A'}")
    print(f"PDF: {paper.pdf_url}")

    print("\nAbstract:")
    print(textwrap.fill(paper.abstract, width=100))

    print("=" * 80)


def display_papers(papers):
    for paper in papers:
        display_paper(paper)







def main():
    for query in [
        "machine learning",
        "deep learning",
        "ai",
        "machine vision"
    ]:

        for paper in search_papers(query, 20):
            insert_whole_paper(paper)




    with get_connection() as conn:
        with conn.cursor() as cur:
            database_papers = get_paper_multiple(cur, 10)

            recommended_papers = recommend_combined(
                database_papers,
                user_categories = ["cs.LG", "cs.MA", "cs.AI", "cs.CV"],
                user_interest="""
                machine learning
                artificial intelligence
                deep learning
                computer vision
                machine vision
                natural language processing
                AI agents
                agentic systems
                autonomous agents
                multi-agent systems
                large language models
                neural networks
                representation learning
                reinforcement learning
                robotics
                parallel computing
                AI planning
                generative AI
                """
            )

            for paper, score in recommended_papers:
                print(f"Recommendation score: {score:.2f}")
                display_paper(paper)


if __name__ == "__main__":
    main()
