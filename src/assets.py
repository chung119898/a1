from __future__ import annotations

import random
from pathlib import Path


class AssetPicker:
    def __init__(self, background_dir: str, music_dir: str, font_dir: str) -> None:
        self.background_dir = Path(background_dir)
        self.music_dir = Path(music_dir)
        self.font_dir = Path(font_dir)

    def pick_background(self) -> Path:
        return self._random_file(self.background_dir, ".mp4")

    def pick_music(self) -> Path:
        return self._random_file(self.music_dir, ".mp3")

    def pick_font(self) -> Path:
        return self._random_file(self.font_dir, ".ttf", ".otf")

    @staticmethod
    def _random_file(directory: Path, *suffixes: str) -> Path:
        if not directory.exists():
            raise FileNotFoundError(f"Missing directory: {directory}")
        files = [
            path
            for path in directory.iterdir()
            if path.is_file() and path.suffix.lower() in suffixes
        ]
        if not files:
            raise FileNotFoundError(f"No files with {suffixes} in {directory}")
        return random.choice(files)
