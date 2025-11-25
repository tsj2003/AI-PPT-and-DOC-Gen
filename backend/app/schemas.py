from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from .models import DocumentType

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class SectionCreate(BaseModel):
    title: str
    order: int

class SectionResponse(BaseModel):
    id: int
    title: str
    content: str
    order: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    title: str
    topic: str
    document_type: DocumentType
    sections: List[SectionCreate]

class ProjectResponse(BaseModel):
    id: int
    title: str
    topic: str
    document_type: DocumentType
    owner_id: int
    created_at: datetime
    updated_at: datetime
    sections: List[SectionResponse] = []
    
    class Config:
        from_attributes = True

class GenerateContentRequest(BaseModel):
    section_id: int
    additional_context: Optional[str] = None

class RefineContentRequest(BaseModel):
    section_id: int
    refine_prompt: str

class FeedbackCreate(BaseModel):
    section_id: int
    is_liked: bool

class CommentCreate(BaseModel):
    section_id: int
    content: str

class CommentResponse(BaseModel):
    id: int
    section_id: int
    user_id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class GenerateTitleRequest(BaseModel):
    topic: str

class GenerateOutlineRequest(BaseModel):
    topic: str
    document_type: DocumentType
    num_sections: int = 5

class GenerateSlideImageRequest(BaseModel):
    prompt: str
    enable_image: bool = True
