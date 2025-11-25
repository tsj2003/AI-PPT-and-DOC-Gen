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

@router.post("/generate-slide-image/")
def generate_slide_image(
    request: GenerateSlideImageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        from .image_generation import engineer_image_prompt, generate_with_free_api
        from .config import settings
        import os
        
        # Create a dummy section object for the image generation
        class DummySection:
            def __init__(self, title, content="", id=1):
                self.title = title
                self.content = content
                self.id = id
        
        # Create section from request
        section = DummySection(request.prompt, "Generated for individual slide")
        sections = [section]
        
        # Get HF token
        hf_token = os.environ.get('HF_TOKEN') or settings.HUGGINGFACE_API_KEY
        
        # Try to generate image using our enhanced pipeline
        if hf_token:
            try:
                from huggingface_hub import InferenceClient
                from .image_generation import generate_with_inference_client
                
                client = InferenceClient(api_key=hf_token)
                result = generate_with_inference_client(client, sections, "presentation")
                
                if result and section.id in result:
                    image_path = result[section.id]
                    return {"success": True, "message": "Image generated successfully", "image_path": image_path}
                else:
                    # Fallback to free API
                    result = generate_with_free_api(sections, "presentation", hf_token)
                    if result and section.id in result:
                        image_path = result[section.id]
                        return {"success": True, "message": "Image generated via fallback API", "image_path": image_path}
                    else:
                        return {"success": False, "message": "Image generation failed, but will be included during export"}
            except Exception as e:
                print(f"Individual image generation failed: {str(e)}")
                return {"success": False, "message": f"Image generation failed: {str(e)}"}
        else:
            return {"success": False, "message": "HuggingFace token not configured"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate image: {str(e)}")
