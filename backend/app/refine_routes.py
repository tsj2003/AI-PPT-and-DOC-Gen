from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .models import Section, Refinement, User, Feedback, Comment
from .schemas import GenerateContentRequest, RefineContentRequest, FeedbackCreate, CommentCreate, CommentResponse
from .auth import get_current_user
from .llm_service import generate_section_content, refine_section_content
from typing import List

router = APIRouter(tags=["generation"])

@router.post("/generate/")
def generate_content(
    request: GenerateContentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    section = db.query(Section).filter(Section.id == request.section_id).first()
    
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    
    if section.project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    generated_content = generate_section_content(
        title=section.title,
        topic=section.project.topic,
        doc_type=section.project.document_type.value,
        additional_context=request.additional_context or ""
    )
    
    section.content = generated_content
    db.commit()
    db.refresh(section)
    
    return {"section_id": section.id, "content": section.content}

@router.post("/refine/")
def refine_content(
    request: RefineContentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    section = db.query(Section).filter(Section.id == request.section_id).first()
    
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    
    if section.project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    if not section.content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Section has no content to refine")
    
    original_content = section.content
    refined_content = refine_section_content(section.content, request.refine_prompt)
    
    refinement = Refinement(
        section_id=section.id,
        original_content=original_content,
        refined_content=refined_content,
        refine_prompt=request.refine_prompt
    )
    db.add(refinement)
    
    section.content = refined_content
    db.commit()
    db.refresh(section)
    
    return {"section_id": section.id, "content": section.content, "refinement_id": refinement.id}

@router.post("/feedback/", status_code=status.HTTP_201_CREATED)
def add_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    section = db.query(Section).filter(Section.id == feedback_data.section_id).first()
    
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    
    existing_feedback = db.query(Feedback).filter(
        Feedback.section_id == feedback_data.section_id,
        Feedback.user_id == current_user.id
    ).first()
    
    if existing_feedback:
        existing_feedback.is_liked = feedback_data.is_liked
    else:
        feedback = Feedback(
            section_id=feedback_data.section_id,
            user_id=current_user.id,
            is_liked=feedback_data.is_liked
        )
        db.add(feedback)
    
    db.commit()
    
    return {"message": "Feedback recorded"}

@router.post("/comments/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    section = db.query(Section).filter(Section.id == comment_data.section_id).first()
    
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    
    comment = Comment(
        section_id=comment_data.section_id,
        user_id=current_user.id,
        content=comment_data.content
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return comment

@router.get("/sections/{section_id}/comments/", response_model=List[CommentResponse])
def get_section_comments(
    section_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    section = db.query(Section).filter(Section.id == section_id).first()
    
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    
    comments = db.query(Comment).filter(Comment.section_id == section_id).all()
    return comments
