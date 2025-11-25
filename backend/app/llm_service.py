import google.generativeai as genai
from .config import settings
from .image_generation import generate_images_for_sections
import json
import os
from datetime import datetime

genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_section_content(title: str, topic: str, doc_type: str, additional_context: str = "") -> str:
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""You are a professional content writer creating high-quality business content.

Task: Write content for the section titled "{title}" in a {doc_type} document about "{topic}"
{f'Additional context: {additional_context}' if additional_context else ''}

Requirements:
- Write 150-250 words of professional, engaging content
- Use clear, business-appropriate language
- Do NOT use markdown formatting (no **, *, #, etc.)
- Write in plain text with proper paragraphs
- Focus on substance and clarity
- Do NOT include the section title in your response
- Make the content informative and well-structured
- End with complete sentences, not cut-off text

Write only the content, nothing else."""
    
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Clean up any markdown formatting that might slip through
        content = content.replace('**', '')
        content = content.replace('*', '')
        content = content.replace('##', '')
        content = content.replace('#', '')
        
        # Ensure content ends properly
        if content and not content.endswith(('.', '!', '?', ':')):
            # Find the last complete sentence
            sentences = content.split('. ')
            if len(sentences) > 1:
                content = '. '.join(sentences[:-1]) + '.'
            else:
                content = content.rstrip() + '.'
        
        return content
    except Exception as e:
        return f"Error generating content: {str(e)}"

def refine_section_content(existing_text: str, refine_prompt: str) -> str:
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""You are refining professional content based on user feedback.

Original text:
{existing_text}

Refinement instructions:
{refine_prompt}

Requirements:
- Apply the requested changes while maintaining professional quality
- Keep the content length appropriate (150-250 words)
- Use plain text formatting (NO markdown symbols like **, *, #)
- Ensure proper grammar and complete sentences
- Make the text flow naturally and professionally
- End with complete sentences

Provide only the refined text, nothing else."""
    
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        # Clean up any markdown formatting
        content = content.replace('**', '')
        content = content.replace('*', '')
        content = content.replace('##', '')
        content = content.replace('#', '')
        
        # Ensure content ends properly
        if content and not content.endswith(('.', '!', '?', ':')):
            sentences = content.split('. ')
            if len(sentences) > 1:
                content = '. '.join(sentences[:-1]) + '.'
            else:
                content = content.rstrip() + '.'
        
        return content
    except Exception as e:
        return f"Error refining content: {str(e)}"

def generate_title(topic: str) -> str:
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""Generate a clean, professional, concise project title (3-7 words) for the following topic.
Topic: {topic}

Respond with ONLY the title, no explanations or quotes."""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip().strip('"\'')
    except Exception as e:
        return f"Generated Project on {topic}"

def generate_outline(topic: str, doc_type: str, num_sections: int = 5) -> str:
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    section_type = "slide titles" if doc_type == "pptx" else "section headers"
    
    prompt = f"""Generate {num_sections} professional {section_type} for a {doc_type} document about: {topic}

Return as a JSON array of objects with 'title' and 'order' fields.
Example: [{{"title": "Introduction", "order": 0}}, {{"title": "Main Points", "order": 1}}]

Respond with ONLY the JSON array, no explanation."""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Extract JSON from response
        start_idx = text.find('[')
        end_idx = text.rfind(']') + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = text[start_idx:end_idx]
            sections = json.loads(json_str)
            for i, section in enumerate(sections):
                section['order'] = i
            return sections
        else:
            # Fallback: create basic outline
            return [{"title": f"Section {i+1}", "order": i} for i in range(num_sections)]
    except Exception as e:
        return [{"title": f"Section {i+1}", "order": i} for i in range(num_sections)]

