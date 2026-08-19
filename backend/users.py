import database
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(cur, username, password):
    password_hash = generate_password_hash(password)
    return database.insert_user(cur, username, password_hash)


def authenticate_user(cur, username, password):
    user = database.get_user_by_username(cur, username)

    if user is None:
        return None

    user_id, user_name, password_hash, created_at = user

    if check_password_hash(password_hash, password):
        return user_id

    return None

def get_user_categories(cur, user_id):
    return database.get_user_interests(cur, user_id)


def add_user_category(cur, user_id, category_id):
    database.insert_user_interest(cur, user_id, category_id)


def remove_user_category(cur, user_id, category_id):
    database.delete_user_interest(cur, user_id, category_id)


def record_paper_interaction(cur,user_id, paper_id, interaction_type):
    return database.insert_paper_interaction(
        cur,
        user_id,
        paper_id,
        interaction_type
    )


def get_user_interactions(cur, user_id):
    return database.get_user_paper_interactions(cur, user_id)
