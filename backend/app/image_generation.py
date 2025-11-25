"""
Image generation module using HuggingFace Inference API and Free APIs
Uses: Multiple models with fallbacks for better image quality
Updated: Enhanced AI image generation with multiple providers
"""

import os
from datetime import datetime
from .config import settings
import google.generativeai as genai

# Configure Gemini for prompt engineering
genai.configure(api_key=settings.GEMINI_API_KEY)


def filepath_to_url(filepath: str) -> str:
    """Convert a local file path to a URL path for the API"""
    # Extract just the filename from the full path
    filename = os.path.basename(filepath)
    # Return the URL path that matches our static files mount
    return f"/images/{filename}"


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
    
    prompt = f"""Create a detailed, visual image prompt for AI image generation.
Make it specific, realistic, and professional for a presentation slide.

Slide Title: {slide_title}
Slide Content: {slide_content[:300]}
Overall Topic: {topic}

Create a prompt that includes:
1. Main subject/scene (be specific - people, places, objects)
2. Visual style (realistic photograph, historical painting, detailed illustration)
3. Setting/background (time period, location, environment)
4. Quality descriptors (high quality, detailed, professional, 8k)
5. Avoid text, logos, or abstract concepts

Examples:
- For Guru Nanak: "A realistic historical painting of Guru Nanak Dev Ji sitting under a tree, wearing white robes and turban, teaching disciples in 15th century Punjab countryside, detailed oil painting style, warm golden lighting, high quality, professional artwork"
- For Sikh Empire: "A detailed historical illustration of the Sikh Empire golden period, showing Lahore Fort with Sikh soldiers in blue uniforms, realistic 19th century setting, detailed architecture, high quality historical artwork"

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
    
    # Try HuggingFace Inference API first (with faster timeout)
    try:
        from huggingface_hub import InferenceClient
        client = InferenceClient(api_key=hf_token)
        result = generate_with_inference_client(client, sections, topic)
        
        # If no images were generated successfully, fall back to placeholders
        if not result or len(result) == 0:
            print("⚠ No images generated successfully. Creating professional placeholder images.")
            return create_placeholder_images(sections, topic)
        
        return result
        
    except ImportError as e:
        print(f"⚠ HuggingFace Hub not installed: {str(e)}")
        print("⚠ Falling back to free API alternatives...")
        try:
            return generate_with_free_api(sections, topic, hf_token)
        except Exception as fallback_error:
            print(f"⚠ Free API also failed: {str(fallback_error)}")
            print("⚠ Creating placeholder images...")
            return create_placeholder_images(sections, topic)
        
    except Exception as e:
        error_msg = str(e)
        print(f"⚠ HuggingFace Inference API failed: {error_msg}")
        
        if "403" in error_msg or "permissions" in error_msg.lower():
            print("⚠ Token doesn't have Inference API permissions. Trying free alternative...")
            return generate_with_free_api(sections, topic, hf_token)
        else:
            print("⚠ Other error with Inference API. Trying free alternative...")
            return generate_with_free_api(sections, topic, hf_token)


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
            
            image_paths[section.id] = {
                "filepath": filepath,
                "url": filepath_to_url(filepath)
            }
            print(f"  ✅ Placeholder image created: {filepath}")
            
        except Exception as e:
            print(f"  ✗ Failed to create placeholder for section {section.id}: {str(e)}")
            continue
    
    return image_paths


def generate_with_free_api(sections: list, topic: str, hf_token: str) -> dict:
    """Try to use alternative free APIs for image generation"""
    print("🎨 Trying alternative free image generation API...")
    
    import requests
    from PIL import Image
    from io import BytesIO
    import time
    
    start_time = time.time()
    max_total_time = 30  # Maximum 30 seconds for all image generation
    image_paths = {}
    
    # Try Pollinations.ai (free alternative)
    for section in sections:
        # Check if we've exceeded our time limit
        if time.time() - start_time > max_total_time:
            print(f"⏰ Time limit reached ({max_total_time}s), switching to placeholders for remaining sections...")
            break
            
        try:
            print(f"\n🎨 Processing with free API: {section.title}")
            
            # Create engineered prompt
            engineered_prompt = engineer_image_prompt(
                section.title,
                section.content or "",
                topic
            )
            
            # Try multiple free APIs in sequence
            apis_to_try = [
                {
                    "name": "Pollinations.ai FLUX",
                    "url": f"https://image.pollinations.ai/prompt/{requests.utils.quote(engineered_prompt)}?width=1024&height=768&model=flux&enhance=true"
                },
                {
                    "name": "Pollinations.ai Turbo",
                    "url": f"https://image.pollinations.ai/prompt/{requests.utils.quote(engineered_prompt)}?width=1024&height=768&model=turbo&enhance=true"
                },
                {
                    "name": "Basic Pollinations",
                    "url": f"https://image.pollinations.ai/prompt/{requests.utils.quote(engineered_prompt)}?width=1024&height=768"
                }
            ]
            
            response = None
            for api in apis_to_try:
                try:
                    print(f"  🚀 Calling {api['name']}...")
                    response = requests.get(api['url'], timeout=8)  # Very fast timeout for production
                    if response.status_code == 200:
                        print(f"  ✅ Success with {api['name']}")
                        break
                    else:
                        print(f"  ✗ {api['name']} failed with status {response.status_code}")
                except Exception as api_error:
                    print(f"  ✗ {api['name']} failed: {str(api_error)}")
                    continue
            
            if response and response.status_code == 200:
                # Validate image content
                try:
                    image = Image.open(BytesIO(response.content))
                    # Ensure minimum image size (avoid tiny error images)
                    if image.size[0] >= 100 and image.size[1] >= 100:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:20]
                        filename = f"slide_{section.id}_{timestamp}.png"
                        filepath = os.path.join(settings.IMAGES_DIR, filename)
                        image.save(filepath, quality=95)
                        
                        image_paths[section.id] = {
                            "filepath": filepath,
                            "url": filepath_to_url(filepath)
                        }
                        print(f"  ✅ AI image generated successfully: {filepath}")
                    else:
                        print(f"  ✗ Generated image too small: {image.size}")
                except Exception as img_error:
                    print(f"  ✗ Invalid image data: {str(img_error)}")
            else:
                print(f"  ✗ All free APIs failed")
                
        except Exception as e:
            print(f"  ✗ Free API failed for section {section.id}: {str(e)}")
            continue
    
    # If no images generated, create enhanced placeholders
    if not image_paths:
        print("🎨 All APIs failed, creating enhanced placeholder images...")
        return create_enhanced_placeholders(sections, topic)
    
    # If only partial images generated, fill in the rest with placeholders
    missing_sections = [s for s in sections if s.id not in image_paths]
    if missing_sections:
        print(f"🎨 Creating placeholders for {len(missing_sections)} missing sections...")
        placeholder_images = create_enhanced_placeholders(missing_sections, topic)
        image_paths.update(placeholder_images)
    
    return image_paths


def create_enhanced_placeholders(sections: list, topic: str) -> dict:
    """Create enhanced, topic-specific placeholder images"""
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    
    image_paths = {}
    
    # Topic-specific color schemes and icons
    color_schemes = {
        "sikh": {"bg": "#FF6B35", "accent": "#004E89", "text": "#FFFFFF", "gradient": "#FF8C42"},
        "history": {"bg": "#8B4513", "accent": "#DAA520", "text": "#FFFFFF", "gradient": "#A0522D"}, 
        "religion": {"bg": "#4682B4", "accent": "#FFD700", "text": "#FFFFFF", "gradient": "#5F9EA0"},
        "ecommerce": {"bg": "#E74C3C", "accent": "#3498DB", "text": "#FFFFFF", "gradient": "#EC7063"},
        "business": {"bg": "#2C3E50", "accent": "#F39C12", "text": "#FFFFFF", "gradient": "#34495E"},
        "technology": {"bg": "#9B59B6", "accent": "#1ABC9C", "text": "#FFFFFF", "gradient": "#AF7AC5"},
        "default": {"bg": "#2C3E50", "accent": "#3498DB", "text": "#FFFFFF", "gradient": "#34495E"}
    }
    
    # Detect topic theme with more categories
    topic_lower = topic.lower()
    section_lower = section.title.lower() if hasattr(section, 'title') else ""
    combined_text = f"{topic_lower} {section_lower}"
    
    if "sikh" in combined_text:
        colors = color_schemes["sikh"]
    elif "history" in combined_text or "guru" in combined_text:
        colors = color_schemes["history"]
    elif "religion" in combined_text or "spiritual" in combined_text:
        colors = color_schemes["religion"]
    elif "ecommerce" in combined_text or "commerce" in combined_text or "shopping" in combined_text or "retail" in combined_text:
        colors = color_schemes["ecommerce"]
    elif "business" in combined_text or "market" in combined_text or "strategy" in combined_text:
        colors = color_schemes["business"]
    elif "technology" in combined_text or "digital" in combined_text or "tech" in combined_text or "ai" in combined_text:
        colors = color_schemes["technology"]
    else:
        colors = color_schemes["default"]
    
    for section in sections:
        try:
            # Create enhanced professional image with gradient
            width, height = 1024, 768
            img = Image.new('RGB', (width, height), color=colors["bg"])
            draw = ImageDraw.Draw(img)
            
            # Create diagonal gradient
            bg_color = [int(colors["bg"][i:i+2], 16) for i in (1, 3, 5)]
            gradient_color = [int(colors["gradient"][i:i+2], 16) for i in (1, 3, 5)]
            
            for y in range(height):
                for x in range(width):
                    # Calculate gradient based on distance from top-left
                    distance = ((x/width)**2 + (y/height)**2)**0.5
                    alpha = min(distance, 1.0)
                    
                    r = int(bg_color[0] * (1-alpha) + gradient_color[0] * alpha)
                    g = int(bg_color[1] * (1-alpha) + gradient_color[1] * alpha)
                    b = int(bg_color[2] * (1-alpha) + gradient_color[2] * alpha)
                    
                    if x % 4 == 0 and y % 4 == 0:  # Sample every 4th pixel for performance
                        draw.point((x, y), fill=(r, g, b))
            
            # Add topic and section info with better typography
            try:
                font_title = ImageFont.truetype("Arial.ttf", 40)
                font_topic = ImageFont.truetype("Arial.ttf", 28)
            except:
                font_title = ImageFont.load_default()
                font_topic = ImageFont.load_default()
            
            # Add decorative elements
            accent_color = colors["accent"]
            
            # Modern geometric shapes
            # Top-right triangle
            triangle_points = [(width-200, 0), (width, 0), (width, 200)]
            draw.polygon(triangle_points, fill=accent_color)
            
            # Bottom-left circle
            circle_radius = 150
            draw.ellipse([50, height-circle_radius-50, 50+circle_radius, height-50], 
                        fill=accent_color, width=3)
            
            # Decorative lines
            for i in range(3):
                y_pos = height - 150 + (i * 20)
                draw.rectangle([width-250, y_pos, width-100, y_pos+4], fill=colors["text"])
            
            # Border frame
            border_width = 6
            draw.rectangle([border_width, border_width, width-border_width, height-border_width], 
                         outline=colors["text"], width=border_width)
            
            # Add topic title
            topic_text = topic.upper()
            topic_bbox = draw.textbbox((0, 0), topic_text, font=font_topic)
            topic_width = topic_bbox[2] - topic_bbox[0]
            draw.text(((width - topic_width) // 2, 80), topic_text, 
                     fill=colors["text"], font=font_topic)
            
            # Add section title with better wrapping
            title = section.title
            wrapped_title = textwrap.fill(title, width=25)
            title_lines = wrapped_title.split('\n')
            
            total_height = len(title_lines) * 50
            start_y = (height - total_height) // 2
            
            for i, line in enumerate(title_lines):
                line_bbox = draw.textbbox((0, 0), line, font=font_title)
                line_width = line_bbox[2] - line_bbox[0]
                draw.text(((width - line_width) // 2, start_y + i * 50), 
                         line, fill=colors["text"], font=font_title)
            
            # Save the enhanced image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:20]
            filename = f"slide_{section.id}_{timestamp}.png"
            filepath = os.path.join(settings.IMAGES_DIR, filename)
            img.save(filepath, quality=95)
            
            image_paths[section.id] = {
                "filepath": filepath,
                "url": filepath_to_url(filepath)
            }
            print(f"  ✅ Enhanced placeholder created: {filepath}")
            
        except Exception as e:
            print(f"  ✗ Failed to create enhanced placeholder for section {section.id}: {str(e)}")
            continue
    
    return image_paths


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
                    # Try multiple models in order of preference
                    models_to_try = [
                        "black-forest-labs/FLUX.1-dev",  # Better quality, newer model
                        "stabilityai/stable-diffusion-xl-base-1.0",  # Fallback
                        "runwayml/stable-diffusion-v1-5"  # Final fallback
                    ]
                    
                    model_used = None
                    for model in models_to_try:
                        try:
                            print(f"    Trying model: {model}")
                            image_result = client.text_to_image(
                                prompt=engineered_prompt,
                                model=model,
                                negative_prompt=negative_prompt,
                                height=768,
                                width=1024,
                            )
                            model_used = model
                            print(f"    ✓ Success with: {model}")
                            break
                        except Exception as model_error:
                            print(f"    ✗ {model} failed: {str(model_error)}")
                            continue
                    
                    if not model_used:
                        raise Exception("All models failed to generate image")
                    
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
                    
                    image_paths[section.id] = {
                        "filepath": filepath,
                        "url": filepath_to_url(filepath)
                    }
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
