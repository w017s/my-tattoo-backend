import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from io import BytesIO
import uuid
from backend.styles import mandala, polarwave, abstractflow, minimalist, ai_style

IMAGE_FOLDER = 'backend/static/images'


# 音频预处理，转换成 WAV 格式
def process_audio(audio_path):
    if audio_path.endswith(".mp3") or audio_path.endswith(".m4a"):
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_channels(1).set_frame_rate(22050)  # 单声道, 22050Hz
        output_path = os.path.splitext(audio_path)[0] + '.wav'
        audio.export(output_path, format='wav')
        return output_path
    return audio_path


# 根据不同风格生成图案
def generate_patterns(audio_path):
    wav_path = process_audio(audio_path)
    y, sr = librosa.load(wav_path, sr=22050)  # 加载音频

    pattern_urls = []
    unique_id = str(uuid.uuid4())

    # 生成五种不同风格的图案
    patterns = {
        "mandala": mandala.create_mandala(y, sr),
        "polarwave": polarwave.create_polarwave(y, sr),
        "abstractflow": abstractflow.create_abstractflow(y, sr),
        "minimalist": minimalist.create_minimalist(y, sr),
        "ai_style": ai_style.create_ai_style(y, sr)
    }

    # 保存图案并生成链接
    for style, pattern in patterns.items():
        pattern_filename = f"{style}_{unique_id}.png"
        pattern_path = os.path.join(IMAGE_FOLDER, pattern_filename)
        pattern.save(pattern_path)
        pattern_urls.append(f"/static/images/{pattern_filename}")

    return pattern_urls
