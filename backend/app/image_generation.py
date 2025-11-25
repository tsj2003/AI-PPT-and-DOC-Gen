"""
Image generation module using HuggingFace Inference API
Uses: InferenceClient + stabilityai/stable-diffusion-xl-base-1.0 model
"""

import os
from datetime import datetime
from .config import settings
import google.generativeai as genai

# Configure Gemini for prompt engineering
genai.configure(api_key=settings.GEMINI_API_KEY)


def engineer_image_prompt(slide_title: str, slide_content: str, topic: str) -> str:
    """
    Use Gemini to create a visual, realistic prompt for image generation from slide content
    
    Example input:
      - slide_title: "Introduction to Guru Gobind Singh Ji"
      - slide_content: "Historical details about the Tenth Guru..."
      - topic: "Sikh History"
    
    Example output:
      - "A realistic historical painting of Guru Gobind Singh Ji on a horse, 
         wearing traditional Sikh attire, set in 17th century India"
    """
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""Create a SHORT, VISUAL image prompt (1-2 sentences) for Stable Diffusion XL.
The prompt should be realistic, vivid, and suitable for professional presentations.

Slide Title: {slide_title}
Slide Content: {slide_content[:200]}
Topic: {topic}

Requirements:
- Make it VISUAL and DESCRIPTIVE (not abstract)
- Use realistic adjectives: realistic, professional, detailed, high-quality
- Include style suggestions: painting, illustration, photography, 3D render
- Keep it under 80 words
- NO generic descriptions, make it SPECIFIC to the content

Return ONLY the image prompt, nothing else."""
    
    try:
        response = model.generate_content(prompt)
        engineered_prompt = response.text.strip()
        print(f"  📝 Prompt engineered: {engineered_prompt[:80]}...")
        return engineered_prompt
    except Exception as e:
        print(f"  ✗ Prompt engineering failed: {str(e)}")
        # Fallback to simple description
        return f"A professional illustration about {slide_title}, realistic style, high quality"


def generate_images_for_sections(sections: list, topic: str) -> dict:
    """
    Generate images for PowerPoint slides using multiple fallback methods
    
    Methods:
    1. HuggingFace Inference API (if token has permissions)
    2. Free HuggingFace spaces (fallback)
    3. Placeholder images (final fallback)
    """
    import requests
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    import time
    
    image_paths = {}
    
    # Get HF token from environment
    hf_token = os.environ.get('HF_TOKEN') or settings.HUGGINGFACE_API_KEY
    
    if not hf_token:
        print("⚠ HF_TOKEN not found in environment. Creating placeholder images.")
        return create_placeholder_images(sections, topic)
    
    print(f"✓ Trying HuggingFace API with token")
    
    # Try HuggingFace Inference API first
    try:
        from huggingface_hub import InferenceClient
        client = InferenceClient(api_key=hf_token)
        result = generate_with_inference_client(client, sections, topic)
        
        # If no images were generated successfully, fall back to placeholders
        if not result or len(result) == 0:
            print("⚠ No images generated successfully. Creating professional placeholder images.")
            return create_placeholder_images(sections, topic)
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        print(f"⚠ HuggingFace Inference API failed: {error_msg}")
        
        if "403" in error_msg or "permissions" in error_msg.lower():
            print("⚠ Token doesn't have Inference API permissions. Using fallback method.")
            return create_placeholder_images(sections, topic)
        else:
            print("⚠ Other error with Inference API. Creating placeholder images.")
            return create_placeholder_images(sections, topic)


def create_placeholder_images(sections: list, topic: str) -> dict:
    """Create professional-looking placeholder images"""
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    
    image_paths = {}
    
    for section in sections:
        try:
            # Create a professional-looking image
            width, height = 1024, 768
            img = Image.new('RGB', (width, height), color='#f8f9fa')
            draw = ImageDraw.Draw(img)
            
            # Try to load a system font
            try:
                font_large = ImageFont.truetype("Arial.ttf", 48)
                font_medium = ImageFont.truetype("Arial.ttf", 32)
                font_small = ImageFont.truetype("Arial.ttf", 24)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw gradient background
            for i in range(height):
                alpha = i / height
                color_r = int(72 + (248 - 72) * alpha)  # From blue to light gray
                color_g = int(123 + (249 - 123) * alpha)
                color_b = int(182 + (250 - 182) * alpha)
                draw.line([(0, i), (width, i)], fill=(color_r, color_g, color_b))
            
            # Add topic title
            topic_text = f"Topic: {topic}"
            topic_bbox = draw.textbbox((0, 0), topic_text, font=font_small)
            topic_width = topic_bbox[2] - topic_bbox[0]
            draw.text(((width - topic_width) // 2, 50), topic_text, 
                     fill='#2c3e50', font=font_small)
            
            # Add section title with text wrapping
            title = section.title
            wrapped_title = textwrap.fill(title, width=30)
            title_bbox = draw.textbbox((0, 0), wrapped_title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            
            draw.text(((width - title_width) // 2, (height - title_height) // 2), 
                     wrapped_title, fill='#2c3e50', font=font_large)
            
            # Add decorative elements (subtle border)
            draw.rectangle([50, height-100, width-50, height-80], fill='#3498db')
            
            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:20]
            filename = f"slide_{section.id}_{timestamp}.png"
            filepath = os.path.join(settings.IMAGES_DIR, filename)
            img.save(filepath, quality=95)
            
            image_paths[section.id] = filepath
            print(f"  ✅ Placeholder image created: {filepath}")
            
        except Exception as e:
            print(f"  ✗ Failed to create placeholder for section {section.id}: {str(e)}")
            continue
    
    return image_paths


def generate_with_free_api(sections: list, topic: str, hf_token: str) -> dict:
    """Try to use free HuggingFace spaces for image generation"""
    print("🎨 Using free HuggingFace Spaces API as fallback...")
    
    # For now, fall back to placeholder images
    # You could implement calls to free HF spaces here
    return create_placeholder_images(sections, topic)


def generate_with_inference_client(client, sections: list, topic: str) -> dict:
    """Generate images using HuggingFace InferenceClient"""
    from PIL import Image
    from io import BytesIO
    import time
    
    image_paths = {}
    
    # Negative prompt to avoid unwanted artifacts
    negative_prompt = "cartoon, low quality, blurry, text, watermark, pixelated"
    
    for section in sections:
        try:
            print(f"\n🎨 Processing: {section.title}")
            
            # Step 1: Engineer a better prompt from slide content
            engineered_prompt = engineer_image_prompt(
                section.title,
                section.content or "",
                topic
            )
            
            # Step 2: Generate image using InferenceClient
            print(f"  🚀 Calling Stable Diffusion XL...")
            
            max_retries = 2
            retry_count = 0
            image_success = False
            
            while retry_count < max_retries and not image_success:
                try:
                    # Call the model with engineered prompt
                    image_result = client.text_to_image(
                        prompt=engineered_prompt,
                        model="stabilityai/stable-diffusion-xl-base-1.0",
                        negative_prompt=negative_prompt,
                        height=768,
                        width=1024,
                    )
                    
                    # Handle different return types from HuggingFace API
                    if hasattr(image_result, 'save'):
                        # It's already a PIL Image
                        image = image_result
                    else:
                        # It's bytes, convert to PIL Image
                        image = Image.open(BytesIO(image_result))
                    
                    # Save image
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:20]
                    filename = f"slide_{section.id}_{timestamp}.png"
                    filepath = os.path.join(settings.IMAGES_DIR, filename)
                    image.save(filepath, quality=95)
                    
                    image_paths[section.id] = filepath
                    print(f"  ✅ Image generated: {filepath}")
                    image_success = True
                    
                except Exception as e:
                    error_msg = str(e)
                    print(f"  ✗ Generation attempt {retry_count + 1}/{max_retries} failed")
                    print(f"    Error: {error_msg}")
                    
                    # Check for specific error types
                    if "overloaded" in error_msg.lower() or "503" in error_msg:
                        retry_count += 1
                        if retry_count < max_retries:
                            wait_time = 3 * retry_count
                            print(f"    ⏳ Retrying in {wait_time}s...")
                            time.sleep(wait_time)
                    else:
                        # Permissions or other errors - stop trying
                        print(f"    Permission/API error - not retrying")
                        raise
                        
        except Exception as e:
            print(f"  ✗ ERROR: Failed to generate image for section {section.id}")
            print(f"    Details: {str(e)}")
            print(f"    Proceeding to next section...")
            continue
    
    print(f"\n📊 Summary: Generated {len(image_paths)}/{len(sections)} images")
    return image_paths
