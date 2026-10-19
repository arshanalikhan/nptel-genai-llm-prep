/* Week notes: shows one week at a time, remembers the last week opened and which weeks are
 * marked as reviewed, and adds a review button + previous/next week links under each week. */

const Notes = (() => {
  const REVIEWED_KEY = STORAGE_KEY + "-weeks";
  const CURRENT_KEY = STORAGE_KEY + "-curweek";
  const WEEK_IDS = [...document.querySelectorAll("#notes .week")].map(a => a.id);   // "w1" … "w7"
  let reviewed = Saved.get(REVIEWED_KEY, {});
  let current = Saved.get(CURRENT_KEY, "w1");
  if (!WEEK_IDS.includes(current)) current = "w1";

  function paintWeekNav() {
    document.querySelectorAll("#notes .weeknav a").forEach(a => {
      const id = a.getAttribute("href").slice(1);
      const on = id === current;
      a.classList.toggle("on", on);
      a.classList.toggle("done", !!reviewed[id]);
      if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
    });
  }

  /** Show one week ("w3"); with no argument, the last week the reader opened. */
  function show(id) {
    id = id || current;
    const changed = id !== current;
    current = id;
    Saved.set(CURRENT_KEY, id);
    document.querySelectorAll("#notes .week").forEach(a => {
      const on = a.id === id;
      a.hidden = !on;
      if (on && changed) { a.classList.remove("enter"); void a.offsetWidth; a.classList.add("enter"); }
    });
    paintWeekNav();
  }

  function addWeekFooters() {
    WEEK_IDS.forEach((id, i) => {
      const body = document.querySelector("#" + id + " .body");
      if (!body || body.querySelector(".weekfoot")) return;
      const foot = el("div", "weekfoot");

      const review = button("btn reviewbtn");
      const paint = () => {
        const on = !!reviewed[id];
        review.textContent = on ? "✓ Week reviewed" : "Mark week as reviewed";
        review.setAttribute("aria-pressed", String(on));
      };
      review.addEventListener("click", () => { reviewed[id] = !reviewed[id]; Saved.set(REVIEWED_KEY, reviewed); paint(); paintWeekNav(); });
      paint();

      const pager = el("div", "wkpager");
      if (i > 0) { const prev = el("a", "btn", "← Week " + WEEK_IDS[i - 1].slice(1)); prev.href = "#" + WEEK_IDS[i - 1]; pager.appendChild(prev); }
      const last = i === WEEK_IDS.length - 1;
      const next = el("a", "btn primary", last ? "Course map →" : "Week " + WEEK_IDS[i + 1].slice(1) + " →");
      next.href = last ? "#map" : "#" + WEEK_IDS[i + 1];
      pager.appendChild(next);

      foot.append(review, pager);
      body.appendChild(foot);
    });
  }

  function init() { addWeekFooters(); }

  /** For the home page. */
  function progress() {
    return { reviewed: WEEK_IDS.filter(id => reviewed[id]).length, total: WEEK_IDS.length, next: WEEK_IDS.find(id => !reviewed[id]), current };
  }

  return { init, show, progress };
})();
