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

### Home Page
The main landing page allows users to search for research papers, filter by publication date, and control the number of results returned.

<img src="screenshots/Homepage.png" alt="Homepage" width="900">

### Logged-In Home Page
Authenticated users can access personalized recommendations in addition to the standard search functionality.

<img src="screenshots/LoggedInHomepage.png" alt="Logged In Homepage" width="900">

### Search Results
Users can search for papers by topic and filter results by publication date. Search results display paper metadata, categories, abstracts, and available actions.

<img src="screenshots/ExampleSearch.png" alt="Example Search Results" width="900">

### Personalized Recommendations
The recommendation system ranks papers based on user interests and interaction history. Users can like, dislike, save, view, or open papers to provide additional feedback to the recommendation engine.

<img src="screenshots/ExampleRecommendation.png" alt="Personalized Paper Recommendations" width="900">

### Authentication

#### Login
Users can securely log in to access personalized features including recommendations.

<img src="screenshots/Login.png" alt="Login Page" width="750">

#### Create Account
New users can create an account to begin tracking interactions and receiving personalized recommendations.

<img src="screenshots/CreateAccount.png" alt="Create Account Page" width="750">

