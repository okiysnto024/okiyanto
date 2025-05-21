import whisper
from openai import OpenAI
from utils import download_audio, download_video_segment

def process_video(url):
    audio_file = download_audio(url)

    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    transcript = result['text']

    prompt = f"""Berikut transkrip video YouTube. Tunjukkan 2-3 bagian penting (highlight) dengan timestamp (HH:MM:SS - HH:MM:SS).

Transkrip:
{transcript}"""
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    highlights = extract_timestamps(response.choices[0].message.content)

    for i, h in enumerate(highlights):
        download_video_segment(url, h["start"], h["end"], f"highlight_{i+1}.mp4")

    return highlights

def extract_timestamps(text):
    import re
    matches = re.findall(r'(\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2})', text)
    return [{"start": m[0], "end": m[1]} for m in matches]
