from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    ideas_csv: str
    background_dir: str
    music_dir: str
    font_dir: str
    output_dir: str
    short_duration: int
    long_min_shorts: int
    long_max_shorts: int

    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            ideas_csv=os.getenv("IDEAS_CSV", "ideas/ideas.csv"),
            background_dir=os.getenv("BACKGROUND_DIR", "input/backgrounds"),
            music_dir=os.getenv("MUSIC_DIR", "input/music"),
            font_dir=os.getenv("FONT_DIR", "input/fonts"),
            output_dir=os.getenv("OUTPUT_DIR", "output"),
            short_duration=int(os.getenv("SHORT_DURATION", "15")),
            long_min_shorts=int(os.getenv("LONG_MIN_SHORTS", "5")),
            long_max_shorts=int(os.getenv("LONG_MAX_SHORTS", "7")),
        )
