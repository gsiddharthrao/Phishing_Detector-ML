# TODO List for Enhancing Phishing Email Detection Project

## 1. Fix Dockerfile
- [x] Correct the path to requirements.txt (it's in requirements/ folder).

## 2. Add Logging and Error Handling
- [x] Implement logging in the Flask app (requirements/app.py).
- [x] Add try-except blocks for robustness in prediction functions.

## 3. Enhance UI for Batch Prediction
- [x] Add a batch email input section in the web interface (requirements/templates/index.html).
- [x] Update JavaScript to handle batch submissions.

## 4. Add Word Cloud Visualizations
- [x] Generate word clouds for phishing vs. non-phishing emails in train.py.
- [x] Save word cloud images to models/ folder.
- [x] Display them in the UI.

## 5. Improve Model Selection
- [x] Modify train.py to save all trained models (not just the best one).
- [x] Update predict.py to accept model selection.
- [x] Add model selection dropdown in the UI.

## 6. Add More Metrics Visualization
- [x] Generate ROC curve or precision-recall curve in train.py.
- [x] Save the plot and display in metrics section.

## 7. Update README
- [x] Generate actual screenshots (run the app and capture).
- [x] Ensure all features are documented accurately.

## 8. Clean Up
- [x] Check for and remove any junk files (none apparent).

## 9. Test the Pipeline
- [x] Run the full pipeline to ensure everything works.
- [x] Fix any issues encountered.

## Additional Hackathon Enhancements
- [x] Add demo data generation for quick testing.
- [x] Improve UI responsiveness and add animations.
- [x] Add export functionality for results.
- [x] Ensure mobile-friendliness.
