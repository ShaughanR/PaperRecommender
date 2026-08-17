import database
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(username, password):
    password_hash = generate_password_hash(password)

    with database.get_connection() as conn:
        with conn.cursor() as cur:
            return database.insert_user(cur, username, password_hash)


def authenticate_user(username, password):
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            user = database.get_user_by_username(cur, username)

            if user is None:
                return None

            user_id, user_name, password_hash, created_at = user

            if check_password_hash(password_hash, password):
                return user_id

            return None

def get_user_categories(user_id):
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            return database.get_user_interests(cur, user_id)


def add_user_category(user_id, category_id):
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            database.insert_user_interest(cur, user_id, category_id)


def remove_user_category(user_id, category_id):
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            database.delete_user_interest(cur, user_id, category_id)


def record_paper_interaction(user_id, paper_id, interaction_type):
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            return database.insert_paper_interaction(
                cur,
                user_id,
                paper_id,
                interaction_type
            )


def get_user_interactions(user_id):
    with database.get_connection() as conn:
        with conn.cursor() as cur:
            return database.get_user_paper_interactions(cur, user_id)
