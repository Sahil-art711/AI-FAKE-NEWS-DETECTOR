# ============================================================
# Project  : AI Spam News Detector
# File     : app.py
# Purpose  : Flask web application & prediction API
# Student  : ___________________________
# Roll No  : ___________________________
# Date     : ___________________________
# ============================================================

import os
import json
import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify

from preprocess import clean_text

app = Flask(__name__)

# ── Load Model & Vectorizer at Startup ───────────────────────
BASE_DIR   = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'spam_detector_model.pkl')
TFIDF_PATH = os.path.join(BASE_DIR, 'models', 'tfidf_vectorizer.pkl')

model  = None
tfidf  = None

def load_artifacts():
    global model, tfidf
    if os.path.exists(MODEL_PATH) and os.path.exists(TFIDF_PATH):
        model = joblib.load(MODEL_PATH)
        tfidf = joblib.load(TFIDF_PATH)
        print("✅ Model and vectorizer loaded successfully.")
    else:
        print("⚠  Model not found. Please run `python train_model.py` first.")

load_artifacts()


# ── Helper: Get Top Influential Words ────────────────────────
def get_top_words(n=10):
    """Returns top FAKE and REAL indicator words from the model."""
    try:
        feature_names = np.array(tfidf.get_feature_names_out())
        coef = model.coef_[0] if hasattr(model, 'coef_') else None
        if coef is None:
            return [], []
        top_fake = feature_names[np.argsort(coef)[:n]].tolist()
        top_real = feature_names[np.argsort(coef)[-n:][::-1]].tolist()
        return top_fake, top_real
    except Exception:
        return [], []


# ── Routes ───────────────────────────────────────────────────

@app.route('/')
def index():
    """Home page with news input form."""
    top_fake, top_real = get_top_words(8)
    model_ready = model is not None and tfidf is not None
    return render_template('index.html',
                           model_ready=model_ready,
                           top_fake=top_fake,
                           top_real=top_real)


@app.route('/predict', methods=['POST'])
def predict():
    """
    POST /predict
    Body (JSON): { "text": "<news article>" }
    Returns: { "prediction": "REAL"|"FAKE", "confidence": 87.5, "label": 1|0 }
    """
    if model is None or tfidf is None:
        return jsonify({
            'error': 'Model not loaded. Please run train_model.py first.'
        }), 503

    data = request.get_json(silent=True) or {}
    text = data.get('text', '').strip()

    # Edge case: empty or too short
    if not text:
        return jsonify({'error': 'Please provide news text.'}), 400
    if len(text) < 20:
        return jsonify({'error': 'Text too short. Please enter at least 20 characters.'}), 400

    # Preprocess & predict
    cleaned = clean_text(text)
    vec     = tfidf.transform([cleaned])

    label      = int(model.predict(vec)[0])
    prediction = 'REAL' if label == 1 else 'FAKE'

    # Confidence (use decision_function or predict_proba if available)
    try:
        if hasattr(model, 'predict_proba'):
            proba      = model.predict_proba(vec)[0]
            confidence = float(round(max(proba) * 100, 1))
        elif hasattr(model, 'decision_function'):
            score      = float(model.decision_function(vec)[0])
            confidence = float(round(min(abs(score) * 25 + 50, 99.9), 1))
        else:
            confidence = 80.0
    except Exception:
        confidence = 80.0

    return jsonify({
        'prediction': prediction,
        'confidence': confidence,
        'label': label
    })


@app.route('/about')
def about():
    """About page describing the project."""
    return render_template('about.html')


# ── Run ──────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
