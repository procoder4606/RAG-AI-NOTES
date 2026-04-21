# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Check

Before you start, make sure you have:

- [ ] Python 3.8 or higher installed
- [ ] FFmpeg installed ([Download here](https://ffmpeg.org/download.html))
- [ ] Tesseract OCR installed ([Download here](https://github.com/UB-Mannheim/tesseract/wiki))
- [ ] An API key from [OpenRouter](https://openrouter.ai/), [Gemini](https://makersuite.google.com/app/apikey), or [OpenAI](https://platform.openai.com/api-keys)

## Quick Setup (5 Steps)

### 1. Create Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**⏱️ Note:** This will take 5-10 minutes and download ~2GB of data.

### 3. Set Up API Key

**Option A: Create .env file (Recommended)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# For example:
# AI_PROVIDER=openrouter
# OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

**Option B: Set environment variable**

```bash
# Windows (PowerShell)
$env:AI_PROVIDER="openrouter"
$env:OPENROUTER_API_KEY="your-key-here"

# macOS/Linux
export AI_PROVIDER="openrouter"
export OPENROUTER_API_KEY="your-key-here"
```

### 4. Test with a Sample File

```bash
python main.py path/to/your/video.mp4
```

### 5. Check Your Notes

Open `notes.txt` to see the generated notes!

## Troubleshooting

### "FFmpeg not found"
- **Windows**: Download from ffmpeg.org and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

### "Tesseract not found"
- **Windows**: Download installer and add to PATH
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt install tesseract-ocr`

### "API Error"
- Check your API key is correct in .env file
- Verify your API provider account has credits
- Make sure AI_PROVIDER matches your chosen service

### Slow Processing
- Use smaller Whisper model: Edit `transcriber.py`, change `"base"` to `"tiny"`
- Reduce OCR frequency: Edit `main.py`, change `interval_sec=10` to `30` or higher

## What's Next?

- Read the full [README.md](README.md) for detailed configuration
- Customize the note format in `notes_generator.py`
- Try different Whisper models for better accuracy
- Process multiple files in batch

## Need Help?

Check the main README.md for:
- Detailed installation instructions
- Configuration options
- Advanced usage examples
- Complete troubleshooting guide
