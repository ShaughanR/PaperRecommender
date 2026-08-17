import psycopg
from sensitive_info import password
from models import Paper
def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="arXiv_data",
        user="postgres",
        password=password
    )

def insert_paper(cur, paper):
    cur.execute(
        """
        INSERT INTO papers (
            paper_id,
            title,
            publish_datetime,
            update_datetime,
            doi,
            pdf_url,
            abstract
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (paper_id) DO UPDATE
        SET
            title = EXCLUDED.title,
            publish_datetime = EXCLUDED.publish_datetime,
            update_datetime = EXCLUDED.update_datetime,
            doi = EXCLUDED.doi,
            pdf_url = EXCLUDED.pdf_url,
            abstract = EXCLUDED.abstract

        WHERE papers.update_datetime < EXCLUDED.update_datetime
            OR papers.update_datetime IS NULL
        RETURNING paper_id;
        """,
        (
            paper.arxiv_id,
            paper.title,
            paper.published_at,
            paper.updated_at,
            paper.doi,
            paper.pdf_url,
            paper.abstract
        )
    )
    return cur.fetchone()

def delete_paper_relationships(cur, paper_id):
    cur.execute(
        """
        DELETE FROM paper_author
        WHERE paper_id = %s
        """,
        (paper_id,)
    )
    cur.execute(
        """
        DELETE FROM paper_category
        WHERE paper_id = %s
        """,
        (paper_id,)
    )

def insert_author_and_return_author_id(cur, author_name):
    cur.execute(
        """
        INSERT INTO authors (author_name)
        VALUES (%s)
        ON CONFLICT (author_name)
        DO UPDATE SET author_name = EXCLUDED.author_name
        RETURNING author_id;
        """,
        (author_name,)
    )

    return cur.fetchone()[0]


def insert_category_and_return_category_id(cur, category_name):
    cur.execute(
        """
        INSERT INTO categories (category_name)
        VALUES (%s)
        ON CONFLICT (category_name)
        DO UPDATE SET category_name = EXCLUDED.category_name
        RETURNING category_id
        """,
        (category_name,)
    )
    return cur.fetchone()[0]

def create_paper_author_relationship(cur, paper_id, author_id):
    cur.execute(
        """
        INSERT INTO paper_author (
            paper_id,
            author_id
            )
            VALUES (%s, %s)
            ON CONFLICT (paper_id, author_id)
            DO NOTHING
            """,
        (
            paper_id,
            author_id
        )
    )

def create_paper_category_relationship(cur, paper_id, category_id):
    cur.execute(
        """
        INSERT INTO paper_category (
            paper_id,
            category_id
        )
        VALUES (%s, %s)
        ON CONFLICT (paper_id, category_id)
        DO NOTHING
        """,
        (
            paper_id,
            category_id
        )
    )

def insert_whole_paper(paper):
    with get_connection() as conn:
        with conn.cursor() as cur:
            result = insert_paper(cur, paper)
            if result is None:
                return

            delete_paper_relationships(cur, paper.arxiv_id)
            for author_name in paper.authors:
                author_id = insert_author_and_return_author_id(cur, author_name)
                create_paper_author_relationship(cur, paper.arxiv_id, author_id)
            for category_name in paper.categories:
                category_id = insert_category_and_return_category_id(cur, category_name)
                create_paper_category_relationship(cur, paper.arxiv_id, category_id)



def get_paper_single(cur, paper_id):
    cur.execute(
        """
        SELECT
            paper_id,
            title,
            publish_datetime,
            update_datetime,
            doi,
            pdf_url,
            abstract
        FROM papers
        WHERE paper_id = %s
        """,
        (paper_id,)
    )

    paper_row = cur.fetchone()
    if paper_row is None:
        return None
    return build_paper(cur, paper_row)



def get_paper_multiple(cur, limit):
    cur.execute(
        """
        SELECT
            paper_id,
            title,
            publish_datetime,
            update_datetime,
            doi,
            pdf_url,
            abstract
        FROM papers
        ORDER BY publish_datetime DESC
        LIMIT %s
        """,
        (limit,)
    )

    return [build_paper(cur, row) for row in cur.fetchall()]


def get_paper_queried_multiple(cur, query):
    cur.execute(
        """
        SELECT
            paper_id,
            title,
            publish_datetime,
            update_datetime,
            doi,
            pdf_url,
            abstract
        FROM papers
        WHERE title ILIKE %s
           OR abstract ILIKE %s
        """,
        (f"%{query}%", f"%{query}%")
    )

    paper_rows = cur.fetchall()
    papers = []
    for paper_row in paper_rows:
        papers.append(build_paper(cur, paper_row))
    return papers

def build_paper(cur, paper_row):
    paper_id = paper_row[0]

    cur.execute(
        """
        SELECT a.author_name
        FROM authors a
        JOIN paper_author pa
            ON a.author_id = pa.author_id
        WHERE pa.paper_id = %s
        """,
        (paper_id,)
    )

    authors = [row[0] for row in cur.fetchall()]

    cur.execute(
        """
        SELECT c.category_name
        FROM categories c
        JOIN paper_category pc
            ON c.category_id = pc.category_id
        WHERE pc.paper_id = %s
        """,
        (paper_id,)
    )

    categories = [row[0] for row in cur.fetchall()]

    return Paper(
        arxiv_id=paper_row[0],
        title=paper_row[1],
        authors=authors,
        abstract=paper_row[6],
        published_at=paper_row[2],
        updated_at=paper_row[3],
        doi=paper_row[4],
        categories=categories,
        pdf_url=paper_row[5]
    )


##############################################
#####database methods for user stuff##########
##############################################


def insert_user(cur, username, password_hash):
    cur.execute(
        """
        INSERT INTO users (
            user_name,
            user_pass_hash
        )
        VALUES (%s, %s)
        RETURNING user_id;
        """,
        (
            username,
            password_hash
        )
    )

    return cur.fetchone()[0]

def get_user_by_username(cur, username):
    cur.execute(
        """
        SELECT
            user_id,
            user_name,
            user_pass_hash,
            created_at
        FROM users
        WHERE user_name = %s
        """,
        (username,)
    )

    return cur.fetchone()

def get_user_interests(cur, user_id):
    cur.execute(
        """
        SELECT c.category_name
        FROM categories c
        JOIN user_interests ui
            ON c.category_id = ui.category_id
        WHERE ui.user_id = %s
        """,
        (user_id,)
    )

    return [row[0] for row in cur.fetchall()]

def insert_user_interest(cur, user_id, category_id):
    cur.execute(
        """
        INSERT INTO user_interests (
            user_id,
            category_id
        )
        VALUES (%s, %s)
        ON CONFLICT (user_id, category_id)
        DO NOTHING
        """,
        (
            user_id,
            category_id
        )
    )

def delete_user_interest(cur, user_id, category_id):
    cur.execute(
        """
        DELETE FROM user_interests
        WHERE user_id = %s
          AND category_id = %s
        """,
        (
            user_id,
            category_id
        )
    )

def insert_paper_interaction(
    cur,
    user_id,
    paper_id,
    interaction_type
):
    cur.execute(
        """
        INSERT INTO user_paper_interactions (
            user_id,
            paper_id,
            interaction_type
        )
        VALUES (%s, %s, %s)
        RETURNING interaction_id;
        """,
        (
            user_id,
            paper_id,
            interaction_type
        )
    )

    return cur.fetchone()[0]

def get_user_paper_interactions(cur, user_id):
    cur.execute(
        """
        SELECT
            interaction_id,
            paper_id,
            interaction_type,
            interaction_timestamp
        FROM user_paper_interactions
        WHERE user_id = %s
        ORDER BY interaction_timestamp DESC
        """,
        (user_id,)
    )

    return cur.fetchall()
