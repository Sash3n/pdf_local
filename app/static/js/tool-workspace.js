(function () {
  const root = document.getElementById("tool-workspace");
  if (!root) return;

  const config = JSON.parse(document.getElementById("tool-config").textContent);
  const form = document.getElementById("tool-form");
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const browseBtn = document.getElementById("browse-btn");
  const queueSection = document.getElementById("queue");
  const fileGrid = document.getElementById("file-grid");
  const fileCountEl = document.getElementById("file-count");
  const fileCountLabelEl = document.getElementById("file-count-label");
  const combinedSizeEl = document.getElementById("combined-size");
  const actionBtn = document.getElementById("action-btn");
  const actionBtnLabel = document.getElementById("action-btn-label");
  const resultPanel = document.getElementById("result-panel");
  const clearAllBtn = document.getElementById("clear-all-btn");

  let files = [];

  function formatSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  }

  function syncFileInput() {
    const dt = new DataTransfer();
    files.forEach((f) => dt.items.add(f));
    fileInput.files = dt.files;
  }

  function renderFiles() {
    fileGrid.innerHTML = "";
    files.forEach((file, index) => {
      const card = document.createElement("div");
      card.className =
        "group relative bg-white dark:bg-surface-container-high rounded-2xl p-4 shadow-sm border border-outline-variant/10";
      card.draggable = config.multiple;
      card.dataset.index = String(index);

      card.innerHTML = `
        <button type="button" class="absolute top-2 right-2 p-1.5 bg-white/90 dark:bg-inverse-surface rounded-full text-error shadow-sm hover:bg-error hover:text-white transition-colors" data-remove="${index}">
          <span class="material-symbols-outlined text-sm">close</span>
        </button>
        <div class="flex items-center gap-3">
          <span class="material-symbols-outlined text-primary text-3xl">description</span>
          <div class="overflow-hidden">
            <h5 class="font-title-md text-body-sm text-primary dark:text-inverse-on-surface truncate">${file.name}</h5>
            <p class="text-[12px] text-slate-gray">${formatSize(file.size)}</p>
          </div>
        </div>
      `;
      fileGrid.appendChild(card);
    });

    queueSection.classList.toggle("hidden", files.length === 0);
    fileCountEl.textContent = `${files.length} ${files.length === 1 ? "FILE" : "FILES"}`;
    const totalBytes = files.reduce((sum, f) => sum + f.size, 0);
    if (files.length === 0) {
      fileCountLabelEl.textContent = "Select files to begin";
      combinedSizeEl.textContent = "";
    } else {
      fileCountLabelEl.textContent = `${files.length} ${files.length === 1 ? "Document" : "Documents"} Selected`;
      combinedSizeEl.textContent = `Combined size: ${formatSize(totalBytes)}`;
    }
    actionBtn.disabled = files.length === 0;
  }

  function addFiles(fileList) {
    const incoming = Array.from(fileList);
    if (config.multiple) {
      files = files.concat(incoming);
    } else {
      files = incoming.slice(0, 1);
    }
    syncFileInput();
    renderFiles();
  }

  fileGrid.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-remove]");
    if (!btn) return;
    const index = Number(btn.dataset.remove);
    files.splice(index, 1);
    syncFileInput();
    renderFiles();
  });

  let dragSrcIndex = null;
  fileGrid.addEventListener("dragstart", (e) => {
    const card = e.target.closest("[data-index]");
    if (!card) return;
    dragSrcIndex = Number(card.dataset.index);
    card.classList.add("opacity-50");
  });
  fileGrid.addEventListener("dragend", (e) => {
    const card = e.target.closest("[data-index]");
    if (card) card.classList.remove("opacity-50");
  });
  fileGrid.addEventListener("dragover", (e) => e.preventDefault());
  fileGrid.addEventListener("drop", (e) => {
    e.preventDefault();
    const card = e.target.closest("[data-index]");
    if (!card || dragSrcIndex === null) return;
    const targetIndex = Number(card.dataset.index);
    const [moved] = files.splice(dragSrcIndex, 1);
    files.splice(targetIndex, 0, moved);
    dragSrcIndex = null;
    syncFileInput();
    renderFiles();
  });

  clearAllBtn.addEventListener("click", () => {
    files = [];
    syncFileInput();
    renderFiles();
  });

  browseBtn.addEventListener("click", () => fileInput.click());
  dropZone.addEventListener("click", (e) => {
    if (e.target === browseBtn) return;
    fileInput.click();
  });
  fileInput.addEventListener("change", () => addFiles(fileInput.files));

  ["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.add("drag-over");
    });
  });
  ["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.remove("drag-over");
    });
  });
  dropZone.addEventListener("drop", (e) => addFiles(e.dataTransfer.files));

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    actionBtn.disabled = true;
    const originalLabel = actionBtnLabel.textContent;
    actionBtnLabel.textContent = "Processing...";
    resultPanel.classList.add("hidden");

    try {
      const formData = new FormData(form);
      const response = await fetch(config.endpoint, { method: "POST", body: formData });
      await handleToolResponse(response, resultPanel);
    } catch (err) {
      showToolResult(resultPanel, `<p class="font-body-sm">Something went wrong: ${err.message}</p>`, true);
    } finally {
      actionBtn.disabled = files.length === 0;
      actionBtnLabel.textContent = originalLabel;
    }
  });
})();
