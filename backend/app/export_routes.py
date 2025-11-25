from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .database import get_db
from .models import Project, User, DocumentType
from .auth import get_current_user
from .docx_generator import generate_docx
from .pptx_generator import generate_pptx
from .image_generation import generate_images_for_sections
import os

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/{project_id}/")
def export_project(
    project_id: int,
    include_images: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    sections = project.sections
    
    if not sections:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project has no sections")
    
    image_paths = {}
    if project.document_type == DocumentType.PPTX and include_images:
        try:
            image_paths = generate_images_for_sections(sections, project.topic)
        except Exception as e:
            print(f"Warning: Image generation failed, continuing without images: {str(e)}")
    
    if project.document_type == DocumentType.DOCX:
        filepath = generate_docx(project, sections)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        filepath = generate_pptx(project, sections, image_paths)
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Export failed")
    
    filename = os.path.basename(filepath)
    
    return FileResponse(
        path=filepath,
        media_type=media_type,
        filename=filename
    )
