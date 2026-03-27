const toggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".site-nav");
const header = document.querySelector(".site-header");

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    nav.classList.toggle("is-open");
  });
}

if (header) {
  const syncHeaderState = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  };

  syncHeaderState();
  window.addEventListener("scroll", syncHeaderState, { passive: true });
}

document.querySelectorAll("[data-year]").forEach((node) => {
  node.textContent = new Date().getFullYear();
});

document.querySelectorAll("[data-tabs]").forEach((group) => {
  const tabs = Array.from(group.querySelectorAll("[data-tab-target]"));
  const panels = Array.from(group.querySelectorAll("[role='tabpanel']"));

  const activateTab = (tab) => {
    if (!tab) return;
    const targetId = tab.getAttribute("data-tab-target");

    tabs.forEach((item) => {
      const isActive = item === tab;
      item.classList.toggle("is-active", isActive);
      item.setAttribute("aria-selected", String(isActive));
      item.setAttribute("tabindex", isActive ? "0" : "-1");
    });

    panels.forEach((panel) => {
      const isActive = panel.id === targetId;
      panel.hidden = !isActive;
      panel.classList.toggle("is-active", isActive);
    });
  };

  const initialTab = tabs.find((tab) => tab.classList.contains("is-active")) || tabs[0];
  activateTab(initialTab);

  group.addEventListener("click", (event) => {
    const tab = event.target.closest("[data-tab-target]");
    if (!tab || !group.contains(tab)) return;
    activateTab(tab);
  });

  tabs.forEach((tab, index) => {
    tab.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowDown" && event.key !== "ArrowUp" && event.key !== "ArrowRight" && event.key !== "ArrowLeft" && event.key !== "Home" && event.key !== "End") {
        return;
      }

      event.preventDefault();

      let nextIndex = index;
      if (event.key === "ArrowDown" || event.key === "ArrowRight") {
        nextIndex = (index + 1) % tabs.length;
      } else if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
        nextIndex = (index - 1 + tabs.length) % tabs.length;
      } else if (event.key === "Home") {
        nextIndex = 0;
      } else if (event.key === "End") {
        nextIndex = tabs.length - 1;
      }

      activateTab(tabs[nextIndex]);
      tabs[nextIndex].focus();
    });
  });
});

/* ── Checklist form: Turnstile (explicit) + redirect then silent submit ── */

(function () {
  /* On the checklist page: render Turnstile via onload callback, gate submit */
  var turnstileToken = "";
  var form = document.getElementById("checklist-form");

  window.onTurnstileLoad = function () {
    var el = document.getElementById("checklist-turnstile");
    if (!el) return;
    turnstile.render(el, {
      sitekey: "0x4AAAAAACsaPQ59_pMzmZb4",
      callback: function (token) {
        turnstileToken = token;
      },
      "expired-callback": function () {
        turnstileToken = "";
      }
    });
  };

  if (form) {
    form.addEventListener("submit", function (e) {
      if (!turnstileToken) {
        e.preventDefault();
        alert("Please complete the verification challenge.");
      }
    });
  }

  /* On the thank-you page: read params, POST to Formspree, clean URL */
  if (window.location.pathname === "/checklist/thank-you/" || window.location.pathname === "/checklist/thank-you") {
    var params = new URLSearchParams(window.location.search);
    var name = params.get("name");
    var email = params.get("email");

    if (name && email) {
      var data = new FormData();
      data.append("name", name);
      data.append("email", email);

      fetch("https://formspree.io/f/mvzvgqjj", {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" }
      });

      history.replaceState(null, "", "/checklist/thank-you/");
    }
  }
})();

/* ── Exit-intent popup ── */

(function () {
  var EXCLUDED = ["/checklist/", "/checklist/thank-you/"];
  var STORAGE_KEY = "eb_exit_popup_seen";
  var MOBILE_DELAY = 30000;

  if (EXCLUDED.indexOf(window.location.pathname) !== -1) return;
  if (localStorage.getItem(STORAGE_KEY)) return;

  function buildPopup() {
    var overlay = document.createElement("div");
    overlay.className = "exit-popup-overlay";
    overlay.innerHTML =
      '<div class="exit-popup">' +
        '<button class="exit-popup-close" type="button" aria-label="Close">&times;</button>' +
        '<p class="eyebrow">Before you go</p>' +
        '<h2>Are your workflows ready for AI?</h2>' +
        '<p>Download the free Readiness Checklist to assess where your team stands before starting an implementation.</p>' +
        '<a class="button button-primary" href="/checklist/">Get the Checklist</a>' +
        '<button class="exit-popup-dismiss" type="button">No thanks</button>' +
      '</div>';
    document.body.appendChild(overlay);
    return overlay;
  }

  var overlay = null;

  function showPopup() {
    if (localStorage.getItem(STORAGE_KEY)) return;
    if (!overlay) overlay = buildPopup();
    overlay.classList.add("is-visible");
    localStorage.setItem(STORAGE_KEY, "1");

    overlay.querySelector(".exit-popup-close").addEventListener("click", closePopup);
    overlay.querySelector(".exit-popup-dismiss").addEventListener("click", closePopup);
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closePopup();
    });
  }

  function closePopup() {
    if (overlay) overlay.classList.remove("is-visible");
  }

  // Desktop: exit intent (mouse leaves viewport at top)
  document.addEventListener("mouseout", function (e) {
    if (!e.relatedTarget && e.clientY <= 0) {
      showPopup();
    }
  });

  // Mobile fallback: show after 30 seconds
  var isMobile = "ontouchstart" in window || navigator.maxTouchPoints > 0;
  if (isMobile) {
    setTimeout(showPopup, MOBILE_DELAY);
  }
})();
