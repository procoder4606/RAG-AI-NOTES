"""
OCR module for extracting on-screen text from video frames
"""
import cv2
import pytesseract
import os
from PIL import Image
import tempfile

def extract_ocr_text(video_path, interval_sec=10):
    """
    Extract on-screen text from video at regular intervals
    
    Args:
        video_path (str): Path to the video file
        interval_sec (int): Interval in seconds between frame captures
        
    Returns:
        str: Extracted text from all frames
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    print(f"Opening video: {video_path}")
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        raise ValueError("Could not open video file")
    
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"Video info: {duration:.1f}s, {fps:.1f} fps")
    
    frame_interval = int(fps * interval_sec)
    extracted_texts = []
    frame_count = 0
    processed_frames = 0
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        # Process frame at intervals
        if frame_count % frame_interval == 0:
            # Convert to grayscale for better OCR
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to improve text detection
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extract text using pytesseract
            text = pytesseract.image_to_string(thresh, config='--psm 6')
            
            if text.strip():  # Only add non-empty text
                timestamp = frame_count / fps
                extracted_texts.append(f"[{timestamp:.1f}s] {text.strip()}")
                processed_frames += 1
        
        frame_count += 1
    
    video.release()
    
    print(f"✓ OCR complete: processed {processed_frames} frames")
    
    if not extracted_texts:
        return "No on-screen text detected."
    
    return "\n\n".join(extracted_texts)
