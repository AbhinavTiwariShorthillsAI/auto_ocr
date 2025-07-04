from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
import os
from pathlib import Path
from PIL import Image
import io
import logging
from typing import List, Dict, Any
import glob
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="OCR Labeling API", version="1.0.0")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Create necessary directories
IMAGES_DIR = Path("images")
LABELS_FILE = Path("labels.txt")

# Mount static files for serving images
app.mount("/images", StaticFiles(directory="images"), name="images")

def natural_sort_key(text):
    """Convert a string into a list of string and number chunks for natural sorting."""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

def get_image_list() -> List[str]:
    """Get list of all images in the images directory."""
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff"]
    image_files = []
    
    for extension in image_extensions:
        image_files.extend(glob.glob(str(IMAGES_DIR / extension)))
        image_files.extend(glob.glob(str(IMAGES_DIR / extension.upper())))
    
    # Return just the filenames, not full paths, with natural sorting
    filenames = [os.path.basename(f) for f in image_files]
    return sorted(filenames, key=natural_sort_key)

def get_processed_images() -> set:
    """Get set of already processed images from labels.txt."""
    processed = set()
    if LABELS_FILE.exists():
        try:
            with open(LABELS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Skip empty lines
                        # Split on first space - everything before first space is image name
                        parts = line.split(' ', 1)
                        if parts:
                            processed.add(parts[0])
        except Exception as e:
            logger.error(f"Error reading labels file: {e}")
    return processed

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {"message": "OCR Labeling API", "version": "1.0.0"}

@app.get("/api/images")
async def get_images():
    """Get list of all images and progress information."""
    try:
        all_images = get_image_list()
        processed_images = get_processed_images()
        
        return {
            "total_images": len(all_images),
            "processed_images": len(processed_images),
            "remaining_images": len(all_images) - len(processed_images),
            "images": all_images,
            "processed": list(processed_images)
        }
    except Exception as e:
        logger.error(f"Error getting images: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/images/next")
async def get_next_image():
    """Get the next unprocessed image."""
    try:
        all_images = get_image_list()
        processed_images = get_processed_images()
        
        if not all_images:
            raise HTTPException(status_code=404, detail="No images found")
        
        # Find first unprocessed image
        for image in all_images:
            if image not in processed_images:
                return {
                    "image_name": image,
                    "image_url": f"/images/{image}",
                    "total_images": len(all_images),
                    "processed_images": len(processed_images)
                }
        
        # All images processed
        return {
            "message": "All images have been processed",
            "total_images": len(all_images),
            "processed_images": len(processed_images)
        }
    except Exception as e:
        logger.error(f"Error getting next image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ocr")
async def extract_text(file: UploadFile = File(...)):
    """Extract text from uploaded image using PaddleOCR."""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Perform OCR
        result = ocr.ocr(image_data, cls=True)
        
        # Extract text from results
        extracted_text = []
        if result and result[0]:
            for line in result[0]:
                if line and len(line) > 1:
                    text = line[1][0]  # Get the text part
                    confidence = line[1][1]  # Get confidence score
                    extracted_text.append({
                        "text": text,
                        "confidence": confidence
                    })
        
        # Combine all text
        combined_text = " ".join([item["text"] for item in extracted_text])
        
        return {
            "extracted_text": combined_text,
            "detailed_results": extracted_text,
            "success": True
        }
    
    except Exception as e:
        logger.error(f"Error in OCR processing: {e}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@app.post("/api/ocr/file")
async def extract_text_from_file(image_name: str):
    """Extract text from a specific image file in the images directory."""
    try:
        image_path = IMAGES_DIR / image_name
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Perform OCR on the image file
        result = ocr.ocr(str(image_path), cls=True)
        
        # Extract text from results
        extracted_text = []
        if result and result[0]:
            for line in result[0]:
                if line and len(line) > 1:
                    text = line[1][0]  # Get the text part
                    confidence = line[1][1]  # Get confidence score
                    extracted_text.append({
                        "text": text,
                        "confidence": confidence
                    })
        
        # Combine all text
        combined_text = " ".join([item["text"] for item in extracted_text])
        
        return {
            "extracted_text": combined_text,
            "detailed_results": extracted_text,
            "success": True,
            "image_name": image_name
        }
    
    except Exception as e:
        logger.error(f"Error in OCR processing for {image_name}: {e}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@app.post("/api/save")
async def save_label(image_name: str = Form(...), corrected_text: str = Form(...)):
    """Save the corrected text for an image to labels.txt."""
    try:
        # Validate inputs
        if not image_name or not corrected_text:
            raise HTTPException(status_code=400, detail="Both image_name and corrected_text are required")
        
        # Check if image exists
        image_path = IMAGES_DIR / image_name
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Clean the text (remove newlines and extra spaces)
        cleaned_text = " ".join(corrected_text.split())
        
        # Append to labels.txt (space-separated format: image_name text)
        with open(LABELS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{image_name} {cleaned_text}\n")
        
        logger.info(f"Saved label for {image_name}: {cleaned_text}")
        
        return {
            "success": True,
            "message": f"Label saved for {image_name}",
            "image_name": image_name,
            "saved_text": cleaned_text
        }
    
    except Exception as e:
        logger.error(f"Error saving label: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save label: {str(e)}")

@app.get("/api/labels")
async def get_labels():
    """Get all saved labels."""
    try:
        labels = []
        if LABELS_FILE.exists():
            with open(LABELS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Skip empty lines
                        # Split on first space - first part is image name, rest is text
                        parts = line.split(' ', 1)
                        if len(parts) >= 2:
                            image_name = parts[0]
                            text = parts[1]
                        elif len(parts) == 1:
                            image_name = parts[0]
                            text = ""
                        else:
                            continue
                        
                        labels.append({
                            "image_name": image_name,
                            "text": text
                        })
        
        return {
            "labels": labels,
            "count": len(labels)
        }
    
    except Exception as e:
        logger.error(f"Error getting labels: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 