const serverUrl = 'http://127.0.0.1:5000/predict'; // local Flask server

document.addEventListener('DOMContentLoaded', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab) {
    chrome.tabs.sendMessage(tab.id, { action: "getPageContent" }, (response) => {
      if (chrome.runtime.lastError) {
        showError('Could not get page content. Try reloading the page.');
        return;
      }
      if (response && response.textContent) {
        checkContent(response.textContent);
      } else {
        showError('No email content found. Please open an email to analyze.');
      }
    });
  }
});

async function checkContent(content) {
  const emailText = content.trim();
  if (!emailText) {
    showError('No text content found on this page.');
    return;
  }

  showLoading('Analyzing...');

  try {
    const resp = await fetch(serverUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: emailText })
    });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      showError('Server error: ' + (err.error || resp.statusText));
      return;
    }
    const data = await resp.json();
    showResult(data);
  } catch (e) {
    showError('Could not reach local server. Is the pipeline running?');
  }
}

function showLoading(message) {
  const status = document.getElementById('status');
  status.className = 'status loading';
  status.innerHTML = `<div class="spinner"></div>${message}`;
  document.getElementById('result').style.display = 'none';
}

function showError(message) {
  const status = document.getElementById('status');
  status.className = 'status error';
  status.textContent = message;
  document.getElementById('result').style.display = 'none';
}

function showResult(data) {
  document.getElementById('status').style.display = 'none';
  const r = document.getElementById('result');
  const confidencePercent = (Number(data.confidence) * 100).toFixed(0);
  const isPhishing = data.prediction === 'Phishing';

  r.className = 'result ' + (isPhishing ? 'phishing' : 'not-phishing');
  r.style.display = 'block';

  r.innerHTML = `
    <strong>${data.prediction}</strong>
    <div class="confidence-bar">
      <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
    </div>
    <p>We are <strong>${confidencePercent}%</strong> confident in this result.</p>
    ${data.explanation ? `<div class="explanation">${data.explanation}</div>` : ''}
  `;
}
