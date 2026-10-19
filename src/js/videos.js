/* Videos page: one card per course week (a player once that week's video is published),
 * a shared playback-speed setting, and a "Watch the Week N video" button on each week's notes. */

const Videos = (() => {
  const SPEED_KEY = STORAGE_KEY + "-vspeed";
  const SPEEDS = [1, 1.25, 1.5, 1.75];
  let speed = Saved.get(SPEED_KEY, 1);
  const $ = id => document.getElementById(id);
  const published = week => VIDEOS.find(v => v.week === week);
  const players = () => [...document.querySelectorAll("#vgrid video")];

  function setSpeed(s) { speed = s; Saved.set(SPEED_KEY, s); }

  function renderSpeed() {
    const box = $("vspeed");
    box.innerHTML = "";
    SPEEDS.forEach(s => {
      const b = button("chip", s + "×", () => { setSpeed(s); players().forEach(v => { v.playbackRate = s; }); renderSpeed(); });
      b.setAttribute("aria-pressed", String(s === speed));
      box.appendChild(b);
    });
  }

  function render() {
    const grid = $("vgrid");
    grid.innerHTML = "";
    COURSE.weeks.forEach(({ week, title }) => {
      const video = published(week);
      const card = el("article", "vcard"); card.id = "vid-" + week;
      const head = el("div", "vhead");
      const text = el("div");
      text.append(el("h3", null, title), el("p", "vmeta", video ? video.duration + " · Hinglish" : "coming soon"));
      const notes = el("a", "btn", "Notes"); notes.href = "#w" + week;
      head.append(el("span", "vnum", "W" + week), text, notes);
      card.appendChild(head);

      if (video) {
        const v = document.createElement("video");
        v.controls = true; v.preload = "none"; v.playsInline = true; v.src = video.file; v.poster = video.poster;
        v.addEventListener("play", () => { v.playbackRate = speed; players().forEach(o => { if (o !== v) o.pause(); }); });
        v.addEventListener("ratechange", () => {   // speed changed from the player's own menu
          if (SPEEDS.includes(v.playbackRate) && v.playbackRate !== speed) { setSpeed(v.playbackRate); renderSpeed(); }
        });
        card.appendChild(v);
      } else {
        const soon = el("div", "vsoon");
        soon.innerHTML = '<i data-lucide="clock"></i><span>Being made · check back soon</span>';
        card.appendChild(soon);
      }
      grid.appendChild(card);
    });
    $("vcount").textContent = VIDEOS.length + " of " + WEEK_COUNT + " weeks published";
    renderSpeed();
    drawIcons();
  }

  /** Put a "Watch the Week N video" button under each week's notes heading. */
  function addWatchButtons() {
    VIDEOS.forEach(video => {
      const body = document.querySelector("#w" + video.week + " .body");
      if (!body || body.querySelector(".watchbtn")) return;
      const a = el("a", "btn primary watchbtn"); a.href = "#v" + video.week;
      a.innerHTML = '<i data-lucide="circle-play"></i><span></span>';
      a.querySelector("span").textContent = "Watch the Week " + video.week + " video (" + video.duration + ")";
      body.querySelector("h3").insertAdjacentElement("afterend", a);
    });
  }

  /** Highlight one week's card (route #vN). */
  function focus(targetId) {
    document.querySelectorAll(".vcard.focus").forEach(x => x.classList.remove("focus"));
    const t = targetId && $(targetId);
    if (t) t.classList.add("focus");
  }

  function init() { render(); addWatchButtons(); }

  return { init, focus };
})();
