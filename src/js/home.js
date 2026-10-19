/* Home page: exam countdowns, progress rings, today's study-plan phase, the "continue" button,
 * and the animated network drawn behind the hero heading. */

const Home = (() => {
  const $ = id => document.getElementById(id);

  /** Fill every countdown on the page: hero card, sidebar and the exam-facts strip. */
  function updateCountdowns() {
    const days = daysToExam();
    const big = (numId, labelId) => {
      const n = $(numId), l = $(labelId); if (!n || !l) return;
      if (days > 1) { n.textContent = days; l.textContent = "days to the exam"; }
      else if (days === 1) { n.textContent = "1"; l.textContent = "day to the exam"; }
      else if (days === 0) { n.textContent = "0"; l.textContent = "exam is today"; }
      else { n.textContent = "✓"; l.textContent = "exam day has passed"; }
    };
    big("cdnum", "cdlabel");
    big("sidecd", "sidecdl");
    const small = $("countdown");
    if (small) small.textContent = days > 1 ? days + " days to go" : days === 1 ? "Tomorrow" : days === 0 ? "Today" : "Exam day has passed";
  }

  function renderStats() {
    const box = $("stats"); if (!box) return;
    const weeks = Notes.progress(), practice = Practice.progress(), must = MustKnow.progress(), best = MockExams.bestScore();
    const pct = p => p.done ? Math.round(p.correct * 100 / p.done) + "% correct so far" : "not started yet";
    const cards = [
      { icon: "calendar-check", href: "#" + (weeks.next || weeks.current), label: "Weeks reviewed", value: weeks.reviewed + "/" + weeks.total,
        sub: weeks.next ? "next up: week " + weeks.next.slice(1) : "all " + weeks.total + " done", fill: weeks.reviewed / weeks.total },
      { icon: "list-checks", href: "#practice", label: "Practice", value: practice.done + "/" + practice.total, sub: pct(practice), fill: practice.done / practice.total },
      { icon: "repeat", href: "#repeated", label: "Must-know", value: must.done + "/" + must.total, sub: pct(must), fill: must.done / must.total },
      { icon: "timer", href: "#mock", label: "Best mock score", value: best >= 0 ? best + "/100" : "—",
        sub: best >= 0 ? (best >= PASS_MARK ? "above the " + PASS_MARK + "/100 pass line" : "pass line is " + PASS_MARK + "/100") : "no paper finished yet",
        fill: Math.max(0, best) / 100, good: best >= PASS_MARK },
    ];
    box.innerHTML = "";
    const C = 2 * Math.PI * 26, rings = [];
    cards.forEach(c => {
      const a = el("a", "stat" + (c.good ? " good" : "")); a.href = c.href;
      const ring = el("span", "ring");
      ring.innerHTML = '<svg viewBox="0 0 64 64" aria-hidden="true"><circle class="rt" cx="32" cy="32" r="26"/><circle class="rf" cx="32" cy="32" r="26" stroke-dasharray="' + C.toFixed(2) + '" stroke-dashoffset="' + C.toFixed(2) + '"/></svg><i data-lucide="' + c.icon + '"></i>';
      const text = el("span", "sx");
      text.append(el("span", "l", c.label), el("span", "v", c.value), el("span", "s", c.sub));
      a.append(ring, text);
      box.appendChild(a);
      rings.push([ring.querySelector(".rf"), Math.min(1, c.fill)]);
    });
    drawIcons();
    // fill the rings on the next frame so the transition animates
    requestAnimationFrame(() => requestAnimationFrame(() => rings.forEach(([r, p]) => { r.style.strokeDashoffset = (C * (1 - p)).toFixed(2); })));
  }

  /** Highlight today's phase of the study plan (dates in data/course.json). */
  function highlightToday() {
    const today = todayInIndia();
    const phase = COURSE.studyPlan.findIndex(p => today >= p.from && today <= p.to);
    const days = [...document.querySelectorAll("#home .days .day")];
    days.forEach((d, i) => {
      d.classList.toggle("today", i === phase);
      const when = d.querySelector(".when");
      let badge = when.querySelector(".todaybadge");
      if (i === phase && !badge) when.appendChild(el("span", "todaybadge", "Today"));
      if (i !== phase && badge) badge.remove();
    });
    const focus = $("todayFocus");
    if (focus) {
      focus.hidden = phase < 0;
      if (phase >= 0) { focus.innerHTML = ""; focus.append(el("span", "tf-l", "Today"), el("span", "tf-v", days[phase].querySelector("h3").textContent + " — see the plan")); }
    }
  }

  function updateContinueButton() {
    const cta = $("cta-notes"); if (!cta) return;
    const weeks = Notes.progress();
    const target = weeks.next || weeks.current;
    cta.href = "#" + target;
    cta.textContent = weeks.reviewed === 0 && weeks.current === "w1" ? "Start week notes" : "Continue: week " + target.slice(1);
  }

  function render() {
    renderStats();
    highlightToday();
    updateContinueButton();
    updateCountdowns();
  }

  /* Animated network behind the hero heading: three rows of nodes with packets moving upward.
     Drawn only while Home is visible, and kept still for readers who prefer reduced motion. */
  const animation = (() => {
    const canvas = document.querySelector(".hero-net");
    if (!canvas || !canvas.getContext) return () => {};
    const ctx = canvas.getContext("2d");
    let raf = 0, running = false, visible = false, nodes = [], links = [], packets = [], W = 0, H = 0, color = "#0b6a87";
    const readColor = () => { color = getComputedStyle(document.documentElement).getPropertyValue("--accent").trim() || color; };

    function layout() {
      const r = canvas.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
      W = r.width; H = r.height;
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      // keep the network in the right-hand column, clear of the heading and intro text
      const main = document.querySelector(".hero-main");
      const x0 = main ? main.getBoundingClientRect().right - r.left + 28 : W * 0.6, x1 = W - 20;
      nodes = []; links = []; packets = [];
      if (W < 760 || x1 - x0 < 140) return;
      const row = (n, y, radius) => Array.from({ length: n }, (_, i) => ({ x: x0 + (x1 - x0) * (n === 1 ? 0.5 : i / (n - 1)), y, r: radius }));
      const top = row(3, H * 0.14, 5), mid = row(4, H * 0.5, 3.6), low = row(7, H * 0.86, 2.6);
      nodes = [...top, ...mid, ...low];
      low.forEach((n, i) => links.push([n, mid[Math.min(3, Math.floor(i / 2))]]));
      mid.forEach((n, i) => links.push([n, top[Math.min(2, Math.round(i * 2 / 3))]]));
    }

    function frame() {
      ctx.clearRect(0, 0, W, H);
      ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 1;
      ctx.globalAlpha = 0.22; links.forEach(([a, b]) => { ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); });
      ctx.globalAlpha = 0.55; nodes.forEach(n => { ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2); ctx.fill(); });
      if (running && links.length && packets.length < 16 && Math.random() < 0.09) {
        packets.push({ link: links[Math.floor(Math.random() * links.length)], p: 0, speed: 0.004 + Math.random() * 0.006 });
      }
      ctx.globalAlpha = 0.9;
      packets = packets.filter(k => {
        k.p += k.speed; if (k.p >= 1) return false;
        const [a, b] = k.link;
        ctx.beginPath(); ctx.arc(a.x + (b.x - a.x) * k.p, a.y + (b.y - a.y) * k.p, 2.2, 0, Math.PI * 2); ctx.fill();
        return true;
      });
      ctx.globalAlpha = 1;
      if (running) raf = requestAnimationFrame(frame);
    }

    function start() {
      readColor(); layout();
      if (REDUCED_MOTION || !links.length) { stop(); frame(); return; }
      if (!running) { running = true; raf = requestAnimationFrame(frame); }
    }
    function stop() { running = false; cancelAnimationFrame(raf); }

    window.addEventListener("resize", () => { if (visible) start(); });
    document.addEventListener("visibilitychange", () => { if (document.hidden) stop(); else if (visible) start(); });
    document.addEventListener("themechange", () => { readColor(); if (!running) frame(); });
    return on => { visible = on; if (on) start(); else stop(); };
  })();

  return { render, updateCountdowns, animate: animation };
})();
