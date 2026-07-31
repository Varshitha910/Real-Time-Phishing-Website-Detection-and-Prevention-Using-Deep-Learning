// Content script loaded on web pages.
// It sends the current page URL to the background worker so pages can be
// scanned as early as possible during navigation.

chrome.runtime.sendMessage({
  type: "SCAN_CURRENT_URL",
  url: window.location.href
});

