"""Quick layout check before the slow narration step: renders the last step of every slide.

Usage:
    python tools/video/preview.py 3

Writes tools/video/.build/week-3/preview/s0.png, s1.png, … and prints each caption's length
(captions over ~150 characters wrap to two lines).
"""
import sys

from slides import load_week, screenshot, week_dir, write_slide_data, caption


def main():
    week = int(sys.argv[1])
    video = load_week(week)
    data_file = write_slide_data(week, video)
    out = week_dir(week) / "preview"
    out.mkdir(exist_ok=True)
    for i, slide in enumerate(video["slides"]):
        last = max(st[0] for st in slide["steps"])
        screenshot(data_file, i, last, out / f"s{i}.png")
        for st in slide["steps"]:
            print(f"slide {i} step {st[0]}: {len(caption(st)):3d} chars")
    print("Preview images in", out)


if __name__ == "__main__":
    main()
