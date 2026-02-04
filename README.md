# faceless-youtube-farm

Automate the creation of calm, cinematic, faceless YouTube Shorts and Long videos from a CSV of ideas.

## Tech Stack
- Python 3.10+
- Gemini API (google-generativeai)
- FFmpeg (CLI)

## Folder Structure
```
faceless-youtube-farm/
  ideas/
    ideas.csv
  input/
    backgrounds/
    music/
    fonts/
  output/
    shorts/
    long/
    metadata/
  src/
  .env.example
  requirements.txt
```

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.
4. Add background videos, music, and fonts into `input/`.
5. Add ideas to `ideas/ideas.csv` (one sentence per idea).

## Usage
Generate Shorts:
```bash
python -m src.pipeline --mode shorts --channel default
```

Generate Long video from existing Shorts:
```bash
python -m src.pipeline --mode long --channel default
```

Generate both (Shorts first, then Long):
```bash
python -m src.pipeline --mode all --channel default
```

## Notes
- Shorts are exported to `output/shorts/`.
- Long videos are exported to `output/long/`.
- Generated metadata is stored in `output/metadata/` per channel.
- Ideas marked `done=true` in `ideas.csv` are skipped.
