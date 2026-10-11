# -*- coding: utf-8 -*-
import os
import glob
import ollama
import whisper
from pathlib import Path
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

# ЖЕСТКИЙ АВТО-ПОИСК: берем первую строку пути из списка glob
magick_paths = glob.glob(r"C:\Program Files\ImageMagick-*\magick.exe")
if magick_paths:
    # Берем самый первый элемент [0] и превращаем в чистую строку!
    magick_file = magick_paths[0]
    print(f"\n[SYSTEM] Found ImageMagick binary automatically at: {magick_file}")
    change_settings({"IMAGEMAGICK_BINARY": magick_file})
else:
    print("\n[SYSTEM] WARNING: magick.exe not found via auto-search!")

PROJECT_DIR = Path(__file__).resolve().parent.parent
input_path = str(PROJECT_DIR / "test_video.mp4")
output_path = str(PROJECT_DIR / "super_final_shorts.mp4")

def generate_subtitles_data():
    print("\n[AI] Waking up Whisper neural network for speech recognition...")
    if not os.path.exists(input_path):
        return []
    
    try:
        model = whisper.load_model("tiny", device="cpu")
        print("[AI] Listening to video and extracting text timestamps...")
        result = model.transcribe(input_path)
        return result.get("segments", [])
    except Exception as e:
        print(f"\nWhisper AI Error: {e}")
        return []

def process_video_with_subtitles(segments, start_time=5, end_time=25):
    print(f"\nStarting MoviePy video processing with embedded subtitles (Trim: {start_time}s to {end_time}s)...")
    try:
        full_clip = VideoFileClip(input_path)
        shorts_clip = full_clip.subclip(start_time, end_time)
        
        video_w, video_h = shorts_clip.size
        txt_clips = []
        
        print("Embedding text clips onto the video timeline...")
        for segment in segments:
            seg_start = segment["start"] - start_time
            seg_end = segment["end"] - start_time
            text = segment["text"].strip()
            
            if seg_end > 0 and seg_start < (end_time - start_time):
                clip_start = max(0, seg_start)
                clip_end = min(end_time - start_time, seg_end)
                
                # Генерируем красивый сочный текст
                txt_clip = TextClip(
                    text, 
                    fontsize=40, 
                    color='yellow', 
                    font='Arial',
                    stroke_color='black',
                    stroke_width=2,
                    method='caption',
                    size=(video_w - 40, None)
                )
                txt_clip = txt_clip.set_start(clip_start).set_end(clip_end).set_position(('center', 'center'))
                txt_clips.append(txt_clip)
        
        # Соединяем видео и титры в один поток
        final_clip = CompositeVideoClip([shorts_clip] + txt_clips)
        
        print("Re-encoding video to H.264 with AAC audio and hardcoded subtitles...")
        final_clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            audio_bitrate="192k",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )
        
        final_clip.close()
        full_clip.close()
        print("\nMoviePy processing complete! super_final_shorts.mp4 with EMBEDDED SUBTITLES created!")
    except Exception as e:
        print(f"\nMoviePy processing error: {e}")

if __name__ == "__main__":
    if os.path.exists(input_path):
        segments_data = generate_subtitles_data()
        process_video_with_subtitles(segments_data, start_time=5, end_time=25)
    else:
        print(f"Error: {input_path} not found! Please download the video first via yt-dlp.")
    
    print("\nGenerating titles via Qwen...")
    prompt_text = "Придумай 3 хайповых заголовка для Shorts про самые дорогие машины."
    try:
        result = ollama.generate(model="qwen2.5-coder:1.5b", prompt=prompt_text)
        print("\n--- РЕЗУЛЬТАТ ИИ ---")
        print(result["response"])
        print("--------------------")
    except Exception as e:
        print(f"\nOllama note: {e}")
    print("Pipeline complete.")