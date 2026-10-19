/* Mock exams: build a 50-question paper, sit it in Practice mode (marked as you go) or Exam mode
 * (marked at the end) on a 3-hour timer, then show the score, a week-by-week table and the misses.
 * The paper in progress (as question ids) and the best scores are saved, so a refresh doesn't lose anything. */

const MockExams = (() => {
  const EXAM_KEY = STORAGE_KEY + "-exam";
  const BEST_KEY = STORAGE_KEY + "-best2";
  const MODES = { learn: "Practice mode", exam: "Exam mode" };
  const $ = id => document.getElementById(id);

  const indexes = test => QUESTIONS.map((_, i) => i).filter(i => test(QUESTIONS[i]));
  const MINE = indexes(q => q.mine);
  const BANK = indexes(q => !q.mine);
  const weeksOf = ids => [...new Set(ids.map(i => QUESTIONS[i].week))].sort((a, b) => a - b);
  const weekRange = ws => !ws.length ? "" : ws.every((w, k) => k === 0 || w === ws[k - 1] + 1) && ws.length > 1 ? "W" + ws[0] + "–W" + ws[ws.length - 1] : ws.map(w => "W" + w).join(", ");

  // "Your paper" = all of your own questions, topped up from the weeks they don't cover yet.
  const uncovered = Array.from({ length: WEEK_COUNT }, (_, k) => k + 1).filter(w => !weeksOf(MINE).includes(w));
  const topUp = Math.max(0, PAPER_SIZE - MINE.length);

  const PAPERS = [
    { id: "mine", name: "Your paper", src: "Your " + COURSE.run + " assignments",
      note: "all " + MINE.length + " of yours (" + weekRange(weeksOf(MINE)) + ")" + (topUp && uncovered.length ? " + " + topUp + " from " + weekRange(uncovered) : "") },
    { id: "p1", name: "Paper 1", src: "Set A", note: Math.floor(PAPER_SIZE / WEEK_COUNT) + " per week + " + (PAPER_SIZE % WEEK_COUNT) },
    { id: "p2", name: "Paper 2", src: "Set B", note: "No overlap with set A" },
    { id: "p3", name: "Paper 3", src: "Set C", note: "No overlap with sets A or B" },
    { id: "rand", name: "Random paper", src: "New mix from all " + QUESTIONS.length + " questions", note: "Different every time" },
  ];

  let exam = Saved.get(EXAM_KEY, null);
  if (exam) {
    exam.mode = exam.mode || "exam"; exam.lock = exam.lock || {}; exam.rev = exam.rev || {}; exam.flag = exam.flag || {};
    // papers saved before ids existed stored list positions
    if (exam.ids.some(x => typeof x === "number")) exam.ids = exam.ids.map(i => QUESTIONS[i] && QUESTIONS[i].id);
    if (!exam.ids.every(id => QUESTION_BY_ID[id])) exam = null;   // a question was removed since: drop the paper
    else Saved.set(EXAM_KEY, exam);
  }
  let best = Saved.get(BEST_KEY, {});
  let reviewAll = false;

  /* ---------- Building a paper ---------- */
  function buildPaper(id) {
    if (id === "mine") {
      if (topUp === 0 || !uncovered.length) return shuffled(MINE, seededRandom(12)).slice(0, PAPER_SIZE);
      const random = seededRandom(11);
      const base = Math.floor(topUp / uncovered.length), extra = topUp % uncovered.length;
      const ids = MINE.slice();
      uncovered.forEach((w, k) => ids.push(...shuffled(BANK.filter(i => QUESTIONS[i].week === w), random).slice(0, base + (k < extra ? 1 : 0))));
      return shuffled(ids, seededRandom(12));
    }
    // Papers 1–3 take disjoint slices of each week's shuffled bank questions; "rand" draws from everything.
    const rand = id === "rand";
    const pool = rand ? QUESTIONS.map((_, i) => i) : BANK;
    const slot = { p1: 0, p2: 1, p3: 2, rand: 0 }[id];
    const seed = rand ? (Date.now() & 0x7fffffff) : 7;
    const random = seededRandom(seed);
    const perWeek = Math.floor(PAPER_SIZE / WEEK_COUNT);
    let pick = [], largest = [];
    for (let w = 1; w <= WEEK_COUNT; w++) {
      const week = shuffled(pool.filter(i => QUESTIONS[i].week === w), random);
      if (week.length > largest.length) largest = week;
      pick = pick.concat(week.slice(slot * perWeek, (slot + 1) * perWeek));
    }
    const need = PAPER_SIZE - pick.length;
    const extra = rand ? shuffled(pool.filter(i => !pick.includes(i)), random).slice(0, need)
                       : largest.slice(3 * perWeek + slot * need, 3 * perWeek + (slot + 1) * need);
    return shuffled(pick.concat(extra), seededRandom(seed + 101 + slot));
  }

  /* ---------- Scoring ---------- */
  function formatTime(sec) {
    sec = Math.max(0, Math.round(sec));
    const h = Math.floor(sec / 3600), m = Math.floor(sec % 3600 / 60), s = sec % 60;
    return h + ":" + String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  }
  function remaining() { return exam ? exam.dur - (Date.now() - exam.start) / 1000 : 0; }
  function paperName(id) { const p = PAPERS.find(p => p.id === id); return p ? p.name + " · " + p.src : id; }
  function isRight(ex, pos) { return !(ex.rev && ex.rev[pos]) && sameSet(ex.ans[pos] || [], QUESTION_BY_ID[ex.ids[pos]].answer); }

  function score(ex) {
    let correct = 0, revealed = 0;
    const byWeek = {};
    ex.ids.forEach((id, pos) => {
      const ok = isRight(ex, pos);
      if (ok) correct++;
      if (ex.rev && ex.rev[pos]) revealed++;
      const w = QUESTION_BY_ID[id].week;
      byWeek[w] = byWeek[w] || [0, 0];
      byWeek[w][1]++; if (ok) byWeek[w][0]++;
    });
    const raw = Math.round(correct / ex.ids.length * 100);
    return { correct, revealed, raw, out75: raw * 0.75, pass: raw >= PASS_MARK, byWeek };
  }

  /* ---------- Starting, saving, finishing ---------- */
  function start(id, mode) {
    exam = { id, mode, ids: buildPaper(id).map(i => QUESTIONS[i].id), ans: {}, flag: {}, lock: {}, rev: {}, cur: 0, start: Date.now(), dur: PAPER_SECONDS, done: false };
    Saved.set(EXAM_KEY, exam); render(); focusQuestion();
  }
  function persist() { Saved.set(EXAM_KEY, exam); render(); }
  function quit() { exam = null; Saved.set(EXAM_KEY, null); render(); }

  function finish() {
    if (!exam || exam.done) return;
    exam.done = true; exam.end = Date.now();
    const s = score(exam);
    const key = exam.id + "|" + exam.mode;
    if (!best[key] || s.raw > best[key].raw) { best[key] = { raw: s.raw, at: exam.end }; Saved.set(BEST_KEY, best); }
    Saved.set(EXAM_KEY, exam); reviewAll = false; render(); window.scrollTo({ top: 0, behavior: "instant" });
    if (s.pass && window.confetti && !REDUCED_MOTION) {
      const cs = getComputedStyle(document.documentElement);
      const colors = ["--accent", "--ok", "--hi"].map(v => cs.getPropertyValue(v).trim()).filter(Boolean);
      setTimeout(() => window.confetti({ particleCount: 140, spread: 80, startVelocity: 42, origin: { y: 0.3 }, colors }), 250);
    }
  }

  // After moving to another question, bring its card into view below the sticky bars (matters on phones).
  function focusQuestion() {
    const go = () => {
      const card = document.querySelector("#mockroot .q"); if (!card) return;
      const bar = document.querySelector(".exambar");
      const offset = (document.querySelector(".topbar") || { offsetHeight: 0 }).offsetHeight + (bar ? bar.offsetHeight : 0) + 12;
      const top = card.getBoundingClientRect().top;
      if (top < offset || top > window.innerHeight * 0.5) window.scrollTo({ top: Math.max(0, window.scrollY + top - offset), behavior: "instant" });
    };
    go();
    requestAnimationFrame(go); // once more after the sticky bar settles
  }

  /* ---------- Screens ---------- */
  function render() {
    const root = $("mockroot");
    root.innerHTML = "";
    root.appendChild(!exam ? renderPapers() : !exam.done ? renderExam() : renderResult());
  }

  function renderPapers() {
    const wrap = el("div", "papers");
    PAPERS.forEach(p => {
      const card = el("div", "paper");
      card.append(el("p", "eyebrow", p.name), el("h3", null, p.src), el("p", "src", PAPER_SIZE + " questions · 3 hours · " + p.note));
      ["learn", "exam"].forEach(m => {
        const b = best[p.id + "|" + m];
        const line = el("p", "best");
        line.append(document.createTextNode(MODES[m] + ": "));
        if (b) line.append(el("b", null, "best " + b.raw + "/100"), document.createTextNode(" (" + (b.raw * 0.75).toFixed(1) + "/75)"));
        else line.append(document.createTextNode("not attempted"));
        card.appendChild(line);
      });
      const row = el("div", "startrow");
      row.append(button("btn primary", "Practice mode", () => start(p.id, "learn")), button("btn", "Exam mode", () => start(p.id, "exam")));
      card.appendChild(row);
      wrap.appendChild(card);
    });
    return wrap;
  }

  function renderExam() {
    const learn = exam.mode === "learn";
    const N = exam.ids.length;
    const box = el("div", "result");

    // Sticky bar: paper name, timer, progress, finish
    const bar = el("div", "exambar");
    const timer = el("span", "timer", formatTime(remaining())); timer.id = "timer";
    let progress;
    if (learn) {
      const checked = Object.keys(exam.lock).filter(k => exam.lock[k]);
      progress = checked.length + "/" + N + " checked · " + checked.filter(k => isRight(exam, Number(k))).length + " right";
    } else {
      progress = Object.keys(exam.ans).filter(k => exam.ans[k].length).length + "/" + N + " answered";
    }
    const finishBtn = button("btn primary", "Finish & see score");
    confirmButton(finishBtn, "Finish & see score", "Tap again to finish", finish);
    bar.append(el("span", "who name", paperName(exam.id) + " · " + MODES[exam.mode]), timer, el("span", "who", progress), finishBtn);

    // Current question
    const pos = exam.cur, q = QUESTION_BY_ID[exam.ids[pos]];
    const multi = q.answer.length > 1;
    const sel = exam.ans[pos] || [];
    const locked = learn && !!exam.lock[pos];
    const revealed = !!exam.rev[pos];
    const card = el("article", "q");
    const meta = el("div", "q-meta");
    meta.append(el("span", null, "Question " + (pos + 1) + " of " + N), el("span", null, "Week " + q.week), el("span", null, multi ? "Select all that apply" : "One answer"));
    if (exam.flag[pos]) meta.appendChild(el("span", "k", "Marked for review"));
    card.append(meta, el("p", "q-text", q.question));

    const opts = el("div", "opts");
    q.options.forEach((text, k) => {
      const b = optionButton(k, text);
      if (locked) {
        b.disabled = true;
        if (q.answer.includes(k)) b.classList.add("correct"); else if (sel.includes(k)) b.classList.add("wrong");
      } else {
        b.setAttribute("aria-pressed", String(sel.includes(k)));
        b.addEventListener("click", () => {
          let s = exam.ans[pos] || [];
          if (multi) s = s.includes(k) ? s.filter(x => x !== k) : s.concat(k);
          else s = learn ? [k] : (s.includes(k) ? [] : [k]);
          exam.ans[pos] = s;
          if (learn && !multi) exam.lock[pos] = true;
          persist();
        });
      }
      opts.appendChild(b);
    });
    card.appendChild(opts);

    if (learn) {
      const foot = el("div", "q-foot");
      if (!locked) {
        if (multi) {
          const check = button("btn primary", "Check", () => { exam.lock[pos] = true; persist(); });
          check.disabled = sel.length === 0;
          foot.appendChild(check);
        }
        foot.appendChild(button("btn", "Reveal answer", () => { exam.rev[pos] = true; exam.lock[pos] = true; persist(); }));
      } else {
        const ok = isRight(exam, pos);
        foot.appendChild(el("span", "verdict " + (revealed ? "rev" : ok ? "ok" : "no"), revealed ? "Revealed (counts as wrong)" : ok ? "Correct" : "Not quite"));
      }
      card.appendChild(foot);
      if (locked) card.appendChild(answerBox(q.answer, null, q.explanation));
    }

    // Previous / mark / clear / next
    const nav = el("div", "navbtns");
    const left = el("div"), right = el("div");
    const prev = button("btn", "← Previous", () => { exam.cur--; persist(); focusQuestion(); });
    prev.disabled = pos === 0;
    left.append(prev, button("btn", exam.flag[pos] ? "Unmark" : "Mark for review", () => { exam.flag[pos] = !exam.flag[pos]; persist(); }));
    if (!locked) left.appendChild(button("btn", "Clear", () => { delete exam.ans[pos]; persist(); }));
    const next = button("btn primary", "Next →", () => { exam.cur++; persist(); focusQuestion(); });
    next.disabled = pos === N - 1;
    right.append(next);
    nav.append(left, right);
    card.appendChild(nav);

    // Side panel: question palette, legend, quit
    const side = el("div", "side");
    side.appendChild(el("p", "eyebrow", "Questions"));
    const palette = el("div", "palette");
    exam.ids.forEach((_, i) => {
      const b = button("pal", String(i + 1), () => { exam.cur = i; persist(); focusQuestion(); });
      if (learn && exam.lock[i]) b.classList.add(exam.rev[i] ? "rev" : isRight(exam, i) ? "ok" : "no");
      else if ((exam.ans[i] || []).length) b.classList.add("ans");
      if (exam.flag[i]) b.classList.add("flag");
      if (i === pos) { b.classList.add("cur"); b.setAttribute("aria-current", "true"); }
      palette.appendChild(b);
    });
    const legend = el("p", "legend");
    (learn ? ["Green = right", "Red = wrong", "Amber = revealed", "Blue = picked, not checked", "Outline = current"]
           : ["Blue = answered", "Amber underline = marked", "Outline = current"]).forEach(t => legend.appendChild(el("span", null, t)));
    const quitBtn = button("btn", "Quit paper");
    confirmButton(quitBtn, "Quit paper", "Tap again to discard", quit);
    side.append(palette, legend, quitBtn);

    const grid = el("div", "exam-grid");
    grid.append(card, side);
    box.append(bar, grid);
    return box;
  }

  function renderResult() {
    const s = score(exam);
    const box = el("div", "result");
    box.appendChild(el("p", "eyebrow", paperName(exam.id) + " · " + MODES[exam.mode] + " · finished"));

    const tiles = el("div", "tiles");
    const tile = (value, label) => { const d = el("div", "tile"); d.append(el("span", "l", label), el("span", "v", value)); return d; };
    const used = Math.min(exam.dur, ((exam.end || Date.now()) - exam.start) / 1000);
    tiles.append(tile(s.raw + "/100", "Final score"), tile(s.out75.toFixed(1) + "/75", "Exam component"), tile(s.correct + "/" + exam.ids.length, "Correct"), tile(formatTime(used), "Time used"));
    if (s.revealed) tiles.appendChild(tile(String(s.revealed), "Answers revealed"));

    const verdict = el("p");
    verdict.append(el("span", "pill " + (s.pass ? "ok" : "no"), s.pass ? "Above the pass line" : "Below the pass line"),
      document.createTextNode(s.pass ? "  You need ≥ 30/75 in the exam; you have " + s.out75.toFixed(1) + "." : "  You need ≥ 30/75 (40/100 raw). Review the misses below and retake."));

    const weeks = el("div", "tbl");
    const table = document.createElement("table");
    table.innerHTML = "<thead><tr><th>Week</th><th>Correct</th><th>Accuracy</th></tr></thead>";
    const body = document.createElement("tbody");
    Object.keys(s.byWeek).map(Number).sort((a, b) => a - b).forEach(w => {
      const [c, n] = s.byWeek[w];
      const tr = document.createElement("tr");
      ["W" + w, c + "/" + n, Math.round(c / n * 100) + "%"].forEach(v => tr.appendChild(el("td", null, v)));
      body.appendChild(tr);
    });
    table.appendChild(body); weeks.appendChild(table);

    const actions = el("div", "navbtns");
    const left = el("div");
    left.append(button("btn primary", "Retake this paper", () => start(exam.id, exam.mode)), button("btn", "Back to papers", quit));
    actions.append(left, button("btn", reviewAll ? "Show only mistakes" : "Show all questions", () => { reviewAll = !reviewAll; render(); }));

    const list = el("div", "qlist");
    exam.ids.forEach((id, pos) => {
      const q = QUESTION_BY_ID[id];
      const picked = exam.ans[pos] || [];
      const ok = isRight(exam, pos);
      if (ok && !reviewAll) return;
      const card = el("article", "q");
      const meta = el("div", "q-meta");
      meta.append(el("span", null, "Q" + (pos + 1)), el("span", null, "Week " + q.week));
      const label = exam.rev[pos] ? "Revealed" : ok ? "Correct" : (picked.length ? "Wrong" : "Not answered");
      meta.appendChild(el("span", "verdict " + (exam.rev[pos] ? "rev" : ok ? "ok" : "no"), label));
      card.append(meta, el("p", "q-text", q.question));
      const opts = el("div", "opts");
      q.options.forEach((text, k) => {
        const b = optionButton(k, text); b.disabled = true;
        if (q.answer.includes(k)) b.classList.add("correct"); else if (picked.includes(k)) b.classList.add("wrong");
        opts.appendChild(b);
      });
      card.append(opts, answerBox(q.answer, null, q.explanation));
      list.appendChild(card);
    });
    if (!list.childNodes.length) list.appendChild(el("p", "callout", "No mistakes on this paper."));

    box.append(tiles, verdict, weeks, actions, list);
    return box;
  }

  function init() {
    setInterval(() => {
      if (!exam || exam.done) return;
      const r = remaining();
      const t = $("timer");
      if (t) { t.textContent = formatTime(r); t.classList.toggle("low", r < 600); }
      if (r <= 0) finish();
    }, 1000);
    render();
  }

  /** Best raw score (out of 100) across all papers and modes, or -1 if none finished. */
  function bestScore() { return Object.values(best).reduce((m, b) => Math.max(m, b && typeof b.raw === "number" ? b.raw : -1), -1); }
  function isRunning() { return !!(exam && !exam.done); }

  return { init, bestScore, isRunning, buildPaper };
})();
