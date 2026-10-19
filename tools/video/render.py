"""Render one week's explainer video.

Usage:
    python tools/video/render.py 3                 voice: Microsoft Swara (Hindi, neural), +8% speed
    python tools/video/render.py 3 --reuse         keep slides/narration already made, only re-encode
    python tools/video/render.py 3 --voice edge:hi-IN-MadhurNeural --rate +5%

Output: tools/video/.build/week-3/week-03.mp4. Publish it with publish.py.

How it works, and why: every step becomes one PNG (headless Chrome) and one narration WAV.
The WAVs are joined into ONE soundtrack and the PNGs into ONE image sequence with matching
durations, then encoded once at a constant 24 fps with a keyframe every 2 s. (Joining separately
encoded clips makes timestamps jump at the joins, and players stall there.)

Needs: Google Chrome, and `pip install -r tools/video/requirements.txt` (edge-tts, imageio-ffmpeg).
The edge-tts service is online and drops connections now and then, so each line is retried.
"""
import argparse
import array
import asyncio
import subprocess
import time
import wave

import imageio_ffmpeg

from slides import load_week, screenshot, week_dir, write_slide_data

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 24
LEAD, TAIL = 0.15, 0.35          # seconds of silence before and after each narrated step


def narrate(text, voice, rate, mp3, wav):
    import edge_tts
    error = None
    for attempt in range(12):
        try:
            asyncio.run(edge_tts.Communicate(text, voice, rate=rate).save(str(mp3)))
            if mp3.stat().st_size > 2000:
                break
        except Exception as e:   # the service drops connections intermittently
            error = e
        time.sleep(2 + 2 * attempt)
    else:
        raise RuntimeError(f"text-to-speech failed for {mp3.stem}: {error}")
    subprocess.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp3),
                    "-ar", "24000", "-ac", "1", "-sample_fmt", "s16", str(wav)], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("week", type=int)
    ap.add_argument("--voice", default="edge:hi-IN-SwaraNeural")
    ap.add_argument("--rate", default="+8%")
    ap.add_argument("--reuse", action="store_true", help="skip slides and narration that already exist")
    args = ap.parse_args()
    voice = args.voice.removeprefix("edge:")

    video = load_week(args.week)
    work = week_dir(args.week)
    frames, audio = work / "frames", work / "audio"
    frames.mkdir(exist_ok=True); audio.mkdir(exist_ok=True)
    data_file = write_slide_data(args.week, video)
    steps = [(si, st[0], st[1]) for si, s in enumerate(video["slides"]) for st in s["steps"]]
    names = [f"s{si}_k{k}" for si, k, _ in steps]

    # 1. slides
    for (si, k, _), name in zip(steps, names):
        png = frames / f"{name}.png"
        if not (args.reuse and png.exists()):
            screenshot(data_file, si, k, png)

    # 2. narration
    for (_, _, text), name in zip(steps, names):
        wav = audio / f"{name}.wav"
        if not (args.reuse and wav.exists()):
            narrate(text, voice, args.rate, audio / f"{name}.mp3", wav)

    # 3. one soundtrack + one image list with matching durations (snapped to whole frames)
    pcm, params, durations = array.array("h"), None, []
    for name in names:
        with wave.open(str(audio / f"{name}.wav")) as w:
            p = w.getparams()
            params = params or p
            assert (p.nchannels, p.sampwidth, p.framerate) == (params.nchannels, params.sampwidth, params.framerate), "voice format changed"
            data = array.array("h", w.readframes(w.getnframes()))
        rate, ch = params.framerate, params.nchannels
        total = round((LEAD + len(data) / ch / rate + TAIL) * FPS) / FPS
        lead = int(LEAD * rate) * ch
        pad = int(round(total * rate)) * ch - lead - len(data)
        pcm.extend(array.array("h", bytes(2 * lead))); pcm.extend(data); pcm.extend(array.array("h", bytes(2 * max(0, pad))))
        durations.append(total)
    track = work / "narration.wav"
    with wave.open(str(track), "wb") as w:
        w.setnchannels(params.nchannels); w.setsampwidth(params.sampwidth); w.setframerate(params.framerate)
        w.writeframes(pcm.tobytes())
    listing = []
    for name, d in zip(names, durations):
        listing += [f"file '{frames / (name + '.png')}'", f"duration {d:.6f}"]
    listing.append(f"file '{frames / (names[-1] + '.png')}'")   # the concat demuxer needs the last image repeated
    (work / "images.txt").write_text("\n".join(listing) + "\n", encoding="utf-8")

    # 4. single encode
    out = work / f"week-{args.week:02d}.mp4"
    subprocess.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", str(work / "images.txt"), "-i", str(track),
                    "-map", "0:v", "-map", "1:a", "-vf", f"fps={FPS},format=yuv420p",
                    "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage", "-crf", "26", "-g", str(FPS * 2),
                    "-c:a", "aac", "-b:a", "96k", "-ar", "44100", "-ac", "2",
                    "-t", f"{sum(durations):.3f}", "-movflags", "+faststart", str(out)], check=True)
    print(f"Rendered {out} ({sum(durations):.1f} s, {len(names)} steps). Next: python tools/video/publish.py {args.week}")


if __name__ == "__main__":
    main()
