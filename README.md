A work-in-progress research paper search and recommendation website built around the arXiv API. The system retrieves research papers from arXiv and stores them in a local PostgreSQL database to enable faster querying and reduce repeated API requests as the dataset grows.

The application uses FastAPI as the backend to handle data transfer between PostgreSQL, the arXiv API, and the React frontend. It also supports authenticated user profiles and tracks user interactions with papers to support personalized recommendations.

A save feature is currently being implemented, allowing users to curate and retrieve a personal collection of saved papers.

Technologies:
Python
PostgreSQL
FastAPI
React
arXiv API
