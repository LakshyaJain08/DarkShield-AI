document.getElementById('analyzeBtn').addEventListener('click', async () => {
  const btn = document.getElementById('analyzeBtn');
  const loader = document.getElementById('loader');
  const resultDiv = document.getElementById('result');
  const errorDiv = document.getElementById('error');
  const model = document.getElementById('modelSelect').value;

  btn.disabled = true;
  loader.classList.remove('hidden');
  resultDiv.classList.add('hidden');
  errorDiv.classList.add('hidden');

  try {
    // Get current active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (!tab || !tab.url) {
      throw new Error("Could not detect active tab URL.");
    }

    // Call local FastAPI backend
    const response = await fetch('http://127.0.0.1:8000/analyze/url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: tab.url,
        model: model
      })
    });

    const data = await response.json();

    if (data.status === 'success') {
      const result = data.data;
      
      const statusBadge = document.getElementById('statusBadge');
      const confVal = document.getElementById('confidenceVal');

      if (result.is_dark_pattern) {
        statusBadge.className = 'status-badge status-danger';
        statusBadge.textContent = 'Potential Dark Pattern Detected';
        if (confVal) {
          confVal.textContent = `${(result.confidence * 100).toFixed(1)}%`;
          confVal.style.color = '#fca5a5';
        }
      } else {
        statusBadge.className = 'status-badge status-safe';
        statusBadge.textContent = 'Verified Clean';
        if (confVal) {
          confVal.textContent = `${((1 - result.confidence) * 100).toFixed(1)}%`;
          confVal.style.color = '#6ee7b7';
        }
      }

      document.getElementById('extractedText').textContent = result.text || 'No text extracted.';

      const shapWords = document.getElementById('shapWords');
      shapWords.innerHTML = '';
      
      if (result.explanation && result.explanation.length > 0) {
        result.explanation.forEach(item => {
          if (item.contribution > 0) {
            const span = document.createElement('span');
            span.className = 'shap-word';
            span.textContent = item.word;
            shapWords.appendChild(span);
          }
        });
      } else {
        shapWords.innerHTML = '<span style="font-size: 11px; color: #64748b; font-style: italic;">No manipulative tokens flagged.</span>';
      }

      resultDiv.classList.remove('hidden');
    } else {
      throw new Error(data.detail || data.message || "Analysis failed.");
    }

  } catch (err) {
    errorDiv.textContent = err.message || "Failed to connect to backend.";
    errorDiv.classList.remove('hidden');
  } finally {
    btn.disabled = false;
    loader.classList.add('hidden');
  }
});
