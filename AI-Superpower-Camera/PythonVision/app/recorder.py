from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Optional


class FFmpegRecorder:
    def __init__(self, ffmpeg_path: str, output_dir: str, fps: int, resolution: str):
        self.ffmpeg_path = ffmpeg_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.fps = fps
        self.resolution = resolution
        self.proc: Optional[subprocess.Popen] = None
        self.output_file: Optional[str] = None

    def start(self, source_device: str = "0") -> str:
        ts = time.strftime("%Y%m%d-%H%M%S")
        self.output_file = str(self.output_dir / f"capture-{ts}.mp4")

        cmd = [
            self.ffmpeg_path,
            "-y",
            "-f",
            "v4l2",
            "-i",
            source_device,
            "-r",
            str(self.fps),
            "-s",
            self.resolution,
            "-c:v",
            "libx264",
            self.output_file,
        ]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return self.output_file

    def stop(self) -> Optional[str]:
        if self.proc is None:
            return None
        self.proc.terminate()
        self.proc.wait(timeout=5)
        self.proc = None
        return self.output_file
