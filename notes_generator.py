"""
Notes generation module using AI APIs (OpenRouter, Gemini, OpenAI)
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# =========================
# 🔹 OpenRouter
# =========================
def generate_notes_openrouter(content):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "AI Notes Generator"
    }

    prompt = f"""
Convert the following content into clean structured study notes:

- Use headings
- Use bullet points
- Remove repetition
- Keep it concise

Content:
{content[:8000]}
"""

    data = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data, timeout=15)

    if response.status_code != 200:
        print("OpenRouter ERROR:", response.text)
        response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]


# =========================
# 🔹 Gemini
# =========================
def generate_notes_gemini(content):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"

    prompt = f"""
Convert the following content into structured study notes:

- Use headings
- Use bullet points
- Remove noise

Content:
{content[:8000]}
"""

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, json=data, timeout=15)

    if response.status_code != 200:
        print("Gemini ERROR:", response.text)
        response.raise_for_status()

    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]


# =========================
# 🔹 OpenAI
# =========================
def generate_notes_openai(content):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Convert the following content into structured study notes:

- Use headings
- Use bullet points
- Remove repetition

Content:
{content[:8000]}
"""

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data, timeout=15)

    if response.status_code != 200:
        print("OpenAI ERROR:", response.text)
        response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]


# =========================
# 🔹 Main Dispatcher
# =========================
def generate_notes(content):
    provider = os.getenv("AI_PROVIDER", "openrouter").lower()

    print(f"Generating notes using {provider}...")

    try:
        if provider == "openrouter":
            return generate_notes_openrouter(content)

        elif provider == "gemini":
            return generate_notes_gemini(content)

        elif provider == "openai":
            return generate_notes_openai(content)

        else:
            raise ValueError(f"Unknown AI provider: {provider}")

    except Exception as e:
        print(f"Error generating notes: {e}")
        return f"# Notes (Generated Manually)\n\n{content}"