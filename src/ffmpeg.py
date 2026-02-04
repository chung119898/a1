from __future__ import annotations

import subprocess
from pathlib import Path


class FFmpegRenderer:
    def __init__(self, output_dir: str) -> None:
        self.output_dir = Path(output_dir)

    def render_short(
        self,
        background: Path,
        music: Path,
        font: Path,
        overlay_text: str,
        duration: int,
        output_path: Path,
    ) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        drawtext = (
            "drawtext="
            f"fontfile='{font.as_posix()}':"
            f"text='{overlay_text}':"
            "fontsize=64:fontcolor=white:"
            "x=(w-text_w)/2:y=(h-text_h)/2:"
            "shadowcolor=black:shadowx=2:shadowy=2:"
            "line_spacing=10"
        )
        video_filter = (
            "scale=1080:1920,"
            "zoompan=z='min(zoom+0.0005,1.08)':"
            "x='iw/2-(iw/zoom/2)':"
            "y='ih/2-(ih/zoom/2)':"
            f"d={duration * 30}:s=1080x1920,"
            "fade=t=in:st=0:d=0.6,"
            f"fade=t=out:st={max(duration - 1, 1)}:d=0.8,"
            f"{drawtext}"
        )
        audio_filter = (
            "[1:a]volume=0.25,"
            "afade=t=in:st=0:d=1,"
            f"afade=t=out:st={max(duration - 1, 1)}:d=1"
        )
        command = [
            "ffmpeg",
            "-y",
            "-stream_loop",
            "-1",
            "-i",
            background.as_posix(),
            "-stream_loop",
            "-1",
            "-i",
            music.as_posix(),
            "-t",
            str(duration),
            "-filter_complex",
            f"[0:v]{video_filter}[v];{audio_filter}[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-r",
            "30",
            "-s",
            "1080x1920",
            "-shortest",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "20",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            output_path.as_posix(),
        ]
        self._run(command)

    def render_long(self, shorts: list[Path], output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        list_file = output_path.parent / "concat_list.txt"
        list_file.write_text(
            "\n".join([f"file '{short.as_posix()}'" for short in shorts]),
            encoding="utf-8",
        )
        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            list_file.as_posix(),
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            output_path.as_posix(),
        ]
        self._run(command)
        list_file.unlink(missing_ok=True)

    @staticmethod
    def _run(command: list[str]) -> None:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
