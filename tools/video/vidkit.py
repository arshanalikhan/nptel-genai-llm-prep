"""Building blocks for the week video scripts in tools/video/scripts/.

A video is a list of slides. Each slide has HTML (elements with data-step="k" appear at step k,
elements with data-focus="k" are highlighted at step k) and a list of steps:
    [k, spoken, caption]
spoken  = what the voice says (Devanagari Hindi with English terms, so the Hindi voice pronounces it well)
caption = what is shown on screen (Roman-script Hinglish)
"""
import re
from pathlib import Path

NOTES = Path(__file__).resolve().parents[2] / "src" / "pages" / "notes"


def diagram(week, index=0, max_h=410):
    """The index-th SVG diagram from the site's notes for this week, sized for a slide."""
    page = (NOTES / f"week-{week}.html").read_text(encoding="utf-8")
    svgs = re.findall(r'<svg class="dg".*?</svg>', page, re.S)
    return f'<div class="diagram" style="max-height:{max_h}px">{svgs[index]}</div>'


def title(week, name, chips):
    """Opening slide: week number, title and topic chips. Steps are filled in by the script."""
    chip_html = "".join(f"<span>{c}</span>" for c in chips)
    return {"html": f'''<div style="padding-top:40px"><p class="kick">Week {week} · NPTEL Generative AI &amp; LLMs</p><h1>{name}</h1>
<p class="sub">Short version · exam ke liye zaroori baatein</p>
<div class="chips">{chip_html}</div></div>''', "steps": []}


def cards(heading, items, cols=4):
    """A grid of cards that builds step by step. items: (step, title, body_html, key_text)."""
    inner = "".join(f'<div class="card" data-step="{k}" data-focus="{k}"><b>{t}</b><p>{b}</p>'
                    + (f'<p class="key">{key}</p>' if key else "") + "</div>"
                    for k, t, b, key in items)
    return f'<h2>{heading}</h2><div class="cards4 big" style="grid-template-columns:repeat({cols},1fr)">{inner}</div>'


def points(items):
    """Bullet boxes that appear and highlight at their step. items: (step, html)."""
    return '<ul class="pts">' + "".join(f'<li data-step="{k}" data-focus="{k}">{t}</li>' for k, t in items) + "</ul>"


def split(heading, week, index, items, max_h=440):
    """The site's diagram on the left, step-by-step points on the right."""
    return f'<h2>{heading}</h2><div class="split">' + diagram(week, index, max_h) + points(items) + "</div>"


def traps(items):
    """Recap slide: numbered "trap → right answer" rows. items: (step, left, right)."""
    rows = "".join(f'<li data-step="{k}">{l} <span>→</span> <b>{r}</b></li>' for k, l, r in items)
    return f'<h2>Traps to remember</h2><ol class="traps">{rows}</ol>'


def end(week, next_line):
    """Closing slide pointing to practice and the next video."""
    return {"html": f'''<div style="padding-top:30px"><p class="kick">Done · Week {week}</p><h1>Ab practice kijiye</h1>
<div class="endcards"><div><b>Practice</b>Practice page → W{week} filter</div><div><b>Next</b>{next_line}</div></div></div>''', "steps": []}


def video(week, topline, slides, steps):
    """Attach each slide's steps and return the VIDEO dict the renderer expects."""
    assert len(steps) == len(slides), f"week {week}: {len(slides)} slides but {len(steps)} step lists"
    for slide, slide_steps in zip(slides, steps):
        slide["steps"] = slide_steps
    return {"topline": topline, "slides": slides}
