/* Practice page: filter chips (your assignments, practice bank, all, numericals, each week),
 * 15 question cards per page, and Shuffle / Show all answers / Reset this set.
 * Answers are saved per question id. */

const Practice = (() => {
  const PER_PAGE = 15;
  const FILTER_KEY = STORAGE_KEY + "-f";
  let answers = keyedById(Saved.get(STORAGE_KEY, {}), QUESTIONS);
  let filter = Saved.getText(FILTER_KEY, "mine");
  let order = QUESTIONS.map((_, i) => i);
  let showAll = false;
  let page = 0;

  const $ = id => document.getElementById(id);
  function save() { Saved.set(STORAGE_KEY, answers); Saved.setText(FILTER_KEY, filter); }

  const FILTERS = [
    ["mine", "My 2026 assignments", q => q.mine],
    ["past", "Practice bank", q => !q.mine],
    ["all", "All", () => true],
    ["num", "Numericals", q => q.numerical],
  ];
  for (let w = 1; w <= WEEK_COUNT; w++) FILTERS.push([String(w), "W" + w, q => q.week === w]);

  function matches(i) {
    const f = FILTERS.find(([id]) => id === filter) || FILTERS[2];
    return f[2](QUESTIONS[i]);
  }
  function visible() { return order.filter(matches); }

  function renderChips() {
    const box = $("chips");
    box.innerHTML = "";
    FILTERS.forEach(([id, label, test]) => {
      const b = button("chip", null, () => { filter = id; page = 0; save(); renderChips(); render(); });
      b.dataset.f = id;
      b.setAttribute("aria-pressed", String(filter === id));
      b.innerHTML = label + " <small>" + QUESTIONS.filter(test).length + "</small>";
      box.appendChild(b);
    });
  }

  function card(i, n) {
    const q = QUESTIONS[i];
    const meta = ["Q" + n, "Week " + q.week];
    if (q.mine) meta.push(["mine", "Your " + COURSE.run + " assignment"]);
    if (q.numerical) meta.push(["k", "Numerical"]);
    return questionCard({
      id: "q" + i, data: { n },
      meta, question: q.question, options: q.options, answer: q.answer, explanation: q.explanation,
      state: answers[q.id], showAnswer: showAll,
      onPick: k => { answers[q.id] = pickOption(answers[q.id], k, q.answer); save(); redraw(i); },
      onCheck: () => { answers[q.id] = checkAnswer(answers[q.id], q.answer); save(); redraw(i); },
    });
  }

  function redraw(i) {
    const old = $("q" + i);
    if (old) old.replaceWith(card(i, Number(old.dataset.n)));
    renderScore();
  }

  function renderScore() {
    const ids = visible();
    $("score").innerHTML = scoreLine(ids.map(i => answers[QUESTIONS[i].id]), ids.length);
  }

  function renderPager(box, pages) {
    box.innerHTML = "";
    if (pages <= 1) return;
    const to = (label, target, cls) => {
      const b = button("btn" + (cls ? " " + cls : ""), label, () => { page = target; render(); $("qlist").scrollIntoView({ block: "start" }); });
      b.disabled = target < 0 || target >= pages;
      return b;
    };
    const info = el("span", "score");
    info.innerHTML = "Page <b>" + (page + 1) + "</b> of " + pages;
    box.append(to("← Previous", page - 1), info, to("Next →", page + 1, "primary"));
  }

  function render() {
    const ids = visible();
    const pages = Math.max(1, Math.ceil(ids.length / PER_PAGE));
    if (page >= pages) page = pages - 1;
    const list = $("qlist");
    list.innerHTML = "";
    const frag = document.createDocumentFragment();
    ids.slice(page * PER_PAGE, (page + 1) * PER_PAGE).forEach((i, n) => frag.appendChild(card(i, page * PER_PAGE + n + 1)));
    list.appendChild(frag);
    renderPager($("qpagerTop"), pages);
    renderPager($("qpagerBot"), pages);
    renderScore();
  }

  function init() {
    save();   // stores progress in the id-keyed form if it was converted
    $("shuffle").addEventListener("click", e => {
      const b = e.currentTarget;
      order = QUESTIONS.map((_, i) => i);
      if (b.dataset.on === "1") { b.dataset.on = "0"; b.textContent = "Shuffle"; }
      else { order = shuffled(order, Math.random); b.dataset.on = "1"; b.textContent = "Original order"; }
      page = 0;
      render();
    });
    $("reveal").addEventListener("click", e => {
      showAll = !showAll;
      e.currentTarget.setAttribute("aria-pressed", String(showAll));
      e.currentTarget.textContent = showAll ? "Hide answers" : "Show all answers";
      render();
    });
    confirmButton($("reset"), "Reset this set", "Tap again to clear", () => {
      visible().forEach(i => delete answers[QUESTIONS[i].id]);
      save(); render();
    });
    renderChips();
    render();
  }

  /** For the home page: how many answered and how many right, across all questions. */
  function progress() {
    const done = Object.keys(answers).filter(k => QUESTION_BY_ID[k] && answers[k] && answers[k].done);
    return { done: done.length, correct: done.filter(k => answers[k].ok).length, total: QUESTIONS.length };
  }

  return { init, progress };
})();
