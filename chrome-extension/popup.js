// Popup controller. It displays the latest scan result and lets the user scan
// the active tab again from the extension popup.

const currentUrlElement = document.getElementById("currentUrl");
const predictionElement = document.getElementById("prediction");
const confidenceElement = document.getElementById("confidence");
const riskBadgeElement = document.getElementById("riskBadge");
const messageElement = document.getElementById("message");
const scanButton = document.getElementById("scanButton");

document.addEventListener("DOMContentLoaded", loadCurrentStatus);
scanButton.addEventListener("click", scanActiveTab);

async function loadCurrentStatus() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  currentUrlElement.textContent = tab?.url || "No active tab";

  chrome.runtime.sendMessage({ type: "GET_LATEST_SCAN" }, (response) => {
    if (response?.result) {
      renderResult(response.result);
    } else {
      messageElement.textContent = "No scan result is available yet.";
    }
  });
}

async function scanActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.url) {
    renderError("No active tab URL found.");
    return;
  }

  scanButton.disabled = true;
  scanButton.textContent = "Scanning";
  messageElement.textContent = "Scanning current tab.";

  chrome.runtime.sendMessage({ type: "SCAN_CURRENT_URL", url: tab.url }, (response) => {
    scanButton.disabled = false;
    scanButton.textContent = "Scan Again";

    if (!response?.ok) {
      renderError(response?.error || "Scan failed.");
      return;
    }

    renderResult({ url: tab.url, ...response.result });
  });
}

function renderResult(result) {
  currentUrlElement.textContent = result.url || "Unknown URL";
  predictionElement.textContent = result.prediction || "Unknown";
  confidenceElement.textContent = `${Number(result.confidence || 0).toFixed(2)}%`;
  riskBadgeElement.textContent = result.risk_level || "Unknown";
  riskBadgeElement.className = `badge ${riskClass(result.risk_level)}`;

  if (String(result.prediction).toLowerCase() === "phishing") {
    messageElement.textContent = "This website is likely phishing. Avoid entering sensitive information.";
  } else {
    messageElement.textContent = "No phishing classification was returned for this URL.";
  }
}

function renderError(message) {
  predictionElement.textContent = "Unavailable";
  confidenceElement.textContent = "0%";
  riskBadgeElement.textContent = "Unknown";
  riskBadgeElement.className = "badge badge-unknown";
  messageElement.textContent = message;
}

function riskClass(riskLevel) {
  const value = String(riskLevel || "").toLowerCase();
  if (value === "high") {
    return "badge-high";
  }
  if (value === "medium") {
    return "badge-medium";
  }
  if (value === "low") {
    return "badge-low";
  }
  return "badge-unknown";
}

