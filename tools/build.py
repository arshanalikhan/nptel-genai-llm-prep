"""Build the website from src/, data/ and public/ into dist/.

Usage:
    python tools/build.py             build into dist/
    python tools/build.py --out DIR   build somewhere else

What it does:
  1. HTML  src/index.html with every <!-- include: path --> replaced by that file (recursively),
           and {{name}} placeholders filled with counts from the data.
  2. CSS   the files in CSS_FILES joined into assets/site.css.
  3. JS    data/ turned into assets/data.js (COURSE, QUESTIONS, MUST_KNOW, VIDEOS);
           the files in JS_FILES joined, in order, into assets/app.js.
  4. Files everything in public/ (videos, favicon) copied as-is.
Asset links get a content hash (?v=…) so browsers never mix a new page with old cached files.
Only the Python standard library is needed.
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, DATA, PUBLIC = ROOT / "src", ROOT / "data", ROOT / "public"

CSS_FILES = [
    "css/base.css", "css/layout.css", "css/components.css",
    "css/pages/home.css", "css/pages/notes.css", "css/pages/course-map.css", "css/pages/numericals.css",
    "css/pages/practice.css", "css/pages/mock-exams.css", "css/pages/videos.css", "css/pages/reference.css",
]
JS_FILES = [   # order matters: later files use what earlier ones define
    "js/config.js", "js/helpers.js", "js/theme.js",
    "js/practice.js", "js/must-know.js", "js/mock-exams.js", "js/videos.js",
    "js/notes.js", "js/numericals.js", "js/home.js", "js/router.js",
    "js/main.js",
]
INCLUDE_LINE = re.compile(r"^[ \t]*<!-- include: (\S+) -->[ \t]*\n?", re.M)   # marker on its own line
INCLUDE_INLINE = re.compile(r"<!-- include: (\S+) -->")                       # marker inside a line (the logo)
BANNER = "Built by tools/build.py from {src}. Edit the source files, not this one."


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def week_files(folder):
    return sorted((DATA / folder).glob("week-*.json"), key=lambda p: int(p.stem.split("-")[1]))


def stable_id(prefix, text):
    """Saved answers are keyed by this, so it only changes if the question's wording changes."""
    return prefix + hashlib.sha1(" ".join(text.lower().split()).encode()).hexdigest()[:8]


def load_data():
    course = read_json(DATA / "course.json")
    questions = []
    # Practice bank first, then your own assignments (older saved progress used this position).
    for folder, mine in (("practice", False), ("my-assignments", True)):
        for path in week_files(folder):
            doc = read_json(path)
            for q in doc["questions"]:
                item = {"id": stable_id("q", q["question"]), "week": doc["week"], "question": q["question"],
                        "options": q["options"], "answer": q["answer"], "explanation": q["explanation"]}
                if q.get("numerical"):
                    item["numerical"] = True
                if mine:
                    item["mine"] = True
                questions.append(item)
    must_know = [{"id": stable_id("k", m["question"]), **m} for m in read_json(DATA / "must-know.json")]
    for items in (questions, must_know):
        ids = [x["id"] for x in items]
        if len(ids) != len(set(ids)):
            raise SystemExit("two questions have the same wording; run python tools/check.py")
    videos = [v for v in read_json(DATA / "videos.json") if (PUBLIC / v["file"]).is_file()]
    return course, questions, must_know, videos


def week_span(weeks):
    weeks = sorted(set(weeks))
    if not weeks:
        return "none"
    if len(weeks) > 1 and weeks == list(range(weeks[0], weeks[-1] + 1)):
        return f"{weeks[0]}–{weeks[-1]}"
    return ", ".join(map(str, weeks))


def render_html(path, values, seen=()):
    if path in seen:
        raise SystemExit(f"include loop: {' -> '.join(map(str, seen + (path,)))}")
    text = (SRC / path).read_text(encoding="utf-8")
    text = INCLUDE_LINE.sub(lambda m: render_html(m.group(1), values, seen + (path,)).rstrip("\n") + "\n", text)
    text = INCLUDE_INLINE.sub(lambda m: render_html(m.group(1), values, seen + (path,)).strip(), text)
    for name, value in values.items():
        text = text.replace("{{" + name + "}}", str(value))
    return text


def write(out, rel, text):
    path = out / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return f"{rel}?v={hashlib.sha1(text.encode()).hexdigest()[:10]}"


def join_files(files, comment):
    parts = []
    for rel in files:
        body = (SRC / rel).read_text(encoding="utf-8").strip()
        parts.append(f"{comment[0]} ===== src/{rel} ===== {comment[1]}\n{body}\n")
    return "\n".join(parts)


def main():
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "dist"
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(PUBLIC, out)

    course, questions, must_know, videos = load_data()
    mine = [q for q in questions if q.get("mine")]
    values = {
        "bank_count": len(questions) - len(mine),
        "mine_count": len(mine),
        "mine_weeks": week_span(q["week"] for q in mine),
        "must_know_count": len(must_know),
        "total_count": len(questions),
    }

    css = f"/* {BANNER.format(src='src/css')} */\n\n" + join_files(CSS_FILES, ("/*", "*/"))
    dumps = lambda v: json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    data_js = (f"// {BANNER.format(src='data/')}\n"
               f"const COURSE = {dumps(course)};\n"
               f"const QUESTIONS = {dumps(questions)};\n"
               f"const MUST_KNOW = {dumps(must_know)};\n"
               f"const VIDEOS = {dumps(videos)};\n")
    app_js = f"// {BANNER.format(src='src/js')}\n\n" + join_files(JS_FILES, ("//", ""))

    values["stylesheet"] = write(out, "assets/site.css", css)
    scripts = [write(out, "assets/data.js", data_js), write(out, "assets/app.js", app_js)]
    values["scripts"] = "\n".join(f'<script src="{s}"></script>' for s in scripts)

    html = render_html("index.html", values)
    leftover = re.findall(r"\{\{\w+\}\}|<!-- include:", html)
    if leftover:
        raise SystemExit(f"unfilled placeholders in the page: {sorted(set(leftover))}")
    (out / "index.html").write_text(html, encoding="utf-8", newline="\n")

    print(f"Built {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}: "
          f"{len(questions)} questions ({len(mine)} yours), {len(must_know)} must-know, {len(videos)} videos; "
          f"page {len(html) // 1024} KB, css {len(css) // 1024} KB, js {len(app_js) // 1024} KB + data {len(data_js) // 1024} KB")


if __name__ == "__main__":
    main()
