"""Shared by render.py and preview.py: load a week's script and photograph its slides.

Slides are drawn by slides.html in headless Chrome at 1280×720. The week's content is passed in a
small JS data file (one per week, so several weeks can be rendered side by side).
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE / ".build"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SLIDES = HERE / "slides.html"

# Spoken text uses spaced-out letters so the voice reads them right; captions show the written form.
CAPTION_FIXES = {"E C 2": "EC2"}


def week_dir(week):
    path = BUILD / f"week-{week}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_week(week):
    """Import tools/video/scripts/week<N>.py and return its VIDEO dict."""
    sys.path.insert(0, str(HERE))   # so the script can `from vidkit import …`
    path = HERE / "scripts" / f"week{week}.py"
    spec = importlib.util.spec_from_file_location(f"week{week}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.VIDEO


def caption(step):
    """On-screen text for a step: the caption if given, otherwise the spoken text with fixes applied."""
    if len(step) > 2:
        return step[2]
    text = step[1]
    for spoken, written in CAPTION_FIXES.items():
        text = text.replace(spoken, written)
    return text


def write_slide_data(week, video):
    """Write the data file slides.html reads; returns its path relative to slides.html."""
    shown = dict(video, slides=[dict(s, steps=[[st[0], caption(st)] for st in s["steps"]]) for s in video["slides"]])
    path = week_dir(week) / "slides-data.js"
    path.write_text("window.VIDEO = " + json.dumps(shown, ensure_ascii=False) + ";", encoding="utf-8")
    return path.relative_to(HERE).as_posix()


def screenshot(data_file, slide, step, png):
    """Render one slide at one step to a PNG."""
    url = SLIDES.as_uri() + f"?s={slide}&k={step}&d={data_file}"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1280,720", "--virtual-time-budget=5000", f"--screenshot={png}", url],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
