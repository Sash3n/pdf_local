function extractFilename(contentDisposition) {
  if (!contentDisposition) return "download";
  const match = contentDisposition.match(/filename="?([^"]+)"?/);
  return match ? match[1] : "download";
}

function showToolResult(resultPanel, html, isError) {
  resultPanel.classList.remove("hidden");
  resultPanel.className = isError
    ? "rounded-2xl p-6 border border-error/30 bg-error/5 text-error"
    : "rounded-2xl p-6 border border-success-teal/30 bg-success-teal/5";
  resultPanel.innerHTML = html;
}

async function handleToolResponse(response, resultPanel) {
  const contentType = response.headers.get("content-type") || "";

  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    if (contentType.includes("application/json")) {
      const data = await response.json();
      message = data.detail || message;
    }
    showToolResult(resultPanel, `<p class="font-body-sm">${message}</p>`, true);
    return;
  }

  if (contentType.includes("application/json")) {
    const data = await response.json();
    showToolResult(
      resultPanel,
      `<pre class="font-body-sm whitespace-pre-wrap">${JSON.stringify(data, null, 2)}</pre>`,
      false
    );
    return;
  }

  const blob = await response.blob();
  const filename = extractFilename(response.headers.get("content-disposition"));
  const objectUrl = URL.createObjectURL(blob);

  if (contentType.startsWith("text/")) {
    const text = await blob.text();
    showToolResult(
      resultPanel,
      `<p class="font-title-md text-body-sm text-primary dark:text-inverse-on-surface mb-3">Result</p>
       <pre class="font-body-sm whitespace-pre-wrap bg-surface-container-low dark:bg-inverse-surface rounded-xl p-4 max-h-96 overflow-auto">${text.replace(/</g, "&lt;")}</pre>
       <a class="inline-flex items-center gap-2 mt-4 text-primary font-bold" href="${objectUrl}" download="${filename}">
         <span class="material-symbols-outlined">download</span> Download ${filename}
       </a>`,
      false
    );
  } else {
    const link = document.createElement("a");
    link.href = objectUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    showToolResult(
      resultPanel,
      `<p class="font-title-md text-body-sm text-primary dark:text-inverse-on-surface mb-2">Done</p>
       <p class="font-body-sm text-slate-gray mb-3">Your download should start automatically.</p>
       <a class="inline-flex items-center gap-2 text-primary font-bold" href="${objectUrl}" download="${filename}">
         <span class="material-symbols-outlined">download</span> Download ${filename}
       </a>`,
      false
    );
  }
}
