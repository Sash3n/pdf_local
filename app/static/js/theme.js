(function () {
  var root = document.documentElement;
  var toggle = document.getElementById("theme-toggle");
  var icon = document.getElementById("theme-toggle-icon");

  function syncIcon() {
    icon.textContent = root.classList.contains("dark") ? "light_mode" : "dark_mode";
  }

  syncIcon();

  toggle.addEventListener("click", function () {
    var isDark = root.classList.contains("dark");
    root.classList.remove(isDark ? "dark" : "light");
    root.classList.add(isDark ? "light" : "dark");
    localStorage.setItem("pdflocal-theme", isDark ? "light" : "dark");
    syncIcon();
  });
})();
