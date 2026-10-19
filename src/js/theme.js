/* Light / dark switch. The saved choice is applied before first paint by the inline script in <head>;
 * with no saved choice the site follows the system setting. Fires a "themechange" event on document. */

const Theme = (() => {
  const SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  const MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  const root = document.documentElement;
  const system = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  const buttons = [...document.querySelectorAll(".themebtn")];

  function current() {
    const t = root.getAttribute("data-theme");
    if (t === "light" || t === "dark") return t;
    return system && system.matches ? "dark" : "light";
  }

  function paint() {
    const dark = current() === "dark";
    buttons.forEach(btn => {
      btn.innerHTML = (dark ? SUN : MOON) + "<span>" + (dark ? "Light mode" : "Dark mode") + "</span>";
      btn.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    });
  }

  function init() {
    buttons.forEach(btn => btn.addEventListener("click", () => {
      const next = current() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      Saved.setText(THEME_KEY, next);
      paint();
      document.dispatchEvent(new Event("themechange"));
    }));
    if (system && system.addEventListener) {
      system.addEventListener("change", () => { paint(); document.dispatchEvent(new Event("themechange")); });
    }
    paint();
  }

  return { init };
})();
