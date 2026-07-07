(function () {
  const root = document.getElementById("sign-workspace");
  if (!root) return;

  const pdfDropZone = document.getElementById("pdf-drop-zone");
  const pdfInput = document.getElementById("pdf-input");
  const pdfBrowseBtn = document.getElementById("pdf-browse-btn");
  const pdfDropLabel = document.getElementById("pdf-drop-label");
  const pdfStatus = document.getElementById("pdf-status");
  const signBtn = document.getElementById("sign-btn");
  const signBtnLabel = document.getElementById("sign-btn-label");
  const resultPanel = document.getElementById("result-panel");
  const canvas = document.getElementById("sign-canvas");
  const ctx = canvas.getContext("2d");
  const clearCanvasBtn = document.getElementById("clear-canvas-btn");
  const boxFields = document.querySelectorAll("[data-box-field]");
  const pointFields = document.querySelectorAll("[data-point-field]");

  let pdfFile = null;
  let mode = "draw";
  let hasDrawn = false;

  function updatePdfStatus() {
    pdfStatus.textContent = pdfFile ? `Ready to sign: ${pdfFile.name}` : "Select a PDF to begin";
    signBtn.disabled = !pdfFile;
  }

  pdfBrowseBtn.addEventListener("click", () => pdfInput.click());
  pdfDropZone.addEventListener("click", (e) => {
    if (e.target === pdfBrowseBtn) return;
    pdfInput.click();
  });
  pdfInput.addEventListener("change", () => {
    if (pdfInput.files[0]) {
      pdfFile = pdfInput.files[0];
      pdfDropLabel.textContent = pdfFile.name;
      updatePdfStatus();
    }
  });
  ["dragenter", "dragover"].forEach((eventName) => {
    pdfDropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      pdfDropZone.classList.add("drag-over");
    });
  });
  ["dragleave", "drop"].forEach((eventName) => {
    pdfDropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      pdfDropZone.classList.remove("drag-over");
    });
  });
  pdfDropZone.addEventListener("drop", (e) => {
    if (e.dataTransfer.files[0]) {
      pdfFile = e.dataTransfer.files[0];
      pdfDropLabel.textContent = pdfFile.name;
      updatePdfStatus();
    }
  });

  document.querySelectorAll(".mode-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      mode = tab.dataset.mode;
      document.querySelectorAll(".mode-tab").forEach((t) => {
        t.classList.toggle("bg-privacy-blue", t === tab);
        t.classList.toggle("text-primary", t === tab);
        t.classList.toggle("text-slate-gray", t !== tab);
      });
      document.querySelectorAll("[data-panel]").forEach((panel) => {
        const panels = panel.dataset.panel.split(" ");
        panel.classList.toggle("hidden", !panels.includes(mode));
      });
      const isPoint = mode === "type";
      boxFields.forEach((f) => f.classList.toggle("hidden", isPoint));
      pointFields.forEach((f) => f.classList.toggle("hidden", !isPoint));
    });
  });

  let drawing = false;
  canvas.addEventListener("pointerdown", (e) => {
    drawing = true;
    hasDrawn = true;
    const rect = canvas.getBoundingClientRect();
    ctx.beginPath();
    ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
  });
  canvas.addEventListener("pointermove", (e) => {
    if (!drawing) return;
    const rect = canvas.getBoundingClientRect();
    ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
    ctx.strokeStyle = "#131f5d";
    ctx.lineWidth = 2;
    ctx.stroke();
  });
  ["pointerup", "pointerleave"].forEach((eventName) => {
    canvas.addEventListener(eventName, () => {
      drawing = false;
    });
  });
  clearCanvasBtn.addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    hasDrawn = false;
  });

  function field(id) {
    return document.getElementById(id).value;
  }

  async function buildRequest() {
    const formData = new FormData();
    formData.append("file", pdfFile);

    if (mode === "draw") {
      if (!hasDrawn) throw new Error("Draw a signature first");
      const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
      formData.append("signature", blob, "signature.png");
      formData.append("page", field("field-page"));
      formData.append("x0", field("field-x0"));
      formData.append("y0", field("field-y0"));
      formData.append("x1", field("field-x1"));
      formData.append("y1", field("field-y1"));
      return { endpoint: "/api/security/sign/image", formData };
    }

    if (mode === "image") {
      const imageInput = document.getElementById("signature-image-input");
      if (!imageInput.files[0]) throw new Error("Choose a signature image first");
      formData.append("signature", imageInput.files[0]);
      formData.append("page", field("field-page"));
      formData.append("x0", field("field-x0"));
      formData.append("y0", field("field-y0"));
      formData.append("x1", field("field-x1"));
      formData.append("y1", field("field-y1"));
      return { endpoint: "/api/security/sign/image", formData };
    }

    if (mode === "type") {
      const text = document.getElementById("signature-text-input").value;
      if (!text) throw new Error("Type a signature first");
      formData.append("text", text);
      formData.append("page", field("field-page"));
      formData.append("x", field("field-x"));
      formData.append("y", field("field-y"));
      return { endpoint: "/api/security/sign/text", formData };
    }

    const pfxInput = document.getElementById("pfx-input");
    const pfxPassword = document.getElementById("pfx-password-input").value;
    if (!pfxInput.files[0]) throw new Error("Choose a certificate file first");
    formData.append("pfx", pfxInput.files[0]);
    formData.append("pfx_password", pfxPassword);
    return { endpoint: "/api/security/sign/certificate", formData };
  }

  signBtn.addEventListener("click", async () => {
    if (!pdfFile) return;
    signBtn.disabled = true;
    const originalLabel = signBtnLabel.textContent;
    signBtnLabel.textContent = "Signing...";
    resultPanel.classList.add("hidden");

    try {
      const { endpoint, formData } = await buildRequest();
      const response = await fetch(endpoint, { method: "POST", body: formData });
      await handleToolResponse(response, resultPanel);
    } catch (err) {
      showToolResult(resultPanel, `<p class="font-body-sm">${err.message}</p>`, true);
    } finally {
      signBtn.disabled = !pdfFile;
      signBtnLabel.textContent = originalLabel;
    }
  });
})();
