# -*- coding: utf-8 -*-

import urllib.request
import json
import ssl
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
VIDEO_URL = "https://r2.dev"
OUTPUT_PATH = PROJECT_DIR / "test_video.mp4"


def download_video(url: str):
    ssl._create_default_https_context = ssl._create_unverified_context

    print("Downloading video from open storage...")

    urllib.request.urlretrieve(url, OUTPUT_PATH)

    print("Download complete. Saved as test_video.mp4")


def generate_titles():
    print("Generating titles via Qwen...")

    prompt_text = (
        "Придумай 3 хайповых заголовка для Shorts "
        "про самые дорогие машины."
    )

    data = json.dumps({
        "model": "qwen2.5-coder:1.5b",
        "prompt": prompt_text,
        "stream": False
    }).encode("utf-8")

    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    print("\n--- РЕЗУЛЬТАТ ИИ ---")
    print(result["response"])
    print("--------------------")


if __name__ == "__main__":
     print("Skipping video download for pipeline test...")

     generate_titles()

     print("Pipeline complete.")