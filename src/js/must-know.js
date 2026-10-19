/* Must-know page: one MCQ per core idea, grouped by week, with "Key idea" explanations. */

const MustKnow = (() => {
  const SAVE_KEY = STORAGE_KEY + "-rep";
  let answers = keyedById(Saved.get(SAVE_KEY, {}), MUST_KNOW);
  const known = new Set(MUST_KNOW.map(it => it.id));
  let showAll = false;
  const $ = id => document.getElementById(id);

  function card(i, rank) {
    const it = MUST_KNOW[i];
    return questionCard({
      id: "rep" + i, data: { rank },
      meta: [["rkn", "#" + String(rank).padStart(2, "0")], "W" + it.week],
      question: it.question, options: it.options, answer: it.answer,
      explanation: it.idea, explanationLabel: "Key idea",
      state: answers[it.id], showAnswer: showAll,
      onPick: k => { answers[it.id] = pickOption(answers[it.id], k, it.answer); Saved.set(SAVE_KEY, answers); redraw(i); },
      onCheck: () => { answers[it.id] = checkAnswer(answers[it.id], it.answer); Saved.set(SAVE_KEY, answers); redraw(i); },
    });
  }

  function redraw(i) {
    const old = $("rep" + i);
    if (old) old.replaceWith(card(i, Number(old.dataset.rank)));
    renderScore();
  }

  function renderScore() { $("repcount").innerHTML = scoreLine(MUST_KNOW.map(it => answers[it.id]), MUST_KNOW.length); }

  function render() {
    const root = $("replist");
    root.innerHTML = "";
    let rank = 0;
    [...new Set(MUST_KNOW.map(it => it.week))].forEach(week => {
      const group = el("div", "repgroup");
      group.appendChild(el("h3", null, "Week " + week));
      const list = el("div", "qlist");
      MUST_KNOW.forEach((it, i) => { if (it.week === week) list.appendChild(card(i, ++rank)); });
      group.appendChild(list);
      root.appendChild(group);
    });
    renderScore();
  }

  function init() {
    Saved.set(SAVE_KEY, answers);   // stores progress in the id-keyed form if it was converted
    $("repreveal").addEventListener("click", e => {
      showAll = !showAll;
      e.currentTarget.setAttribute("aria-pressed", String(showAll));
      e.currentTarget.textContent = showAll ? "Hide answers" : "Show all answers";
      render();
    });
    confirmButton($("represet"), "Reset answers", "Tap again to clear", () => { answers = {}; Saved.set(SAVE_KEY, answers); render(); });
    render();
  }

  function progress() {
    const done = Object.keys(answers).filter(k => known.has(k) && answers[k] && answers[k].done);
    return { done: done.length, correct: done.filter(k => answers[k].ok).length, total: MUST_KNOW.length };
  }

  return { init, progress };
})();
