from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .auth import get_current_user
from .models import User
from .schemas import GenerateTitleRequest, GenerateOutlineRequest, GenerateSlideImageRequest
from .llm_service import generate_title as llm_generate_title
from .llm_service import generate_outline as llm_generate_outline
import json

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/generate-title/")
def generate_project_title(
    request: GenerateTitleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        title = llm_generate_title(request.topic)
        return {"title": title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate title: {str(e)}")

@router.post("/generate-outline/")
def generate_project_outline(
    request: GenerateOutlineRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        outline = llm_generate_outline(request.topic, request.document_type.value, request.num_sections)
        sections = json.loads(outline) if isinstance(outline, str) else outline
        return {"sections": sections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate outline: {str(e)}")

# Image generation is now handled via export route with generate_images_for_sections()
# using HuggingFace InferenceClient + prompt engineering
