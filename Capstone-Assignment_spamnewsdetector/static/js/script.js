// ============================================================
// Project  : AI Spam News Detector
// File     : static/js/script.js
// Purpose  : Fetch API prediction, history log, theme toggle
// Student  : ___________________________
// Roll No  : ___________________________
// Date     : ___________________________
// ============================================================

const textarea    = document.getElementById('newsText');
const detectBtn   = document.getElementById('detectBtn');
const btnText     = document.getElementById('btnText');
const btnSpinner  = document.getElementById('btnSpinner');
const resultBox   = document.getElementById('resultBox');
const resultBadge = document.getElementById('resultBadge');
const progressBar = document.getElementById('progressBar');
const confValue   = document.getElementById('confValue');
const resultNote  = document.getElementById('resultNote');
const errorBox    = document.getElementById('errorBox');
const charCount   = document.getElementById('charCount');
const themeToggle = document.getElementById('themeToggle');
const historySection = document.getElementById('historySection');
const historyBody = document.getElementById('historyBody');

// ── Live char count ───────────────────────────────────────
if (textarea) {
  textarea.addEventListener('input', () => {
    charCount.textContent = textarea.value.length;
  });
}

// ── Theme Toggle ──────────────────────────────────────────
const htmlEl = document.documentElement;
const savedTheme = localStorage.getItem('theme') || 'dark';
htmlEl.setAttribute('data-theme', savedTheme);
updateThemeIcon(savedTheme);

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = htmlEl.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    htmlEl.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeIcon(next);
  });
}

function updateThemeIcon(theme) {
  if (themeToggle) themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// ── Prediction History (in-memory) ───────────────────────
const history = [];

// ── Detect Button Click ───────────────────────────────────
if (detectBtn) {
  detectBtn.addEventListener('click', analyzeNews);
}

// Allow Enter (Ctrl+Enter) to trigger
if (textarea) {
  textarea.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') analyzeNews();
  });
}

async function analyzeNews() {
  const text = textarea ? textarea.value.trim() : '';

  // Client-side validation
  if (!text) {
    showError('Please paste a news article before analyzing.');
    return;
  }
  if (text.length < 20) {
    showError('Text is too short. Please enter at least 20 characters.');
    return;
  }

  // Show loading state
  setLoading(true);
  hideResult();
  hideError();

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      showError(data.error || 'Server error. Please try again.');
      return;
    }

    displayResult(data, text);
    addToHistory(data, text);

  } catch (err) {
    showError('Could not connect to the server. Make sure Flask is running on port 5000.');
  } finally {
    setLoading(false);
  }
}

// ── Display Result ────────────────────────────────────────
function displayResult(data, text) {
  const isReal = data.label === 1;
  const conf   = data.confidence;

  // Badge
  resultBadge.textContent = isReal ? '✅  REAL NEWS' : '🚫  FAKE / SPAM NEWS';
  resultBadge.className   = 'result-badge ' + (isReal ? 'real' : 'fake');

  // Progress bar (animate after show)
  progressBar.className   = 'progress-bar-fill ' + (isReal ? 'real' : 'fake');
  progressBar.style.width = '0%';

  // Box class
  resultBox.className = 'result-box ' + (isReal ? 'real-result' : 'fake-result');
  resultBox.classList.remove('hidden');

  setTimeout(() => {
    progressBar.style.width = conf + '%';
  }, 50);

  confValue.textContent = conf + '%';

  // Note
  if (isReal) {
    resultNote.textContent = 'This article shows characteristics of genuine news based on our model.';
  } else {
    resultNote.textContent = 'This article shows patterns commonly associated with fake or spam news. Always verify with trusted sources.';
  }
}

// ── History Log ───────────────────────────────────────────
function addToHistory(data, text) {
  const entry = {
    preview: text.length > 60 ? text.slice(0, 60) + '…' : text,
    prediction: data.prediction,
    confidence: data.confidence,
    label: data.label
  };

  history.unshift(entry);
  if (history.length > 5) history.pop();

  renderHistory();
}

function renderHistory() {
  if (!historySection || !historyBody) return;
  historySection.style.display = 'block';
  historyBody.innerHTML = '';

  history.forEach((item, i) => {
    const tr = document.createElement('tr');
    const badgeClass = item.label === 1 ? 'badge-real' : 'badge-fake';
    tr.innerHTML = `
      <td>${i + 1}</td>
      <td style="max-width:380px; word-break:break-word;">${escapeHtml(item.preview)}</td>
      <td class="${badgeClass}">${item.prediction}</td>
      <td>${item.confidence}%</td>
    `;
    historyBody.appendChild(tr);
  });
}

// ── UI Helpers ────────────────────────────────────────────
function setLoading(on) {
  detectBtn.disabled = on;
  if (on) {
    btnText.classList.add('hidden');
    btnSpinner.classList.remove('hidden');
  } else {
    btnText.classList.remove('hidden');
    btnSpinner.classList.add('hidden');
  }
}

function hideResult() {
  if (resultBox) resultBox.classList.add('hidden');
}

function hideError() {
  if (errorBox) { errorBox.textContent = ''; errorBox.classList.add('hidden'); }
}

function showError(msg) {
  if (errorBox) {
    errorBox.textContent = '⚠️ ' + msg;
    errorBox.classList.remove('hidden');
  }
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
