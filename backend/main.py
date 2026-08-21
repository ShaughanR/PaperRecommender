from fastapi import FastAPI, Depends, HTTPException
from psycopg.errors import UniqueViolation
from fastapi.middleware.cors import CORSMiddleware


from backend import database, authentication, users
from backend.models import Paper, CreateUserRequest, UserCreate, UserLogin, Token, UserInteraction, UserCategory


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
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
    return database.get_paper_queried_multiple(cur, query, published_after, published_before, limit)

@app.get("/api/papers/{paper_id}", response_model=Paper)
def get_paper(paper_id: str, cur=Depends(database.get_db)):
    return database.get_paper_single(cur, paper_id)

#####user stuff##############################################
#####user stuff##############################################
#####user stuff##############################################
#####user stuff##############################################


@app.post("/api/auth/register")
def register_user(
    user: UserCreate,
    cur=Depends(database.get_db)
):
    try:
        return users.create_user(
            cur,
            user.username,
            user.password
        )

    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )


@app.post("/api/auth/login", response_model=Token)
def login_user(
    user: UserLogin,
    cur=Depends(database.get_db)
):
    user_id = users.authenticate_user(
        cur,
        user.username,
        user.password
    )

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    access_token = authentication.create_access_token(user_id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/api/auth/me")
def get_current_user(
    user_id: int = Depends(authentication.get_current_user)
):
    return {"user_id": user_id}


@app.post("/api/users/interactions")
def record_interaction(
    interaction: UserInteraction,
    user=Depends(authentication.get_current_user),
    cur=Depends(database.get_db)
):
    return users.record_paper_interaction(
        cur,
        user,
        interaction.paper_id,
        interaction.interaction_type
    )

@app.get("/api/users/interactions")
def get_interactions(
    user=Depends(authentication.get_current_user),
    cur=Depends(database.get_db)
):
    return users.get_user_interactions(
        cur,
        user
    )

@app.get("/api/users/categories")
def get_categories(
    user=Depends(authentication.get_current_user),
    cur=Depends(database.get_db)
):
    return users.get_user_categories(
        cur,
        user["user_id"]
    )

@app.post("/api/users/categories")
def add_category(
    category: UserCategory,
    user=Depends(authentication.get_current_user),
    cur=Depends(database.get_db)
):
    users.add_user_category(
        cur,
        user["user_id"],
        category.category_id
    )

    return {
        "message": "Category added"
    }

@app.delete("/api/users/categories/{category_id}")
def remove_category(
    category_id: int,
    user=Depends(authentication.get_current_user),
    cur=Depends(database.get_db)
):
    users.remove_user_category(
        cur,
        user["user_id"],
        category_id
    )

    return {
        "message": "Category removed"
    }

################################################
#########recommender stuff######################
################################################

@app.get("/api/recommendations")
def get_recommendations(
    user=Depends(authentication.get_current_user),
    cur=Depends(database.get_db)
):
    papers = database.get_paper_multiple(
        cur,
        50
    )

    recommendations = users.get_user_recommendations(
        cur,
        user,
        papers,
        limit=10
    )

    return [
        {
            "paper": paper.model_dump(),
            "recommendation_score": score
        }
        for paper, score in recommendations
    ]