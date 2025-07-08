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

```bash 
pip install yt-dlp librosa numpy matplotlib seaborn scikit-learn tqdm pydub
```

## CLI tool

1. Conversion of youtube video to .wav file
2. Trimming audio - start time to end time
3. Source separation - yields 2 files- vocals and no_vocals

```bash
python youtube_to_stem.py "youtube_link" name
```

then followed by start time and end time 