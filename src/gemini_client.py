from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Any

import google.generativeai as genai


@dataclass
class GeminiResponse:
    overlay_text: str
    title: str
    description: str
    tags: list[str]


class GeminiClient:
    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def generate_metadata(self, idea: str, avoid_phrases: set[str]) -> GeminiResponse:
        randomness_hint = random.choice(
            [
                "Use a poetic, cinematic tone.",
                "Keep it minimal and calm.",
                "Use gentle imagery and subtle phrasing.",
            ]
        )
        prompt = (
            "You are generating metadata for a faceless YouTube video. "
            "Return STRICT JSON only with fields: overlay_text, title, description, tags. "
            "overlay_text must be <= 18 words. title must be < 60 characters. "
            "description must be one sentence. tags must be an array of strings. "
            f"Idea: {idea} "
            f"Avoid using any of these phrases exactly: {sorted(avoid_phrases)}. "
            f"{randomness_hint}"
        )
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 1.1,
                "top_p": 0.9,
                "max_output_tokens": 300,
                "response_mime_type": "application/json",
            },
        )
        return self._parse_response(response.text)

    @staticmethod
    def _parse_response(text: str) -> GeminiResponse:
        data: dict[str, Any] = json.loads(text)
        return GeminiResponse(
            overlay_text=data["overlay_text"].strip(),
            title=data["title"].strip(),
            description=data["description"].strip(),
            tags=list(data["tags"]),
        )
