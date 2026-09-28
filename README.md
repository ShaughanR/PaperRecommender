# Research Paper Recommendation Platform

A full-stack research paper discovery and recommendation application built with Python, FastAPI, PostgreSQL, React, and scikit-learn.

## Overview
The application ingests paper metadata from arXiv, stores normalized data in PostgreSQL, supports search and authentication, tracks user interactions, and generates personalized paper recommendations.

## Features
- arXiv paper ingestion pipeline
- PostgreSQL relational database
- Full-text paper search
- JWT authentication
- Personalized recommendations
- Likes, dislikes, saves, views, and PDF-open tracking
- React frontend
- FastAPI REST backend

## Recommendation Approach
The ranking system combines:
- Category affinity
- TF-IDF cosine similarity
- Explicit user feedback
- Implicit behavioral signals

## Architecture
Frontend → FastAPI API → PostgreSQL
                     ↓
              Recommendation Engine

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- React
- scikit-learn
- JWT

## Screenshots
...

## Running Locally
...

## Future Improvements
...
