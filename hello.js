function reloadExtension() {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          files: ["content.js"], // Re-inject content script
        }, () => {
          console.log("Content script re-injected successfully!");
        });
      } else {
        console.error("No active tab found!");
      }
    });
  }