document.addEventListener("DOMContentLoaded", function() {
  const tabs = document.querySelectorAll(".tab-button");
  const panels = document.querySelectorAll(".tab-panel");

  function setActive(targetId) {
    const active = Array.from(tabs).find(tab => tab.dataset.target === targetId);
    if (!active) return;

    tabs.forEach(tab => {
      const isActive = tab.dataset.target === targetId;
      tab.classList.toggle("active", isActive);
      tab.setAttribute("aria-selected", String(isActive));
      tab.setAttribute("tabindex", isActive ? "0" : "-1");
    });

    panels.forEach(panel => {
      const isActive = panel.id === targetId;
      panel.classList.toggle("active", isActive);
      panel.style.display = isActive ? "block" : "none";
      panel.setAttribute("aria-hidden", String(!isActive));
    });

    document.body.dataset.design = active?.dataset.design || "home";

    if (active && active.dataset.accent) {
      document.documentElement.style.setProperty('--accent', active.dataset.accent);
      document.documentElement.style.setProperty('--accent-rgb', hexToRgb(active.dataset.accent));
    }
  }

  function hexToRgb(hex) {
    const clean = hex.replace('#', '');
    const full = clean.length === 3
      ? clean.split('').map(ch => ch + ch).join('')
      : clean;

    const num = parseInt(full, 16);
    const r = (num >> 16) & 255;
    const g = (num >> 8) & 255;
    const b = num & 255;

    return `${r}, ${g}, ${b}`;
  }

  tabs.forEach(tab => {
    tab.setAttribute("aria-controls", tab.dataset.target);

    tab.addEventListener("click", function() {
      setActive(this.dataset.target);
      history.pushState(null, "", `#${this.dataset.target}`);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    tab.addEventListener("keydown", function(event) {
      if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") return;

      event.preventDefault();
      const index = Array.from(tabs).indexOf(this);
      const direction = event.key === "ArrowRight" ? 1 : -1;
      const nextTab = tabs[(index + direction + tabs.length) % tabs.length];
      setActive(nextTab.dataset.target);
      nextTab.focus();
      history.pushState(null, "", `#${nextTab.dataset.target}`);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  const hashTarget = window.location.hash.slice(1);
  const initialTab = Array.from(tabs).find(tab => tab.dataset.target === hashTarget)
    || document.querySelector('.tab-button.active')
    || tabs[0];
  if (initialTab) {
    tabs.forEach(tab => tab.setAttribute("role", "tab"));
    panels.forEach(panel => panel.setAttribute("role", "tabpanel"));
    const tabList = document.querySelector(".nav-tabs");
    tabList?.setAttribute("role", "tablist");
    setActive(initialTab.dataset.target);
  }

  function syncFromHash() {
    const targetId = window.location.hash.slice(1);
    if (Array.from(tabs).some(tab => tab.dataset.target === targetId)) {
      setActive(targetId);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  window.addEventListener("hashchange", syncFromHash);
  window.addEventListener("popstate", syncFromHash);
});
