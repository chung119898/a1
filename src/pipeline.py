from __future__ import annotations

import argparse
from pathlib import Path

from src.assets import AssetPicker
from src.config import Settings
from src.ffmpeg import FFmpegRenderer
from src.gemini_client import GeminiClient
from src.idea_store import IdeaStore
from src.long import LongPipeline
from src.shorts import ShortsPipeline
from src.utils import ensure_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Faceless YouTube content farm")
    parser.add_argument("--mode", choices=["shorts", "long", "all"], required=True)
    parser.add_argument("--channel", required=True, help="Channel slug for multi-channel usage")
    return parser


def run_shorts(settings: Settings, channel: str) -> None:
    idea_store = IdeaStore(settings.ideas_csv)
    asset_picker = AssetPicker(
        settings.background_dir, settings.music_dir, settings.font_dir
    )
    renderer = FFmpegRenderer(settings.output_dir)
    gemini = GeminiClient(settings.gemini_api_key)
    pipeline = ShortsPipeline(
        channel=channel,
        idea_store=idea_store,
        asset_picker=asset_picker,
        gemini=gemini,
        renderer=renderer,
        output_dir=Path(settings.output_dir),
        duration=settings.short_duration,
    )
    pipeline.run()


def run_long(settings: Settings, channel: str) -> None:
    renderer = FFmpegRenderer(settings.output_dir)
    pipeline = LongPipeline(
        channel=channel,
        renderer=renderer,
        output_dir=Path(settings.output_dir),
        min_shorts=settings.long_min_shorts,
        max_shorts=settings.long_max_shorts,
    )
    pipeline.run()


def main() -> None:
    settings = Settings.from_env()
    ensure_dir(Path(settings.output_dir))
    parser = build_parser()
    args = parser.parse_args()

    if args.mode in {"shorts", "all"}:
        run_shorts(settings, args.channel)
    if args.mode in {"long", "all"}:
        run_long(settings, args.channel)


if __name__ == "__main__":
    main()
