# NPTEL Generative AI & LLMs — exam prep

An unofficial study site for the NPTEL course **Generative AI and Large Language Models**
(`imb26_mg164`, IIM Bangalore, Prof. Naveen Kumar Bhansali, Jul–Oct 2026 run).

**Live site:** https://arshanalikhan.github.io/nptel-genai-llm-prep/

| Page | What's there |
|---|---|
| Week notes | All 7 weeks, each opening with a diagram; "Your 2026" boxes summarise what each assignment asked |
| Videos | A short Hinglish explainer for every week, with captions |
| Course map | The whole course on one poster |
| Numericals | Formula cards and step-by-step worked examples (TF-IDF, attention, LoRA, GPU memory, ROUGE …) |
| Must-know | 40 core ideas as exam-style MCQs |
| Practice | Questions from your own assignments plus an original practice bank, filterable by week |
| Mock exams | 50-question, 3-hour papers in practice or exam mode, with a score and review |
| Traps · Resources | Last-minute traps, the course page, textbook and original papers |

Everything runs in the browser; progress is saved in the reader's own browser (`localStorage`). No server, no tracking.

## Repository layout

```
├── src/                     Website source
│   ├── index.html           Page skeleton; pulls in the parts below with <!-- include: … -->
│   ├── partials/            Navigation (sidebar, phone bars), footer, logo
│   ├── pages/               One file per page; notes/week-1.html … week-7.html for the week notes
│   ├── css/                 base · layout · components, then pages/<page>.css
│   └── js/                  One module per feature (see "How the code fits together")
├── data/                    Content as JSON (edit these to change questions)
│   ├── course.json          Course facts, exam date, week titles, study-plan dates
│   ├── practice/            Original practice questions, week-1.json … week-7.json
│   ├── my-assignments/      Your own graded assignments (added only after their due date)
│   ├── must-know.json       The 40 must-know MCQs
│   └── videos.json          Published videos and their durations
├── public/                  Copied to the site as-is: videos/, favicon.svg
├── tools/
│   ├── build.py             src/ + data/ + public/ → dist/
│   ├── check.py             Validates everything in data/
│   └── video/               Makes the week videos (scripts/week1.py … week7.py)
└── .github/workflows/       Checks, builds and deploys to GitHub Pages on every push to main
```

`dist/` (the built site) and `tools/video/.build/` (video work files) are generated and not committed.

## Build and preview locally

Needs Python 3.10+ only.

```bash
python tools/check.py
python tools/build.py
python -m http.server 8000 --directory dist
```

Then open http://localhost:8000.

## Editing content

**Add or fix a practice question:** edit `data/practice/week-N.json`. Each question looks like:

```json
{
  "question": "Which Word2Vec variant generally works better for rare words?",
  "options": ["CBOW", "Skip-gram", "One-hot", "TF-IDF"],
  "answer": [1],
  "explanation": "Skip-gram makes several training examples per occurrence of a word."
}
```

`answer` lists the 0-based index of every correct option (two or more = "select all that apply").
Add `"numerical": true` for calculation questions. Then run `python tools/check.py --format`, which
checks the file and tidies its formatting.

**Add a finished assignment week:** create `data/my-assignments/week-N.json` in the same shape
(`week`, `source`, `questions`). Only add a week after its due date has passed and NPTEL shows the
accepted answers, and reword the questions rather than copying them.

> Readers' saved answers are keyed by an id made from each question's wording, so you can add,
> remove or reorder questions freely. Rewording a question resets that one question's saved answer.

**Notes, numericals, traps, resources:** edit the matching file in `src/pages/`.
`{{mine_count}}`-style placeholders are filled in from the data at build time.

## Videos

Each week's video is a script in `tools/video/scripts/weekN.py`: slides (HTML) plus narration
steps written as `[step, spoken, caption]`. The narration is spoken Hindi with English terms;
captions are Roman-script Hinglish.

```bash
pip install -r tools/video/requirements.txt   # once; also needs Google Chrome
python tools/video/preview.py 3               # check slide layouts (fast)
python tools/video/render.py 3                # make tools/video/.build/week-3/week-03.mp4 (~3 min)
python tools/video/publish.py 3               # check it, copy to public/videos, update data/videos.json
```

## How the code fits together

`tools/build.py` joins the CSS files into `assets/site.css` and the JS modules, in this order,
into `assets/app.js`. It also turns `data/` into `assets/data.js` (`COURSE`, `QUESTIONS`,
`MUST_KNOW`, `VIDEOS`).

| Module | Job |
|---|---|
| `config.js` | Site name, storage key, exam date, paper size |
| `helpers.js` | Saved state, DOM helpers, dates, seeded shuffle, the shared question card |
| `theme.js` | Light / dark switch |
| `practice.js` | Practice page: filters, paging, answers |
| `must-know.js` | Must-know page |
| `mock-exams.js` | Paper building, timer, exam and result screens |
| `videos.js` | Videos page and the "Watch" buttons in the notes |
| `notes.js` | One week at a time, "reviewed" marks, week footers |
| `numericals.js` | "Open all workings" |
| `home.js` | Countdowns, progress rings, study plan, hero animation |
| `router.js` | Hash routes (`#practice`, `#w3`, `#v3` …), phone menu, pager |
| `main.js` | Starts everything in order |

Each module is a small object (`Practice`, `MockExams`, …) that exposes only what other modules use.

## Deployment

Every push to `main` runs `.github/workflows/deploy.yml`: check the data, build, syntax-check the
JavaScript, and publish `dist/` to GitHub Pages.

## Notes

- Not affiliated with NPTEL, SWAYAM or IIM Bangalore. Practice-bank questions are original, written
  from the public syllabus. Assignment questions are reworded from the author's own graded work and
  added only after each due date.
- Fonts: IBM Plex (Google Fonts). Icons: Lucide. Confetti: canvas-confetti. Voices: Microsoft Edge TTS.
