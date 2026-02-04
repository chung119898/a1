from __future__ import annotations

import random
from dataclasses import dataclass
import json
from pathlib import Path

from src.assets import AssetPicker
from src.ffmpeg import FFmpegRenderer
from src.gemini_client import GeminiClient, GeminiResponse
from src.idea_store import IdeaStore
from src.utils import ensure_dir, save_json, slugify


@dataclass
class ShortResult:
    idea: str
    output_path: Path
    metadata: GeminiResponse


class ShortsPipeline:
    def __init__(
        self,
        channel: str,
        idea_store: IdeaStore,
        asset_picker: AssetPicker,
        gemini: GeminiClient,
        renderer: FFmpegRenderer,
        output_dir: Path,
        duration: int,
    ) -> None:
        self.channel = channel
        self.idea_store = idea_store
        self.asset_picker = asset_picker
        self.gemini = gemini
        self.renderer = renderer
        self.output_dir = output_dir
        self.duration = duration
        self.metadata_dir = output_dir / "metadata" / channel
        ensure_dir(self.metadata_dir)

    def run(self) -> list[ShortResult]:
        results: list[ShortResult] = []
        ideas = [idea for idea in self.idea_store.load() if not idea.done]
        random.shuffle(ideas)
        seen_phrases = self._load_seen_phrases()

        for idea in ideas:
            metadata = self._generate_unique_metadata(idea.text, seen_phrases)
            background = self.asset_picker.pick_background()
            music = self.asset_picker.pick_music()
            font = self.asset_picker.pick_font()

            slug = slugify(idea.text)
            output_path = self.output_dir / "shorts" / self.channel / f"{slug}.mp4"
            self.renderer.render_short(
                background=background,
                music=music,
                font=font,
                overlay_text=metadata.overlay_text,
                duration=self.duration,
                output_path=output_path,
            )

            metadata_path = self.metadata_dir / f"{slug}.json"
            save_json(
                metadata_path,
                {
                    "idea": idea.text,
                    "overlay_text": metadata.overlay_text,
                    "title": metadata.title,
                    "description": metadata.description,
                    "tags": metadata.tags,
                    "background": background.as_posix(),
                    "music": music.as_posix(),
                    "font": font.as_posix(),
                    "output": output_path.as_posix(),
                },
            )
            self.idea_store.mark_done(idea.text)
            seen_phrases.update(
                {metadata.overlay_text.lower(), metadata.title.lower(), metadata.description.lower()}
            )
            results.append(ShortResult(idea=idea.text, output_path=output_path, metadata=metadata))
        return results

    def _generate_unique_metadata(self, idea: str, seen_phrases: set[str]) -> GeminiResponse:
        for _ in range(4):
            metadata = self.gemini.generate_metadata(idea, seen_phrases)
            candidates = {
                metadata.overlay_text.lower(),
                metadata.title.lower(),
                metadata.description.lower(),
            }
            if not candidates & seen_phrases:
                return metadata
        return metadata

    def _load_seen_phrases(self) -> set[str]:
        phrases: set[str] = set()
        for path in self.metadata_dir.glob("*.json"):
            try:
                data = path.read_text(encoding="utf-8")
                payload = json.loads(data)
            except (ValueError, OSError):
                continue
            for key in ("overlay_text", "title", "description"):
                value = (payload.get(key) or "").strip()
                if value:
                    phrases.add(value.lower())
        return phrases
