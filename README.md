# 🎵 RagaVerse

This project enables the analysis and clustering of Indian classical ragas, and other pieces based on them, intending to reveal interesting correlations that might not be evident beforehand. The process follows audio pre-processing, computing pitch-based features, and visualisation using dimensionality reduction techniques.

---

##  Repository Structure for preprocessing

under the tools folder- 

```bash
├── downloads/           # Raw audio downloaded from YouTube
├── trimmed/             # Trimmed audio segments
├── separated/
│   ├── vocals/          # Source-separated vocal files
│   └── no_vocals/       # Source-separated accompaniment files
├── youtube_to_stems.py  # CLI tool to process YouTube audio
```

## Requirements

Mac OS

1. install homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. install ffmpeg

```bash
brew install ffmpeg
```
3. clone this repository
```bash
git clone https://github.com/Yash-Bhake/RagaVerse.git
```
4. install python3.10 (if not present)
```bash
brew install python@3.10
```
5. create virtual environment 
```bash
python3.10 -m venv ragaverse_venv
source ragaverse_venv/bin/activate
```
6. install dependencies
```bash 
pip install yt-dlp librosa ffmpeg-python soundfile numpy matplotlib seaborn scikit-learn tqdm openpyxl
```

Windows

1. Download ffmpeg from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system environment variables -> path
4. clone this repository
```bash
git clone https://github.com/Yash-Bhake/RagaVerse.git
```
5. install python 3.10 from https://www.python.org/downloads/release/python-3100/ and add it to your path (if not present)
6. create virtual environment (optional but recommended)
```bash
python3.10 -m venv ragaverse_venv
ragaverse_venv\Scripts\activate
```
7. install dependencies
```bash 
pip install yt-dlp librosa ffmpeg-python soundfile numpy matplotlib seaborn scikit-learn tqdm openpyxl
```

## CLI tool

1. Conversion of youtube video to .wav file
2. Trimming audio - start time to end time
3. Source separation - yields 2 files- vocals and no_vocals

```bash
cd tools
python youtube_to_stem.py "youtube_link" name
```

Enter start and end time on entering
