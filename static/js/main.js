// Auto-dismiss flash messages after 4 seconds
document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => el.remove(), 4000);
});

// Live preview of color changes
const colorInputs = document.querySelectorAll('input[type="color"]');
colorInputs.forEach(input => {
  input.addEventListener('input', () => {
    document.documentElement.style.setProperty(
      `--preview-${input.name.replace('_color', '')}`, input.value
    );
  });
});

// File input preview
document.querySelectorAll('input[type="file"][accept*="image"]').forEach(input => {
  input.addEventListener('change', function() {
    const files = Array.from(this.files);
    const existingPreview = this.parentElement.querySelector('.file-preview');
    if (existingPreview) existingPreview.remove();
    if (files.length === 0) return;
    const preview = document.createElement('div');
    preview.className = 'file-preview';
    preview.style.cssText = 'display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;';
    files.forEach(file => {
      const img = document.createElement('img');
      img.style.cssText = 'width:80px;height:80px;object-fit:cover;border-radius:6px;';
      img.src = URL.createObjectURL(file);
      preview.appendChild(img);
    });
    this.parentElement.appendChild(preview);
  });
});

// Copy-to-clipboard buttons
document.addEventListener('click', async (e) => {
  const btn = e.target.closest('[data-copy]');
  if (!btn) return;
  const text = btn.getAttribute('data-copy');
  if (!text) return;

  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
    } else {
      const tmp = document.createElement('textarea');
      tmp.value = text;
      tmp.style.position = 'fixed';
      tmp.style.opacity = '0';
      document.body.appendChild(tmp);
      tmp.select();
      document.execCommand('copy');
      tmp.remove();
    }
    const prev = btn.textContent;
    btn.textContent = 'Copied';
    setTimeout(() => (btn.textContent = prev), 1200);
  } catch (_) {
    // no-op
  }
});
