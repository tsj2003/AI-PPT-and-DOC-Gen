# AI Document Authoring Platform

A full-stack application for creating professional documents and presentations with AI-powered content generation and refinement.

## Features

- **User Authentication**: Secure JWT-based authentication system
- **Project Management**: Create and manage multiple document/presentation projects
- **AI Content Generation**: Generate professional content using Gemini AI
- **Content Refinement**: Refine and improve content with custom prompts
- **Feedback System**: Like/dislike and comment on generated content
- **Export**: Export to Word (DOCX) or PowerPoint (PPTX) formats
- **Real-time Updates**: Live content updates in the editor

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy + SQLite
- Gemini AI
- python-docx & python-pptx
- JWT Authentication

### Frontend
- React 18
- Vite
- React Router
- Tailwind CSS
- Axios

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Gemini API Key

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables (Gemini API key is required)

4. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open http://localhost:5000 in your browser

## Usage

1. **Register/Login**: Create an account or login
2. **Create Project**: Choose document type (DOCX/PPTX) and add sections
3. **Generate Content**: Use AI to generate professional content for each section
4. **Refine Content**: Improve content with custom refinement prompts
5. **Add Feedback**: Like/dislike and comment on generated content
6. **Export**: Download your completed document or presentation

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── models.py         # Database models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── auth.py           # Authentication logic
│   │   ├── llm_service.py    # Gemini AI integration
│   │   ├── docx_generator.py # Word export
│   │   ├── pptx_generator.py # PowerPoint export
│   │   └── routes/           # API routes
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/            # React pages
│   │   ├── components/       # React components
│   │   ├── api/              # API client modules
│   │   └── App.jsx           # Main app component
│   └── package.json
│
└── README.md
```

## Environment Variables

### Backend
- `JWT_SECRET`: Secret key for JWT tokens
- `GEMINI_API_KEY`: Google Gemini API key

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT
