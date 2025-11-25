# AI Document Generator - Copilot Instructions

## Architecture Overview

This is a full-stack AI document authoring platform with FastAPI backend + React frontend:

- **Backend**: FastAPI (port 8000) with SQLAlchemy + SQLite, Gemini AI integration
- **Frontend**: React + Vite (port 5000) with Tailwind CSS
- **AI Services**: Google Gemini for content generation, HuggingFace for image generation
- **Export**: Python-docx for Word, python-pptx for PowerPoint documents

## Core Data Model

```
User -> Project -> Section -> [Refinement, Feedback, Comment]
```

Projects have a `document_type` enum (`DOCX`/`PPTX`) that drives export behavior. Sections are ordered and contain AI-generated content. The refinement system tracks content evolution with original/refined versions.

## Critical Development Workflows

### Backend Development
- **Start server**: Use the VS Code task "Start Backend Server" or `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` from `/backend`
- **Environment**: Requires `GEMINI_API_KEY` and `JWT_SECRET` in `.env` file
- **Database**: SQLite auto-initializes on startup via `init_db()` in main.py

### Frontend Development
- **Start dev server**: `npm run dev` from `/frontend` (runs on port 5000)
- **API proxy**: Vite config should proxy `/api` requests to backend

### Authentication Flow
- JWT tokens stored in localStorage on frontend
- Backend uses `get_current_user` dependency for protected routes
- Token format: `{"sub": user_id}` as string per JWT spec

## Key Patterns & Conventions

### Route Organization
- **Main routes**: Defined in `main.py` (auth endpoints)
- **Feature routes**: Separate routers (`project_routes.py`, `ai_routes.py`, etc.)
- **Route prefixes**: `/projects`, `/refine`, `/export`, `/ai`

### AI Content Generation
- **Content generation**: `llm_service.py` with Gemini 2.5-flash model
- **Prompt engineering**: Enforces plain text output (no markdown), 150-250 words
- **Image generation**: `image_generation.py` uses HuggingFace Stable Diffusion XL
- **Content refinement**: Tracks original content + user prompts for improvements

### Export System
- **DOCX exports**: `docx_generator.py` creates Word documents with sections
- **PPTX exports**: `pptx_generator.py` creates PowerPoint with title slide + content slides
- **File storage**: Exports saved to `backend/exports/`, images to `backend/generated_images/`

### Frontend API Integration
- **API modules**: Organized by feature in `src/api/` (auth.js, projects.js, ai.js)
- **Route protection**: `PrivateRoute` component checks `isAuthenticated()`
- **State management**: Local component state (no global state library)

## Development Gotchas

- **CORS**: Backend allows all origins (`["*"]`) for development
- **File paths**: Use absolute paths for VS Code tools; relative paths in terminal commands
- **Token handling**: Frontend stores JWT in localStorage, backend expects Bearer token
- **Content validation**: AI service cleans markdown artifacts from generated content
- **Section ordering**: Sections have explicit `order` field for consistent display

## Environment Setup Requirements

- Python 3.11+ with dependencies from `pyproject.toml`
- Node.js 20+ for frontend
- Gemini API key for content generation
- Optional: HuggingFace API key for image generation

## Testing & Debugging

- **API docs**: Available at `http://localhost:8000/docs` (Swagger) when backend running
- **Database inspection**: SQLite file at `backend/app.db`
- **Error handling**: FastAPI returns structured HTTP exceptions; frontend shows user-friendly messages
