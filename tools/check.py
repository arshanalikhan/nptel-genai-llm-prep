"""Validate everything under data/ before a build.

Usage:
    python tools/check.py            check all data files, exit 1 on any problem
    python tools/check.py --format   also rewrite the JSON files in the house style

Checks: required fields, week numbers match file names, answers point at real options,
no duplicate options or questions, and every published video file exists.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
problems = []


def fail(where, message):
    problems.append(f"{where}: {message}")


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(path.relative_to(ROOT), f"invalid JSON ({e})")
        return None


def dump(value):
    """JSON with 2-space indents, but short number lists (answers) kept on one line."""
    text = json.dumps(value, indent=2, ensure_ascii=False)
    return re.sub(r"\[\s+([\d,\s]+?)\s+\]", lambda m: "[" + ", ".join(re.split(r",\s*", m.group(1).strip())) + "]", text) + "\n"


def check_question(where, q, extra_text_field="explanation"):
    for field in ("question", "options", "answer", extra_text_field):
        if field not in q:
            fail(where, f"missing '{field}'")
            return
    opts, ans = q["options"], q["answer"]
    if not (2 <= len(opts) <= 6):
        fail(where, f"has {len(opts)} options (expected 2–6)")
    if len(set(opts)) != len(opts):
        fail(where, "has duplicate options")
    if not ans or any(not isinstance(a, int) or not 0 <= a < len(opts) for a in ans):
        fail(where, f"answer {ans} does not match its {len(opts)} options")
    if len(set(ans)) != len(ans):
        fail(where, "answer lists the same option twice")
    unknown = set(q) - {"question", "options", "answer", extra_text_field, "numerical"}
    if unknown:
        fail(where, f"unknown fields {sorted(unknown)}")


def main():
    course = load(DATA / "course.json")
    weeks = {w["week"] for w in course["weeks"]} if course else set()
    seen = {}
    counts = {}

    for folder in ("practice", "my-assignments"):
        for path in sorted((DATA / folder).glob("week-*.json"), key=lambda p: int(p.stem.split("-")[1])):
            rel = path.relative_to(ROOT)
            doc = load(path)
            if doc is None:
                continue
            week = int(path.stem.split("-")[1])
            if doc.get("week") != week:
                fail(rel, f"'week' is {doc.get('week')} but the file name says {week}")
            if week not in weeks:
                fail(rel, f"week {week} is not listed in data/course.json")
            for i, q in enumerate(doc.get("questions", []), 1):
                where = f"{rel} question {i}"
                check_question(where, q)
                key = q.get("question", "").strip().lower()
                if key in seen:
                    fail(where, f"same question text as {seen[key]}")
                seen[key] = where
            counts[folder] = counts.get(folder, 0) + len(doc.get("questions", []))
            if "--format" in sys.argv:
                path.write_text(dump(doc), encoding="utf-8")

    must = load(DATA / "must-know.json") or []
    for i, q in enumerate(must, 1):
        where = f"data/must-know.json item {i}"
        check_question(where, {k: v for k, v in q.items() if k != "week"}, extra_text_field="idea")
        if q.get("week") not in weeks:
            fail(where, f"week {q.get('week')} is not in data/course.json")
    if "--format" in sys.argv:
        (DATA / "must-know.json").write_text(dump(must), encoding="utf-8")

    videos = load(DATA / "videos.json") or []
    for v in videos:
        where = f"data/videos.json week {v.get('week')}"
        if v.get("week") not in weeks:
            fail(where, "week is not in data/course.json")
        for field in ("file", "poster"):
            if not (ROOT / "public" / v.get(field, "")).is_file():
                fail(where, f"{field} public/{v.get(field)} does not exist")
        if not re.fullmatch(r"\d+:\d\d", v.get("duration", "")):
            fail(where, "duration should look like 3:29")

    if problems:
        print(f"{len(problems)} problem(s) found:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print(f"Data OK: {counts.get('practice', 0)} practice questions, {counts.get('my-assignments', 0)} from your assignments, "
          f"{len(must)} must-know, {len(videos)} videos.")


if __name__ == "__main__":
    main()
