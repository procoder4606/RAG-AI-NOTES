"""
Audio transcription module using OpenAI Whisper
"""
import whisper
import os

def transcribe_audio(audio_path):
    """
    Transcribe audio from video or audio file using Whisper
    
    Args:
        audio_path (str): Path to the audio or video file
        
    Returns:
        str: Transcribed text
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    print(f"Loading Whisper model...")
    # Using 'base' model for balance between speed and accuracy
    # Options: tiny, base, small, medium, large
    model = whisper.load_model("tiny")
    
    print(f"Transcribing: {audio_path}")
    result = model.transcribe(audio_path, verbose=False)
    
    transcript = result["text"]
    print(f"✓ Transcription complete ({len(transcript)} characters)")
    
    return transcript
