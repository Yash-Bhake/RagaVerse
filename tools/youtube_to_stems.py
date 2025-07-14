from __future__ import unicode_literals
import yt_dlp
import librosa
import soundfile as sf
import os
import sys
import subprocess
import logging
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
            y, sr = librosa.load(input_path, sr=None)
            start_sample = int(start_sec * sr)
            end_sample = int(end_sec * sr)
            trimmed = y[start_sample:end_sample]
            output_path = os.path.join("trimmed", f"{name}_trimmed.wav")
            sf.write(output_path, trimmed, sr)
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
        logging.info("[3/3] Running Demucs...")
        subprocess.run(
            ["demucs", audio_path, "--out", "separated", "--two-stems", "vocals"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        model_dir = next(d for d in os.listdir("separated") if os.path.isdir(os.path.join("separated", d)) and d != "vocals" and d != "no_vocals")
        base = os.path.splitext(os.path.basename(audio_path))[0]
        out_dir = os.path.join("separated", model_dir, base)

        os.makedirs("separated/vocals", exist_ok=True)
        os.makedirs("separated/no_vocals", exist_ok=True)

        os.replace(os.path.join(out_dir, "vocals.wav"), f"separated/vocals/{name}_vocals.wav")
        os.replace(os.path.join(out_dir, "no_vocals.wav"), f"separated/no_vocals/{name}_no_vocals.wav")

        import shutil
        shutil.rmtree(os.path.join("separated", model_dir))

        logging.info(f"✅ Saved: separated/vocals/{name}_vocals.wav")
        logging.info(f"✅ Saved: separated/no_vocals/{name}_no_vocals.wav")

    except Exception as e:
        logging.error(f"[ERROR] Demucs failed: {e}")
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
