from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

from src.ffmpeg import FFmpegRenderer
from src.utils import ensure_dir


@dataclass
class LongResult:
    shorts: list[Path]
    output_path: Path


class LongPipeline:
    def __init__(
        self,
        channel: str,
        renderer: FFmpegRenderer,
        output_dir: Path,
        min_shorts: int,
        max_shorts: int,
    ) -> None:
        self.channel = channel
        self.renderer = renderer
        self.output_dir = output_dir
        self.min_shorts = min_shorts
        self.max_shorts = max_shorts

    def run(self) -> LongResult | None:
        shorts_dir = self.output_dir / "shorts" / self.channel
        ensure_dir(shorts_dir)
        shorts = sorted(shorts_dir.glob("*.mp4"))
        if len(shorts) < self.min_shorts:
            return None
        count = random.randint(self.min_shorts, min(self.max_shorts, len(shorts)))
        selected = random.sample(shorts, count)
        output_path = self.output_dir / "long" / self.channel / "long_video.mp4"
        self.renderer.render_long(selected, output_path)
        return LongResult(shorts=selected, output_path=output_path)
