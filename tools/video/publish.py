"""Check rendered week videos and add them to the site.

Usage:
    python tools/video/publish.py 3          (or several: 1 2 3)

For each week: checks tools/video/.build/week-N/week-0N.mp4 (decodes without warnings, audio and
video end together, under 15 MB), copies it to public/videos/, makes a poster from the title
slide, and records it in data/videos.json. Commit and push to put it live.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VIDEOS_JSON = ROOT / "data" / "videos.json"


def stream_end(path, stream):
    log = subprocess.run([FFMPEG, "-i", str(path), "-map", stream, "-f", "null", "-"], capture_output=True, text=True).stderr
    h, m, s = re.findall(r"time=(\d+):(\d+):([\d.]+)", log)[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


def publish(week):
    nn = f"{week:02d}"
    src = HERE / ".build" / f"week-{week}" / f"week-{nn}.mp4"
    if not src.exists():
        raise SystemExit(f"{src} not found; render it first: python tools/video/render.py {week}")
    warnings = subprocess.run([FFMPEG, "-v", "warning", "-i", str(src), "-f", "null", "-"], capture_output=True, text=True).stderr.strip()
    if warnings:
        raise SystemExit(f"week {week}: decode warnings:\n{warnings}")
    v, a = stream_end(src, "0:v"), stream_end(src, "0:a")
    if abs(v - a) > 0.1:
        raise SystemExit(f"week {week}: audio ends at {a:.2f}s but video at {v:.2f}s")
    size = src.stat().st_size
    if size > 15e6:
        raise SystemExit(f"week {week}: {size / 1e6:.1f} MB is over the 15 MB limit")

    out = ROOT / "public" / "videos"
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out / f"week-{nn}.mp4")
    subprocess.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(HERE / ".build" / f"week-{week}" / "frames" / "s0_k0.png"),
                    "-vf", "scale=960:-2", "-q:v", "4", str(out / f"week-{nn}.jpg")], check=True)

    duration = f"{int(v) // 60}:{int(v) % 60:02d}"
    videos = [x for x in json.loads(VIDEOS_JSON.read_text(encoding="utf-8")) if x["week"] != week]
    videos.append({"week": week, "file": f"videos/week-{nn}.mp4", "poster": f"videos/week-{nn}.jpg", "duration": duration})
    VIDEOS_JSON.write_text(json.dumps(sorted(videos, key=lambda x: x["week"]), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"week {week}: {duration}, {size / 1e6:.2f} MB, audio/video end {v:.2f}/{a:.2f} s — added to public/videos and data/videos.json")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        publish(int(arg))
    print("Now build and check: python tools/check.py && python tools/build.py")
