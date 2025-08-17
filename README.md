# Phishing Detector MVP

This is a proof-of-concept Minimum Viable Product (MVP) for detecting phishing websites using a Random Forest classifier. It leverages a subset of features from the UCI Phishing Websites Dataset and provides a user-friendly FastAPI web app with Jinja2 templates, featuring a modern orange-themed UI with animations and detailed prediction outputs.

## Project Structure
```
phishing_detector/
├── data/
│   └── phishing_dataset.csv
├── models/
│   └── random_forest_model.pkl
├── results/
│   ├── metrics.txt
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   ├── precision_recall_curve.png
│   └── feature_importances.png
├── src/
│   ├── data_preprocessing.py
│   ├── feature_extraction.py
│   ├── train_model.py
├── templates/
│   ├── index.html
│   └── result.html
├── main.py
├── requirements.txt
├── runserver.sh
├── runserver.bat
└── README.md
```

## Installation and Setup
The project includes automation scripts (`runserver.sh` for Unix/macOS, `runserver.bat` for Windows) to streamline setup. These scripts:
- Create and activate a virtual environment (`env`) if it doesn't exist.
- Install dependencies from `requirements.txt`.
- Configure the Git remote to use SSH (`git@github.com:Levi-Chinecherem/phishing-detector.git`).
- Train the model if `models/random_forest_model.pkl` is missing.
- Start the FastAPI server and open `http://127.0.0.1:8000` in your default browser.

### Steps
1. **Ensure Prerequisites**:
   - Python 3.8+ installed (`python3` on Unix/macOS, `python` on Windows).
   - SSH keys set up for GitHub (see [GitHub SSH setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)).
2. **Run the Script**:
   - **Unix/macOS**:
     ```bash
     chmod +x runserver.sh
     ./runserver.sh
     ```
   - **Windows**:
     ```cmd
     runserver.bat
     ```

### Manual Setup (Alternative)
1. Create a virtual environment (optional):
   ```bash
   python -m venv env
   ```
2. Activate it:
   - Unix/macOS: `source env/bin/activate`
   - Windows: `env\Scripts\activate.bat`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Train the model:
   ```bash
   python src/train_model.py
   ```
5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
6. Open `http://127.0.0.1:8000` in your browser.

## Example Prediction Steps
1. Navigate to `http://127.0.0.1:8000`.
2. Enter a URL (e.g., `https://www.google.com`).
3. Click "Scan for Phishing".
4. View the result page, showing:
   - The entered URL (wrapped for long URLs).
   - Classification (Phishing or Legitimate).
   - Confidence score (e.g., 95.67%).
   - A table of extracted features and their values.

## Dataset
The UCI "Phishing Websites Dataset" is used, containing pre-extracted URL features with values -1 (suspicious), 0 (neutral), 1 (legitimate). The target is "Result" (1: legitimate, -1: phishing). No missing values; all features are integer-encoded.

## Data Preprocessing
- Loaded with Pandas.
- Selected a subset of URL-based features.
- No scaling or encoding needed for Random Forest.

## Feature Engineering
The MVP uses a subset of dataset features, extracted in real-time from URLs:
- `having_IP_Address`: -1 if hostname is an IP address, 1 otherwise.
- `URL_Length`: 1 if <54 chars, 0 if 54–75, -1 if >75.
- `Shortining_Service`: -1 if domain is a known URL shortener, 1 otherwise.
- `having_At_Symbol`: -1 if '@' is present, 1 otherwise.
- `double_slash_redirecting`: -1 if '//' appears after protocol, 1 otherwise.
- `Prefix_Suffix`: -1 if '-' in hostname, 1 otherwise.
- `having_Sub_Domain`: 1 if ≤1 dots in hostname, 0 if 2, -1 if >2.
- `SSLfinal_State`: Approximated as 1 if HTTPS, -1 otherwise (simplified for POC).
- `HTTPS_token`: -1 if 'https' in hostname, 1 otherwise.

The `extract_features_from_url(url)` function in `feature_extraction.py` computes these for predictions.

## Model Training and Evaluation
Run `python src/train_model.py` to:
- Train a Random Forest Classifier (scikit-learn) on a 20% test split.
- Evaluate with:
  - Accuracy, Precision, Recall, F1-score (saved to `results/metrics.txt`).
  - Confusion Matrix (saved as `results/confusion_matrix.png`).
  - ROC Curve (saved as `results/roc_curve.png`).
  - Precision-Recall Curve (saved as `results/precision_recall_curve.png`).
  - Feature Importances (saved as `results/feature_importances.png`).
- Save the model to `models/random_forest_model.pkl`.

## Git Setup
The project uses an SSH-based Git remote (`git@github.com:Levi-Chinecherem/phishing-detector.git`). The setup scripts automatically configure this. To push changes manually:
```bash
git push -u origin main
```

## Notes
- This is a POC; production systems should include additional features (e.g., WHOIS data, page content analysis).
- `SSLfinal_State` is approximated; full implementation requires certificate validation.
- Suspicious keywords feature can be added for enhanced detection.
- Long URLs are handled with proper text wrapping in the UI.
- The UI uses a warning-themed orange gradient with animations for a modern look.
