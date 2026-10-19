/* Navigation: one <section class="page"> is shown at a time, picked by the URL hash.
 *   #home, #notes, #practice …   a page
 *   #w3                          week 3 of the notes
 *   #v3                          week 3's video
 *   #plan, #sources, #poster     a spot inside a page (see ALIASES)
 * Also handles the phone "More" sheet, the previous/next pager, the sticky-bar height and back-to-top. */

const Router = (() => {
  // Order = sidebar order = previous/next pager order. Section ids are kept short for stable links.
  const PAGES = [
    ["home", "Home"], ["notes", "Week notes"], ["videos", "Videos"], ["map", "Course map"],
    ["formulas", "Numericals"], ["repeated", "Must-know"], ["practice", "Practice"],
    ["mock", "Mock exams"], ["traps", "Last-minute traps"], ["resources", "Videos & sources"],
  ];
  const PAGE_IDS = PAGES.map(p => p[0]);
  const PAGE_NAME = Object.fromEntries(PAGES);
  const MORE_SHEET_PAGES = ["map", "formulas", "repeated", "traps", "resources"];   // phone: behind "More"
  const ALIASES = { plan: ["home", "plan"], lectures: ["resources", "videos-block"], sources: ["resources", "sources-block"], poster: ["map", null] };
  const weekLink = /^([wv])(\d+)$/;
  let current = null;
  const $ = id => document.getElementById(id);

  function hashNow() { try { return decodeURIComponent((location.hash || "").slice(1)); } catch (e) { return ""; } }
  function isWeekLink(h) { const m = weekLink.exec(h); return !!m && +m[2] >= 1 && +m[2] <= WEEK_COUNT; }
  function isRoute(h) { return PAGE_IDS.includes(h) || !!ALIASES[h] || isWeekLink(h); }

  /* ---------- Phone "More" sheet ---------- */
  function openSheet() { $("moreSheet").hidden = false; $("moreBtn").setAttribute("aria-expanded", "true"); }
  function closeSheet() { const s = $("moreSheet"); if (!s || s.hidden) return; s.hidden = true; $("moreBtn").setAttribute("aria-expanded", "false"); }

  function renderPager(page) {
    const nav = $("pager"); if (!nav) return;
    nav.innerHTML = "";
    const i = PAGE_IDS.indexOf(page);
    if (i > 0) {
      const p = el("a", "pg prev"); p.href = "#" + PAGE_IDS[i - 1];
      p.append(el("span", "l", "Previous"), el("span", "n", "← " + PAGE_NAME[PAGE_IDS[i - 1]]));
      nav.appendChild(p);
    }
    if (i < PAGE_IDS.length - 1) {
      const n = el("a", "pg next"); n.href = "#" + PAGE_IDS[i + 1];
      n.append(el("span", "l", "Next"), el("span", "n", PAGE_NAME[PAGE_IDS[i + 1]] + " →"));
      nav.appendChild(n);
    }
  }

  /** Show the page for a hash (or the current URL hash). */
  function route(hashIn) {
    const h = hashIn == null ? hashNow() : hashIn;
    let page = h || "home", target = null, week = null;
    const m = weekLink.exec(h);
    if (m && isWeekLink(h)) {
      if (m[1] === "w") { page = "notes"; week = h; } else { page = "videos"; target = "vid-" + m[2]; }
    } else if (ALIASES[h]) {
      [page, target] = ALIASES[h];
    }
    if (!PAGE_IDS.includes(page)) page = "home";

    const pageChanged = current !== page;
    const animate = pageChanged && current !== null && !!document.startViewTransition && !REDUCED_MOTION && document.visibilityState === "visible";
    let applied = false;
    const apply = () => {
      if (applied) return;
      applied = true;
      if (page === "notes") Notes.show(week);
      document.querySelectorAll("main > section.page").forEach(s => {
        const on = s.id === page;
        s.hidden = !on;
        if (on && pageChanged && !animate) { s.classList.remove("enter"); void s.offsetWidth; s.classList.add("enter"); }
      });
      document.querySelectorAll("[data-page]").forEach(a => {
        const on = a.dataset.page === page;
        a.classList.toggle("on", on);
        if (on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
      });
      $("moreBtn").classList.toggle("on", MORE_SHEET_PAGES.includes(page));
      $("topTitle").textContent = PAGE_NAME[page];
      closeSheet();
      renderPager(page);
      current = page;
      if (page === "home") Home.render();
      if (page === "videos") Videos.focus(target);
      Home.animate(page === "home");
      document.title = (page === "home" ? "" : PAGE_NAME[page] + " · ") + SITE_NAME;
      const t = target ? $(target) : null;
      if (t) t.scrollIntoView(); else window.scrollTo({ top: 0, behavior: "instant" });
    };
    if (animate) {
      // never let the animation hold up navigation: if it hasn't run shortly, switch pages directly
      try {
        const vt = document.startViewTransition(apply);
        [vt.ready, vt.finished, vt.updateCallbackDone].forEach(p => p && p.catch(() => {}));   // skipping rejects these; that's expected
        setTimeout(() => { if (!applied) { try { vt.skipTransition(); } catch (e) {} apply(); } }, 400);
      } catch (e) { apply(); }
    } else {
      apply();
    }
  }

  // Page switches never depend on the URL changing (some embedded viewers ignore hash changes);
  // the URL is updated when the browser allows it, so links and the back button still work.
  function go(h) {
    route(h);
    try { if (hashNow() !== h) history.pushState({ h }, "", "#" + h); } catch (e) {}
  }

  function init() {
    document.addEventListener("click", e => {
      const a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) return;
      const h = a.getAttribute("href").slice(1);
      if (!isRoute(h)) return;
      e.preventDefault();
      go(h);
    });

    $("moreBtn").addEventListener("click", () => { $("moreSheet").hidden ? openSheet() : closeSheet(); });
    $("moreSheet").addEventListener("click", e => { if (e.target.id === "moreSheet") closeSheet(); });
    document.addEventListener("keydown", e => { if (e.key === "Escape") closeSheet(); });

    // Sticky elements sit below the phone top bar: expose its height as --navh.
    const topbar = document.querySelector(".topbar");
    const setNavHeight = () => document.documentElement.style.setProperty("--navh", topbar.offsetHeight + "px");
    setNavHeight();
    window.addEventListener("resize", setNavHeight);

    // Back-to-top button (hidden while sitting a mock paper)
    const up = $("totop");
    const onScroll = () => up.classList.toggle("show", window.scrollY > 900 && !MockExams.isRunning());
    window.addEventListener("scroll", onScroll, { passive: true });
    up.addEventListener("click", () => window.scrollTo({ top: 0 }));
    onScroll();

    window.addEventListener("hashchange", () => route());
    window.addEventListener("popstate", () => route());
    route();
  }

  return { init, go };
})();
