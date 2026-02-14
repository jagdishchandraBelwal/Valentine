# =============================================================================
#   Desi Comedy YouTube Shorts Generator - WORKING VERSION (Feb 2026)
#   For jagdish - Delhi grind - Human feel, no ImageMagick
# =============================================================================

import os
import random
import requests
import numpy as np
from datetime import datetime
from io import BytesIO

# MoviePy
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip,
    ColorClip
)
from moviepy.video.fx.all import crop, resize

# TTS + Pillow for text
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

# Your Groq key
GROQ_API_KEY = "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"

OUTPUT_FOLDER = "desi_shorts_feb2026"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ──────────────────────────────────────────────
#   Generate funny script with Groq
# ──────────────────────────────────────────────

def generate_script():
    topics = [
        "Budget 2026 sunke middle class dad ka reaction",
        "February ke thand mein subah uthna Delhi wala struggle",
        "Valentine's Day single logon ki tragedy",
        "Maha Shivratri vrat fail funny moments",
        "Petrol price badhne ke baad bike rider ki halat",
        "Mom ka har cheez pe 'budget tight hai beta'",
        "February mein board exam padhai be like",
        "Rishtedaar budget advice dene lage",
        "Delhi February smog + thand combo",
        "Naya mahina shuru, purani pareshaniyaan same"
    ]
    
    topic = random.choice(topics)
    
    prompt = f"""\
Write a very short 20-30 second YouTube Short comedy script in casual Hinglish.
Topic: {topic}

Rules:
- First line strong funny hook (3 seconds)
- 4-6 lines total only
- Very desi relatable Delhi style language
- Include actions in [brackets]
- End with punchline

Format exactly like this:

HOOK: [action] "dialogue"
LINE1: [action] "dialogue"
LINE2: [action] "dialogue"
...
PUNCH: [action] "final funny line"
"""
    
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9,
            "max_tokens": 350
        }
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"].strip()
        
        print(f"\nTopic: {topic}\n\n{text}\n")
        return topic, text
    except Exception as e:
        print(f"Groq error: {e}")
        return None, None

# ──────────────────────────────────────────────
#   Download stock clip (optional - no key needed)
# ──────────────────────────────────────────────

def download_funny_clip(keyword="funny indian reaction"):
    # Using direct public links fallback (no API key needed for basic use)
    print("Trying to find stock clip...")
    return None  # For now fallback to color bg (add Pexels later if you want)

# ──────────────────────────────────────────────
#   Create short video - FIXED & WORKING
# ──────────────────────────────────────────────

def make_short(topic, script_text):
    if not script_text:
        return None

    lines = [l.strip() for l in script_text.split('\n') if l.strip() and ':' in l]
    if not lines:
        return None

    # Voiceover - save to disk (fixes BytesIO bug)
    voice_text = " ".join([l.split(":",1)[1].strip().strip('"') for l in lines])
    voice_file = "temp_voice.mp3"
    try:
        tts = gTTS(voice_text, lang='hi', tld='co.in')
        tts.save(voice_file)
        audio = AudioFileClip(voice_file)
        duration = audio.duration + 2
    except Exception as e:
        print(f"TTS failed: {e} → silent video")
        audio = None
        duration = 25

    # Base clip - color fallback (no stock for now)
    clip = ColorClip((1080, 1920), color=(20, 30, 50), duration=duration)

    if audio:
        clip = clip.set_audio(audio)

    # Animated text overlays using Pillow + numpy
    composites = [clip]
    current_time = 0.5
    
    try:
        font = ImageFont.truetype("arialbd.ttf", 80)  # Windows default bold
    except:
        font = ImageFont.load_default()

    for line in lines:
        if ':' not in line:
            continue
        _, txt = line.split(":", 1)
        text = txt.strip().strip('"').strip()
        if not text:
            continue

        # Create text image with Pillow
        img = Image.new('RGBA', (1000, 200), (0, 0, 0, 160))  # semi-transparent bg
        draw = ImageDraw.Draw(img)
        draw.text((30, 40), text, font=font, fill='yellow', stroke_width=5, stroke_fill='black')

        # Convert to numpy array for MoviePy
        img_np = np.array(img)

        txt_clip = ImageClip(img_np).set_duration(4.5).set_start(current_time).set_position('center')

        composites.append(txt_clip)
        current_time += 5

    final = CompositeVideoClip(composites)

    # Save file
    safe_name = "".join(c for c in topic if c.isalnum() or c in " -_")[:40]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_FOLDER}/{safe_name}_{timestamp}.mp4"
    
    print(f"Rendering video → {filename}")
    final.write_videofile(
        filename,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=4,
        verbose=False,
        logger=None
    )
    
    # Cleanup
    if os.path.exists(voice_file):
        os.remove(voice_file)
    
    print(f"DONE → {filename}\n")
    return filename

# ──────────────────────────────────────────────
#   MAIN - run 3 shorts (change count to make more)
# ──────────────────────────────────────────────

def main(count=3):
    print("=== Desi Comedy Shorts Generator - WORKING VERSION ===\n")
    print(f"Output folder: {os.path.abspath(OUTPUT_FOLDER)}\n")
    print("Starting...\n")
    
    for i in range(1, count + 1):
        print(f"Short #{i}/{count}")
        print("-" * 60)
        topic, script = generate_script()
        if script:
            make_short(topic, script)
    
    print("\nAll shorts created! Open folder → play videos → upload to YouTube Shorts!")
    print("Folder location:", os.path.abspath(OUTPUT_FOLDER))

if __name__ == "__main__":
    main(count=3)  # ← change to 5, 10, 20 whatever you want