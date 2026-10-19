/* Small helpers shared by every page module: saved state, DOM building, dates, random numbers,
 * and the question card used by Practice and Must-know. */

/* ---------- Saved state (localStorage; silently does nothing when storage is blocked) ---------- */
const Saved = {
  get(key, fallback) {
    try { const v = JSON.parse(localStorage.getItem(key)); return v == null ? fallback : v; } catch (e) { return fallback; }
  },
  set(key, value) {
    try { if (value == null) localStorage.removeItem(key); else localStorage.setItem(key, JSON.stringify(value)); } catch (e) {}
  },
  getText(key, fallback) {
    try { return localStorage.getItem(key) || fallback; } catch (e) { return fallback; }
  },
  setText(key, value) {
    try { localStorage.setItem(key, value); } catch (e) {}
  },
};

/** Saved answers are keyed by question id. Progress saved before ids existed was keyed by list
 *  position ("0", "1", …); convert it once, using the order the questions had then. */
function keyedById(saved, list) {
  if (!saved || !Object.keys(saved).some(k => /^\d+$/.test(k))) return saved || {};
  const out = {};
  Object.entries(saved).forEach(([k, v]) => {
    const item = /^\d+$/.test(k) ? list[Number(k)] : null;
    out[item ? item.id : k] = v;
  });
  return out;
}

const QUESTION_BY_ID = Object.fromEntries(QUESTIONS.map(q => [q.id, q]));

/* ---------- DOM ---------- */
/** Create an element with an optional class name and text. */
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
}

/** A <button type="button">. */
function button(className, text, onClick) {
  const b = el("button", className, text);
  b.type = "button";
  if (onClick) b.addEventListener("click", onClick);
  return b;
}

/** A button that needs a second tap within 3 seconds (for destructive actions like "Reset"). */
function confirmButton(btn, label, armedLabel, action) {
  let timer = null;
  btn.addEventListener("click", () => {
    if (!timer) {
      btn.textContent = armedLabel;
      timer = setTimeout(() => { timer = null; btn.textContent = label; }, 3000);
      return;
    }
    clearTimeout(timer); timer = null; btn.textContent = label; action();
  });
}

/** Turn the <i data-lucide> placeholders into icons (the icon library loads asynchronously). */
function drawIcons() { if (window.refreshIcons) window.refreshIcons(); }

const REDUCED_MOTION = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);

/* ---------- Dates (the exam runs on India time) ---------- */
function todayInIndia() { return new Date(Date.now() + 5.5 * 3600e3).toISOString().slice(0, 10); }
function daysToExam() {
  const [y, m, d] = EXAM_DAY.split("-").map(Number);
  const [ty, tm, td] = todayInIndia().split("-").map(Number);
  return Math.round((Date.UTC(y, m - 1, d) - Date.UTC(ty, tm - 1, td)) / 86400000);
}

/* ---------- Random numbers (seeded, so fixed mock papers come out the same every time) ---------- */
function seededRandom(seed) {
  return function () {
    seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function shuffled(list, random) {
  const a = list.slice();
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}
function sameSet(a, b) { return a.slice().sort().join() === b.slice().sort().join(); }

/* ---------- Answering ---------- */
/** Apply a pick to a saved answer state {sel, done, ok}. One-answer questions are marked straight away;
 *  "select all" questions toggle the option until Check is pressed. */
function pickOption(state, option, answer) {
  const st = state || { sel: [], done: false };
  if (st.done) return st;
  if (answer.length === 1) return { sel: [option], done: true, ok: option === answer[0] };
  st.sel = st.sel.includes(option) ? st.sel.filter(x => x !== option) : st.sel.concat(option);
  return st;
}
function checkAnswer(state, answer) {
  if (!state || !state.sel.length) return state;
  return { sel: state.sel, done: true, ok: sameSet(state.sel, answer) };
}

/* ---------- Question card pieces ---------- */
function optionButton(index, text) {
  const b = button("opt");
  b.append(el("span", "key", LETTERS[index]), el("span", null, text));
  return b;
}

/** The "Answer B  explanation" box shown under a marked question. */
function answerBox(answer, label, text) {
  const box = el("p", "why");
  box.append(el("b", null, "Answer " + answer.map(a => LETTERS[a]).join(", ")));
  if (label) box.append(el("b", null, label));
  box.append(document.createTextNode(text || ""));
  return box;
}

/**
 * A clickable question card (Practice and Must-know).
 * @param {object} c
 *   id, data      element id and data-* attributes (used to redraw the card in place)
 *   meta          array of strings or [className, text] pairs shown above the question
 *   question, options, answer, explanation, explanationLabel
 *   state         saved {sel, done, ok}
 *   showAnswer    true to show the answer even if not attempted ("Show all answers")
 *   onPick(k), onCheck()
 */
function questionCard(c) {
  const st = c.state || { sel: [], done: false };
  const multi = c.answer.length > 1;
  const show = st.done || c.showAnswer;
  const card = el("article", "q");
  card.id = c.id;
  Object.entries(c.data || {}).forEach(([k, v]) => { card.dataset[k] = v; });

  const meta = el("div", "q-meta");
  c.meta.concat([multi ? "Select all that apply" : "One answer"]).forEach(m => {
    meta.appendChild(Array.isArray(m) ? el("span", m[0], m[1]) : el("span", null, m));
  });
  card.append(meta, el("p", "q-text", c.question));

  const opts = el("div", "opts");
  c.options.forEach((text, k) => {
    const b = optionButton(k, text);
    const picked = st.sel.includes(k);
    b.setAttribute("aria-pressed", String(picked && !show));
    if (show) {
      b.disabled = true;
      if (c.answer.includes(k)) b.classList.add("correct");
      else if (picked) b.classList.add("wrong");
    } else {
      b.addEventListener("click", () => c.onPick(k));
    }
    opts.appendChild(b);
  });
  card.appendChild(opts);

  const foot = el("div", "q-foot");
  if (multi && !show) {
    const check = button("btn primary", "Check", () => c.onCheck());
    check.disabled = st.sel.length === 0;
    foot.appendChild(check);
  }
  if (st.done) foot.appendChild(el("span", "verdict " + (st.ok ? "ok" : "no"), st.ok ? "Correct" : "Not quite"));
  if (foot.childNodes.length) card.appendChild(foot);

  if (show) card.appendChild(answerBox(c.answer, c.explanationLabel, c.explanation));
  return card;
}

/** "12/40 answered · 9 correct (75%)" for a set of saved states. */
function scoreLine(states, total) {
  let done = 0, ok = 0;
  states.forEach(s => { if (s && s.done) { done++; if (s.ok) ok++; } });
  return "<b>" + done + "</b>/" + total + " answered · <b>" + ok + "</b> correct" + (done ? " (" + Math.round(ok * 100 / done) + "%)" : "");
}
