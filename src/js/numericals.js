/* Numericals page: "Open all workings" button for the worked examples. */

const Numericals = (() => {
  function init() {
    const toggle = document.getElementById("wxAll");
    if (!toggle) return;
    toggle.addEventListener("click", () => {
      const workings = [...document.querySelectorAll("#formulas details.wsol")];
      const open = !workings.every(d => d.open);
      workings.forEach(d => { d.open = open; });
      toggle.textContent = open ? "Close all workings" : "Open all workings";
    });
  }
  return { init };
})();
