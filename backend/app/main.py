from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .database import get_db, init_db
from .models import User
from .schemas import UserCreate, UserLogin, UserResponse, Token
from .auth import get_password_hash, verify_password
from .utils.jwt_handler import create_access_token
from .utils.validators import validate_password, validate_username
from .project_routes import router as project_router
from .refine_routes import router as refine_router
from .export_routes import router as export_router
from .ai_routes import router as ai_router
from .config import settings
import os

app = FastAPI(title="Document Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Document Generator API"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint that also tests database connectivity"""
    try:
        # Test database connection
        user_count = db.query(User).count()
        return {
            "status": "healthy", 
            "database": "connected",
            "total_users": user_count,
            "timestamp": "2024-11-25"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error", 
            "error": str(e),
            "timestamp": "2024-11-25"
        }

@app.post("/auth/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    is_valid, message = validate_username(user_data.username)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    is_valid, message = validate_password(user_data.password)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(project_router)
app.include_router(refine_router)
app.include_router(export_router)
app.include_router(ai_router)

# Mount static files for generated images
if os.path.exists(settings.IMAGES_DIR):
    app.mount("/images", StaticFiles(directory=settings.IMAGES_DIR), name="images")
else:
    os.makedirs(settings.IMAGES_DIR, exist_ok=True)
    app.mount("/images", StaticFiles(directory=settings.IMAGES_DIR), name="images")
