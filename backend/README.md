# AI Document Authoring Platform - Backend

## Overview
FastAPI backend for AI-assisted document and presentation generation using Gemini AI.

## Features
- JWT authentication
- SQLite database with SQLAlchemy ORM
- Gemini AI integration for content generation and refinement
- Export to DOCX and PPTX formats
- RESTful API endpoints

## Setup

### Environment Variables
Create a `.env` file in the backend directory:
```
JWT_SECRET=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
```

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Run Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Projects
- `POST /projects` - Create new project
- `GET /projects` - Get all user projects
- `GET /projects/{id}` - Get specific project
- `DELETE /projects/{id}` - Delete project

### Generation & Refinement
- `POST /generate` - Generate content for section
- `POST /refine` - Refine existing content
- `POST /feedback` - Add like/dislike feedback
- `POST /comments` - Add comment to section
- `GET /sections/{id}/comments` - Get section comments

### Export
- `GET /export/{project_id}` - Export project to DOCX or PPTX
