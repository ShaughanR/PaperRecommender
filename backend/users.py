import backend.database
import backend.recommender

from werkzeug.security import generate_password_hash, check_password_hash


def create_user(cur, username, password):
    password_hash = generate_password_hash(password)
    return backend.database.insert_user(cur, username, password_hash)


def authenticate_user(cur, username, password):
    user = backend.database.get_user_by_username(cur, username)

    if user is None:
        return None

    user_id, user_name, password_hash, created_at = user

    if check_password_hash(password_hash, password):
        return user_id

    return None

def get_user_categories(cur, user_id):
    return backend.database.get_user_interests(cur, user_id)


def add_user_category(cur, user_id, category_id):
    backend.database.insert_user_interest(cur, user_id, category_id)


def remove_user_category(cur, user_id, category_id):
    backend.database.delete_user_interest(cur, user_id, category_id)


def record_paper_interaction(cur, user_id, paper_id, interaction_type):
    return backend.database.insert_paper_interaction(
        cur,
        user_id,
        paper_id,
        interaction_type
    )


def get_user_interactions(cur, user_id):
    return backend.database.get_user_paper_interactions(cur, user_id)


def build_user_profile(cur, user_id):
    interactions = backend.database.get_user_paper_interactions(
        cur,
        user_id
    )

    positive_interactions = {
        "liked",
        "saved",
        "pdf_opened"
    }

    positive_paper_ids = [
        interaction[1]
        for interaction in interactions
        if interaction[2] in positive_interactions
    ]

    user_categories = []
    user_interest_parts = []

    for paper_id in positive_paper_ids:
        paper = backend.database.get_paper_single(
            cur,
            paper_id
        )

        if paper is None:
            continue

        user_interest_parts.append(
            f"{paper.title} {paper.abstract}"
        )

        user_categories.extend(
            paper.categories
        )

    user_categories = list(set(user_categories))

    user_interest = " ".join(
        user_interest_parts
    )

    return user_categories, user_interest







###############################################
##########recommendation stuff#################
###############################################


def get_user_interaction_papers(cur, user_id):
    interactions = backend.database.get_user_paper_interactions(
        cur,
        user_id
    )

    user_interactions = []

    for interaction in interactions:
        paper_id = interaction[1]
        interaction_type = interaction[2]

        paper = backend.database.get_paper_single(
            cur,
            paper_id
        )

        if paper is None:
            continue

        user_interactions.append(
            (paper, interaction_type)
        )

    return user_interactions

def get_user_recommendations(cur, user_id, papers, limit=10):
    user_categories, user_interest = build_user_profile(
        cur,
        user_id
    )

    user_interactions = get_user_interaction_papers(
        cur,
        user_id
    )

    return backend.recommender.recommend_combined(
        papers,
        user_categories,
        user_interest,
        user_interactions,
        n=limit
    )


