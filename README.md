# AI Document Generator

A full-stack web application for creating professional documents and presentations with AI-powered content generation. The platform enables users to generate, refine, and export high-quality documents using advanced AI technologies.

## Live Demo

**Live Application**: [https://docugenaii.netlify.app/](https://docugenaii.netlify.app/)

**GitHub Repository**: [https://github.com/tsj2003/AI-PPT-and-DOC-Gen.git](https://github.com/tsj2003/AI-PPT-and-DOC-Gen.git)

Access the fully deployed application to test all features including user registration, AI content generation, and document export functionality.

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Node.js 20 or higher
- Google Gemini API key
- Git (for cloning the repository)

### Clone Repository
```bash
git clone https://github.com/tsj2003/AI-PPT-and-DOC-Gen.git
cd AI-PPT-and-DOC-Gen
```

### Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Dependencies
```bash
cd frontend
npm install
```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
JWT_SECRET=your-super-secret-jwt-key-here
GEMINI_API_KEY=your-google-gemini-api-key
HUGGINGFACE_API_KEY=your-huggingface-api-key (optional)
```

**Required Variables:**
- `JWT_SECRET`: A secure secret key for JWT token generation
- `GEMINI_API_KEY`: Google Gemini API key for AI content generation

**Optional Variables:**
- `HUGGINGFACE_API_KEY`: For enhanced image generation capabilities

## Running the Backend

Navigate to the backend directory and start the server:

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### Verify Backend
Visit `http://localhost:8000/health` to check server status and database connectivity.

## Running the Frontend

In a separate terminal, navigate to the frontend directory:

```bash
cd frontend
npm run dev
```

The frontend application will be available at `http://localhost:5001`

## Usage Guide

### Getting Started
1. **Registration**: Create a new account with email and username
2. **Login**: Access your account using your credentials
3. **Dashboard**: View and manage all your projects from the main dashboard

### Creating Documents
1. **New Project**: Click "Create New Project" from the dashboard
2. **Project Setup**: 
   - Enter project title and description
   - Choose document type (Word Document or PowerPoint Presentation)
   - Add section titles for your content
3. **Content Generation**: 
   - Click "Generate Content" for each section
   - AI will create professional content based on section titles
   - Review and edit generated content as needed

### Advanced Features
1. **Content Refinement**: Use custom prompts to improve generated content
2. **Image Generation**: Add professional images to enhance presentations
3. **Feedback System**: Rate content and add comments for future reference
4. **Export Options**: Download completed documents in DOCX or PPTX formats

## Demo Video

**Demo Video**: [Add your demo video link here]

### What the Demo Video Covers (Required)

The demo video includes:

- User registration and login
- Creating a new project from the dashboard
- Configuring a Word (.docx) document
- Configuring a PowerPoint (.pptx) document
- AI content generation for sections and slides
- Using refinement features (AI prompts, like/dislike, comments)
- Viewing saved refinements and updated content
- Exporting documents in DOCX and PPTX formats
- (Optional) Using AI to auto-generate outlines or slide titles

*Note: Replace the placeholder above with your actual demo video URL when available.*

## Project Structure

```
AI-Document-Generator/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── models.py            # Database models and schemas
│   │   ├── auth.py              # Authentication and JWT handling
│   │   ├── config.py            # Application configuration
│   │   ├── database.py          # Database connection and setup
│   │   ├── llm_service.py       # Google Gemini AI integration
│   │   ├── image_generation.py  # AI image generation service
│   │   ├── docx_generator.py    # Word document export
│   │   ├── pptx_generator.py    # PowerPoint export
│   │   ├── project_routes.py    # Project management endpoints
│   │   ├── refine_routes.py     # Content refinement endpoints
│   │   ├── export_routes.py     # Document export endpoints
│   │   ├── ai_routes.py         # AI service endpoints
│   │   └── utils/               # Utility functions
│   ├── requirements.txt         # Python dependencies
│   └── exports/                 # Generated document storage
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx        # User authentication
│   │   │   ├── Register.jsx     # User registration
│   │   │   ├── Dashboard.jsx    # Project overview
│   │   │   ├── CreateProject.jsx # New project creation
│   │   │   └── Editor.jsx       # Content editing interface
│   │   ├── components/
│   │   │   ├── Navbar.jsx       # Navigation component
│   │   │   ├── SectionCard.jsx  # Content section display
│   │   │   └── PrivateRoute.jsx # Route protection
│   │   ├── api/
│   │   │   ├── auth.js          # Authentication API calls
│   │   │   ├── projects.js      # Project management API
│   │   │   ├── ai.js            # AI service integration
│   │   │   └── llm.js           # Content generation API
│   │   └── App.jsx              # Main application component
│   └── package.json             # Node.js dependencies
│
└── README.md                    # Project documentation
```

## Features Implemented

### Core Functionality
- **User Management**: Complete registration, login, and authentication system
- **Project Creation**: Support for both Word documents and PowerPoint presentations
- **AI Content Generation**: Professional content creation using Google Gemini AI
- **Content Management**: Full CRUD operations for project content
- **Document Export**: High-quality export to DOCX and PPTX formats

### Advanced Features
- **Content Refinement**: AI-powered content improvement with custom prompts
- **Image Generation**: Automatic image creation for presentations using multiple AI providers
- **Feedback System**: User rating and commenting on generated content
- **Real-time Updates**: Live content editing and preview
- **Responsive Design**: Mobile-friendly interface with modern UI components

### Technical Features
- **JWT Authentication**: Secure token-based authentication
- **RESTful API**: Well-structured API endpoints with proper HTTP methods
- **Database Management**: SQLite database with SQLAlchemy ORM
- **Error Handling**: Comprehensive error handling and user feedback
- **File Management**: Secure file upload and download capabilities

## Tech Stack

### Backend Technologies
- **FastAPI**: Modern Python web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM for Python
- **SQLite**: Lightweight database for development and deployment
- **Google Gemini AI**: Advanced AI for natural language generation
- **python-docx**: Library for creating and updating Word documents
- **python-pptx**: Library for creating and updating PowerPoint presentations
- **JWT (PyJWT)**: JSON Web Token implementation for authentication
- **Pydantic**: Data validation using Python type annotations

### Frontend Technologies
- **React 18**: Modern JavaScript library for building user interfaces
- **Vite**: Fast build tool and development server
- **React Router**: Declarative routing for React applications
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Axios**: Promise-based HTTP client for API communication
- **Lucide React**: Beautiful and customizable icons

### Development Tools
- **Uvicorn**: ASGI server for running FastAPI applications
- **PostCSS**: Tool for transforming CSS with JavaScript plugins
- **ESLint**: JavaScript linting utility for code quality

## API Endpoints

### Authentication Endpoints
```
POST /register          # User registration
POST /login            # User authentication
GET  /health           # System health check
```

### Project Management
```
GET    /projects       # List all user projects
POST   /projects       # Create new project
GET    /projects/{id}  # Get specific project
PUT    /projects/{id}  # Update project
DELETE /projects/{id}  # Delete project
```

### Content Generation
```
POST /generate         # Generate content for sections
POST /refine           # Refine existing content
POST /ai/generate-title        # Generate project titles
POST /ai/generate-outline      # Generate project outlines
POST /ai/generate-slide-image  # Generate images for slides
```

### Document Export
```
GET /export/{id}       # Export project as document
GET /export/{id}?include_images=true  # Export with images
```

### Feedback System
```
POST /feedback         # Submit content feedback
GET  /feedback/{id}    # Get feedback for content
POST /comments         # Add comments to content
```

## Submission

- **GitHub Repository**: https://github.com/tsj2003/AI-PPT-and-DOC-Gen
- **Live Demo**: https://docugenaii.netlify.app/
- **Demo Video**: [Add your final demo video link here]

These three links complete the required submission checklist.
