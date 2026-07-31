# Real-Time Phishing Website Detection and Prevention Using Deep Learning

## Project Overview

This project is a real-time phishing website detection and prevention system built with deep learning. It analyzes URLs, extracts phishing-related features, predicts whether a website is legitimate or phishing, explains predictions using SHAP, stores scan activity in MongoDB, and supports integration with a React dashboard and Chrome Extension.

The system is designed for practical browser protection. A user visits or submits a URL, the backend extracts URL features, the trained TensorFlow/Keras model predicts phishing probability, and the prevention layer returns a risk level that can be shown in the dashboard or browser extension.

## Objectives

- Detect phishing URLs in real time.
- Extract meaningful URL-based features for deep learning.
- Train a TensorFlow/Keras binary classification model.
- Provide prediction confidence and risk level.
- Explain model decisions using SHAP explainability.
- Store prediction logs and analytics in MongoDB.
- Provide a FastAPI backend for dashboard and extension integration.
- Support a React analytics dashboard.
- Support a Chrome Extension for browser-based protection.

## Features

- Dataset loading and preprocessing.
- Automatic labeling of phishing and legitimate URLs.
- Duplicate and null URL removal.
- URL feature extraction.
- Deep learning model training.
- Model evaluation using accuracy, precision, recall, F1 score, ROC-AUC, and confusion matrix.
- Saved model and scaler artifacts.
- Real-time URL prediction.
- SHAP-based feature contribution explanation.
- FastAPI prediction route.
- MongoDB connection foundation.
- Starter backend services, schemas, and utilities.
- Planned dashboard analytics and Chrome Extension blocking workflow.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- TensorFlow
- Keras
- NumPy
- Pandas
- Scikit-learn
- Joblib
- SHAP
- Matplotlib
- MongoDB
- PyMongo
- Motor
- tldextract
- python-dotenv
- ReactJS
- Chrome Extension Manifest V3

## Folder Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── detection_routes.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── tests/
│   └── utils/
│
├── ml/
│   ├── preprocessing/
│   │   └── dataset_loader.py
│   ├── feature_extraction/
│   │   └── url_features.py
│   ├── training/
│   │   └── train_model.py
│   ├── inference/
│   │   └── predictor.py
│   ├── explainability/
│   │   └── shap_explainer.py
│   └── artifacts/
│       ├── README.md
│       ├── feature_columns.example.json
│       └── model_metrics.example.json
│
├── data/
│   ├── raw/
│   │   ├── phishing_urls.csv
│   │   └── legitimate_urls.csv
│   └── processed/
│       └── cleaned_dataset.csv
│
├── frontend/
├── chrome-extension/
├── requirements.txt
└── README.md
```

## Installation Steps

1. Clone or open the project folder.

2. Create a Python virtual environment.

```bash
python -m venv .venv
```

3. Activate the virtual environment.

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install Python dependencies.

```bash
pip install -r requirements.txt
```

5. Create a `.env` file if needed.

```text
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=phishing_detection
```

## Dataset Preparation

Place raw datasets inside:

```text
data/raw/
```

Required files:

```text
data/raw/phishing_urls.csv
data/raw/legitimate_urls.csv
```

Each CSV should contain a URL column. Supported column names include:

```text
url, URL, Url, link, Link, website, Website, domain, Domain
```

Run preprocessing:

```bash
python ml/preprocessing/dataset_loader.py
```

This creates:

```text
data/processed/cleaned_dataset.csv
```

The cleaned dataset contains:

```text
url,label
```

Labels:

```text
phishing = 1
legitimate = 0
```

## Model Training

Train the phishing detection model:

```bash
python ml/training/train_model.py
```

Training performs:

- URL feature extraction.
- 70/15/15 train-validation-test split.
- StandardScaler feature scaling.
- TensorFlow/Keras model training.
- EarlyStopping and ModelCheckpoint.
- Model evaluation.
- Training curve plotting.

Generated artifacts:

```text
ml/artifacts/phishing_model.keras
ml/artifacts/scaler.pkl
ml/artifacts/model_metrics.json
ml/artifacts/training_history.png
```

## Running FastAPI Backend

Start the FastAPI backend:

```bash
uvicorn backend.app.main:app --reload
```

Default API URL:

```text
http://127.0.0.1:8000
```

Health check:

```text
GET /health
```

Prediction endpoint:

```text
POST /predict
```

Example request:

```json
{
  "url": "https://example.com"
}
```

Example response:

```json
{
  "prediction": "Legitimate",
  "confidence": 98.4,
  "risk_level": "Low"
}
```

## Running React Frontend

The React frontend is planned under:

```text
frontend/
```

Expected setup:

```bash
cd frontend
npm install
npm run dev
```

Expected local URL:

```text
http://localhost:5173
```

Planned dashboard pages:

- URL scanner
- Prediction history
- Risk analytics
- SHAP explanations
- Model metrics
- Settings

## Chrome Extension Setup

The Chrome Extension is planned under:

```text
chrome-extension/
```

Expected files:

```text
manifest.json
background.js
content.js
popup.html
popup.js
warning.html
warning.js
styles/
assets/
```

Setup steps:

1. Open Chrome.
2. Go to:

```text
chrome://extensions/
```

3. Enable Developer Mode.
4. Click Load unpacked.
5. Select the `chrome-extension/` folder.
6. Ensure the FastAPI backend is running.
7. Visit a website and let the extension send the URL to the prediction API.

Planned extension behavior:

- Read active tab URL.
- Send URL to FastAPI backend.
- Show Safe, Suspicious, or Phishing result.
- Block or warn on high-risk URLs.
- Allow user feedback for false positives and false negatives.

## Future Enhancements

- Complete MongoDB persistence for scan logs and feedback.
- Add analytics aggregation routes.
- Build the React dashboard.
- Build the Chrome Extension.
- Add user authentication and role-based access.
- Add domain WHOIS, DNS, SSL, redirect, and page content features.
- Store SHAP background samples during training.
- Add model versioning.
- Add scheduled retraining pipeline.
- Add Docker and Docker Compose deployment.
- Add Nginx reverse proxy.
- Add CI tests and linting.
- Add threat intelligence feed integration.
