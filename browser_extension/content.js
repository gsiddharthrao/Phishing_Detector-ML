chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getPageContent") {
    let responsePayload = { htmlContent: '', textContent: '' };
    if (window.location.host === 'mail.google.com') {
      // Try to get the full email content including headers
      const emailContainer = document.querySelector('div.a3s.aiO') || document.querySelector('[data-message-id]');
      if (emailContainer) {
        // Extract headers if available
        let headersText = '';
        const headerElements = emailContainer.querySelectorAll('.adn.ads, .adp, .aqw'); // Gmail header classes
        headerElements.forEach(el => {
          headersText += el.textContent.trim() + '\n';
        });

        // Get body content
        const bodyElement = emailContainer.querySelector('.a3s.aiO') || emailContainer;
        const bodyText = bodyElement ? bodyElement.innerText : emailContainer.innerText;

        // Combine headers and body
        responsePayload.textContent = headersText + '\n\n' + bodyText;
        responsePayload.htmlContent = emailContainer.innerHTML;
      } else {
        // Email not opened, do not analyze
        responsePayload = {};
      }
    } else {
      // For non-Gmail pages, do not analyze (this is an email phishing detector)
      responsePayload = {};
    }
    sendResponse(responsePayload);
  }
  return true; // Required for async sendResponse
});
