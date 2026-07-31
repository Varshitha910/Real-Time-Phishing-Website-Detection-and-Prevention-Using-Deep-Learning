// Background service worker for real-time phishing prevention.
// It monitors tab URL changes, calls the FastAPI /predict endpoint, stores the
// latest result, and redirects phishing pages to the extension warning page.

const API_ENDPOINT = "http://127.0.0.1:8000/predict";
const WARNING_PAGE = chrome.runtime.getURL("warning.html");

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "loading" && tab.url) {
    scanTabUrl(tabId, tab.url);
  }
});

chrome.tabs.onActivated.addListener(async ({ tabId }) => {
  const tab = await chrome.tabs.get(tabId);
  if (tab?.url) {
    scanTabUrl(tabId, tab.url);
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "SCAN_CURRENT_URL" && message.url) {
    scanUrl(message.url)
      .then((result) => sendResponse({ ok: true, result }))
      .catch((error) => sendResponse({ ok: false, error: error.message }));
    return true;
  }

  if (message.type === "GET_LATEST_SCAN") {
    chrome.storage.local.get(["latestScan"], (data) => {
      sendResponse({ ok: true, result: data.latestScan || null });
    });
    return true;
  }

  return false;
});

async function scanTabUrl(tabId, url) {
  if (!shouldScanUrl(url)) {
    return;
  }

  try {
    const result = await scanUrl(url);
    await chrome.storage.local.set({ latestScan: { url, ...result, scannedAt: new Date().toISOString() } });

    if (isPhishing(result)) {
      const warningUrl = `${WARNING_PAGE}?blockedUrl=${encodeURIComponent(url)}&risk=${encodeURIComponent(result.risk_level)}`;
      await chrome.tabs.update(tabId, { url: warningUrl });
    }
  } catch (error) {
    await chrome.storage.local.set({
      latestScan: {
        url,
        prediction: "Unavailable",
        confidence: 0,
        risk_level: "Unknown",
        error: error.message,
        scannedAt: new Date().toISOString()
      }
    });
  }
}

async function scanUrl(url) {
  const response = await fetch(API_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });

  if (!response.ok) {
    const errorBody = await safeJson(response);
    throw new Error(errorBody?.detail || `Prediction API failed with status ${response.status}`);
  }

  return response.json();
}

async function safeJson(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

function shouldScanUrl(url) {
  return url.startsWith("http://") || url.startsWith("https://");
}

function isPhishing(result) {
  return String(result.prediction).toLowerCase() === "phishing" || String(result.risk_level).toLowerCase() === "high";
}

