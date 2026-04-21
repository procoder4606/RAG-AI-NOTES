
````md
# 🎥 Video/Audio Transcription & Notes Generator

An automated pipeline that extracts audio transcripts and on-screen text (OCR) from videos/audio files, then generates structured AI-powered notes.

---

## ✨ Features

- 🎤 **Audio Transcription** using OpenAI Whisper (high-accuracy speech-to-text)
- 🎥 **OCR Extraction** from video frames (on-screen text detection)
- 🤖 **AI-Powered Notes Generation** (OpenRouter / Gemini / OpenAI)
- 📝 **Markdown Output** for clean, structured notes
- ⚡ Works with both video and audio files

---

## 🧰 Prerequisites

### 1. FFmpeg (Required)

#### Windows
```bash
choco install ffmpeg
````

Or download: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

#### macOS

```bash
brew install ffmpeg
```

#### Linux

```bash
sudo apt update
sudo apt install ffmpeg
```

---

### 2. Tesseract OCR

#### Windows

* Download: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
* Add to PATH

#### macOS

```bash
brew install tesseract
```

#### Linux

```bash
sudo apt install tesseract-ocr
```

---

## 🚀 Installation

### Step 1: Go to Project Folder

```bash
cd SEM_8_PROJECT
```

---

### Step 2: Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 API Configuration

You can use:

* OpenRouter (Recommended) → [https://openrouter.ai/](https://openrouter.ai/)
* Gemini → [https://makersuite.google.com/](https://makersuite.google.com/)
* OpenAI → [https://platform.openai.com/](https://platform.openai.com/)

---

### Set Environment Variables

#### Windows (PowerShell)

```bash
$env:AI_PROVIDER="openrouter"
$env:OPENROUTER_API_KEY="your-api-key"
```

#### macOS/Linux

```bash
export AI_PROVIDER="openrouter"
export OPENROUTER_API_KEY="your-api-key"
```

---

### OR use `.env` file (Recommended)

```env
AI_PROVIDER=openrouter
OPENROUTER_API_KEY=your-api-key
```

Install:

```bash
pip install python-dotenv
```

Add in `main.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## ▶️ Usage

### Run with Video

```bash
python main.py path/to/video.mp4
```

### Run with Audio

```bash
python main.py path/to/audio.mp3
```

---

## 📂 Supported Formats

### Video

* .mp4
* .mkv
* .mov
* .avi

### Audio

* .mp3
* .wav
* .m4a
* .flac
* .ogg

---

## 📄 Output

Generated notes are saved as:

```
notes.txt
```

---

## ⚙️ How It Works

1. Detects file type (audio/video)
2. Extracts OCR text from video frames
3. Transcribes audio using Whisper
4. Combines text + transcript
5. Sends to AI for structured notes
6. Saves final output

---

## 🛠️ Customization

### Change OCR Interval

```python
interval_sec = 10
```

### Change Whisper Model

```python
whisper.load_model("base")
```

Options:

* tiny
* base
* small
* medium
* large

---

## 🧯 Troubleshooting

### FFmpeg not found

* Install FFmpeg and restart terminal

### Tesseract error

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Torch error

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

---

## 🚀 Deactivate Environment

```bash
deactivate
```

---

## 📜 License

For educational and personal use.

---

## 🙏 Credits

* OpenAI Whisper
* Tesseract OCR
* OpenCV
* OpenRouter / Gemini / OpenAI

```

