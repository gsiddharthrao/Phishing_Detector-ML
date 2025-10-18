Phishing Detector — Browser Extension (local)
=============================================

This is a simple Chrome/Edge/Firefox extension (Manifest v3) that lets you send selected text or pasted email content to the project's local Flask API at `http://127.0.0.1:5000/predict` and shows the prediction.

How it works
- The extension popup lets you paste an email or use the page selection (select text on a page and click "Use Selection").
- On "Check Now" the extension POSTs JSON { email: <text> } to the local Flask `/predict` endpoint.

Requirements
- The project's Flask server must be running locally (see `requirements/app.py`). Start it by running:

```pwsh
python run_pipeline.py
```

Load extension (developer mode)
1. Open Chrome/Edge and go to Extensions > Manage Extensions.
2. Enable "Developer mode".
3. Click "Load unpacked" and select this `browser_extension` folder.
4. The extension will appear in the toolbar.

Notes & next steps
- The extension relies on the local Flask server. If you want a fully self-contained browser extension, the model must be converted to run in JavaScript (TensorFlow.js) or another WASM-based approach — this project does not include that conversion.
- If the local server is on a different host/port, update `popup.js` serverUrl.
