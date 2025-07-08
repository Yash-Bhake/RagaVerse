from __future__ import unicode_literals
import yt_dlp
import ffmpeg
import os
import sys
import subprocess
import logging
from pydub import AudioSegment
from tqdm import tqdm
import time

# ---------- Setup ----------
os.makedirs("downloads", exist_ok=True)
os.makedirs("trimmed", exist_ok=True)
os.makedirs("separated", exist_ok=True)

# Logging config
logging.basicConfig(
    filename='process.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# ---------- Step 1: Download from YouTube ----------
def download_from_url(url, name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'downloads/{name}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'noplaylist': True,
        'quiet': False,
        'ignoreerrors': True,
        'postprocessor_args': ['-ar', '44100'],
        'preferredquality': '192',
    }

    logging.info("[1/3] Downloading from YouTube...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            output_file = os.path.join("downloads", f"{name}.wav")

            if not os.path.exists(output_file) or os.path.getsize(output_file) < 1024:
                logging.error("Downloaded file is empty or too small.")
                sys.exit(1)

        with tqdm(total=100, desc="Downloading", unit="%", ncols=80) as pbar:
            for _ in range(30):
                time.sleep(0.03)
                pbar.update(2)
        logging.info(f"✅ Download complete: {output_file}")
        return output_file
    except Exception as e:
        logging.error(f"[ERROR] Download failed: {e}")
        sys.exit(1)

# ---------- Step 2: Trim Audio ----------
def trim_audio(input_path, start_sec, end_sec, name):
    try:
        logging.info("[2/3] Trimming audio...")
        with tqdm(total=100, desc="Trimming", ncols=80) as pbar:
            audio = AudioSegment.from_wav(input_path)
            trimmed = audio[start_sec * 1000:end_sec * 1000]
            output_path = os.path.join("trimmed", f"{name}_trimmed.wav")
            trimmed.export(output_path, format="wav")
            for _ in range(25):
                time.sleep(0.01)
                pbar.update(4)
        logging.info(f"✅ Trimmed audio saved: {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"[ERROR] Trimming failed: {e}")
        sys.exit(1)

# ---------- Step 3: Run Demucs ----------
def separate_audio(audio_path, name):
    try:
        logging.info("[3/3] Running Demucs for source separation...")
        with tqdm(total=100, desc="Separating", ncols=80) as pbar:
            command = [
                "demucs", audio_path,
                "--out", "separated",
                "--two-stems", "vocals"
            ]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for _ in range(50):
                time.sleep(0.2)
                pbar.update(2)

            stdout, stderr = process.communicate()

            if process.returncode != 0:
                logging.error(f"[ERROR] Demucs failed:\n{stderr.decode()}")
                sys.exit(1)

        vocals_dir = os.path.join("separated", "vocals")
        no_vocals_dir = os.path.join("separated", "no_vocals")
        os.makedirs(vocals_dir, exist_ok=True)
        os.makedirs(no_vocals_dir, exist_ok=True)

        vocals_path = os.path.join(vocals_dir, os.path.splitext(os.path.basename(audio_path))[0], "vocals.wav")
        no_vocals_path = os.path.join(no_vocals_dir, os.path.splitext(os.path.basename(audio_path))[0], "no_vocals.wav")

        if os.path.exists(vocals_path):
            new_vocals_path = os.path.join(vocals_dir, f"{name}_vocals.wav")
            os.replace(vocals_path, new_vocals_path)
            logging.info(f"✅ Vocals: {new_vocals_path}")
        if os.path.exists(no_vocals_path):
            new_nv_path = os.path.join(no_vocals_dir, f"{name}_no_vocals.wav")
            os.replace(no_vocals_path, new_nv_path)
            logging.info(f"✅ Accompaniment: {new_nv_path}")
    except Exception as e:
        logging.error(f"[ERROR] Demucs separation failed: {e}")
        sys.exit(1)

# ---------- Main ----------
def main():
    if len(sys.argv) != 3:
        print("Usage: python youtube_to_stems.py <YouTube URL> <output_name>")
        sys.exit(1)

    url = sys.argv[1]
    name = sys.argv[2]

    try:
        start = int(input("Start time (in seconds): "))
        end = int(input("End time (in seconds): "))
        if start < 0 or end <= start:
            raise ValueError
    except ValueError:
        logging.error("[ERROR] Invalid time inputs. Start must be >= 0 and End > Start.")
        sys.exit(1)

    wav_path = download_from_url(url, name)
    trimmed_path = trim_audio(wav_path, start, end, name)
    separate_audio(trimmed_path, name)

    logging.info("🎉 All done! Check the 'separated' folder for outputs.")

if __name__ == "__main__":
    main()
