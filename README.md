# AI Resume Skill Gap Analyzer

An AI-powered platform that analyzes resumes and job descriptions to identify missing skills, recommend learning paths, and automate career development insights.

---

## Overview

The **AI Resume Skill Gap Analyzer** uses **Sentence-BERT embeddings** to measure skill similarity between candidate resumes and job descriptions.  
It integrates **OpenAI’s GPT API** to generate personalized upskilling recommendations and runs on a **containerized FastAPI microservice architecture**, deployed via **Microsoft Azure** with **CI/CD pipelines** powered by **GitHub Actions**.

---

## Key Features

- **Skill Matching:** Extracts and compares resume and job description skills using semantic similarity (Sentence-BERT).  
- **AI Recommendations:** Uses OpenAI GPT models to suggest courses, certifications, and personalized learning paths.  
- **Modular Design:** Built with FastAPI microservices for parsing, embedding, analysis, and recommendations.  
- **Cloud-Native Deployment:** Containerized with Docker and deployed on Microsoft Azure.  
- **Automated CI/CD:** GitHub Actions pipeline for build, test, and deployment — reducing manual deployment time by **70%**.  

---

## Project Structure

main.py -> Initializes FastAPI app
routes.py -> REST API routes
schemas.py -> Data models (Pydantic)
parser.py -> Resume & job text extraction
embedder.py -> Generates Sentence-BERT embeddings
analyzer.py -> Computes skill similarity & gaps
recommender.py -> OpenAI-powered learning suggestions
known_skills.json -> Skill taxonomy reference
roles.json -> Role-to-skill benchmark mapping

---

## Tech Stack

| Category | Tools |
|-----------|--------|
| **Backend** | FastAPI, Python |
| **AI / NLP** | Sentence-BERT, OpenAI API |
| **Data Processing** | Pandas, scikit-learn |
| **Containerization** | Docker |
| **Cloud & Deployment** | Microsoft Azure, GitHub Actions |
| **Architecture** | Microservices, REST API |
