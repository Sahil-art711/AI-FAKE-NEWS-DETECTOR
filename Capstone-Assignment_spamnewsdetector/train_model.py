# ============================================================
# Project  : AI Spam News Detector
# File     : train_model.py
# Purpose  : Data loading, EDA, model training & evaluation
# Student  : ___________________________
# Roll No  : ___________________________
# Date     : ___________________________
# ============================================================

import os
import pandas as pd
import numpy as np
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier, LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (accuracy_score, confusion_matrix,
                              classification_report)

from preprocess import clean_text

# ── Paths ────────────────────────────────────────────────────
DATA_DIR   = os.path.join(os.path.dirname(__file__), 'data')
MODEL_DIR  = os.path.join(os.path.dirname(__file__), 'models')
FAKE_CSV   = os.path.join(DATA_DIR,  'fake.csv')
TRUE_CSV   = os.path.join(DATA_DIR,  'true.csv')
MODEL_PATH = os.path.join(MODEL_DIR, 'spam_detector_model.pkl')
TFIDF_PATH = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')

os.makedirs(MODEL_DIR, exist_ok=True)


# ── 1. Load & Label Data ─────────────────────────────────────
def load_data():
    print("\n[1/6] Loading dataset...")

    if not os.path.exists(FAKE_CSV) or not os.path.exists(TRUE_CSV):
        print("⚠  Dataset not found in data/. Generating synthetic demo data...")
        return _generate_demo_data()

    fake = pd.read_csv(FAKE_CSV)
    true = pd.read_csv(TRUE_CSV)

    fake['label'] = 0   # 0 = FAKE
    true['label'] = 1   # 1 = REAL

    df = pd.concat([fake, true], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle

    # Use 'text' column; fallback to 'title' if missing
    if 'text' not in df.columns and 'title' in df.columns:
        df['text'] = df['title']
    elif 'text' in df.columns and 'title' in df.columns:
        df['text'] = df['title'].fillna('') + ' ' + df['text'].fillna('')

    df = df[['text', 'label']].dropna()
    return df


def _generate_demo_data():
    """Creates 1000-row synthetic dataset for demo/testing purposes."""
    import random
    random.seed(42)

    fake_phrases = [
        "shocking secret governments hide from you",
        "miracle cure doctors don't want you to know",
        "exclusive leaked documents expose elite conspiracy",
        "you won't believe what celebrities are doing now",
        "breaking aliens spotted near government facility",
        "deep state exposed by whistleblower insider",
        "banned video reveals truth about vaccines",
        "scientists baffled by this strange discovery",
    ]
    real_phrases = [
        "parliament passed new budget for infrastructure",
        "research published in nature journal confirms findings",
        "central bank announces interest rate decision",
        "government releases annual economic survey data",
        "university study links exercise to improved health",
        "stock markets close higher amid positive earnings",
        "weather forecast predicts above normal rainfall",
        "election commission announces polling schedule",
    ]

    rows = []
    for _ in range(500):
        rows.append({'text': random.choice(fake_phrases) + ' ' +
                     ' '.join(random.choices(fake_phrases, k=3)), 'label': 0})
    for _ in range(500):
        rows.append({'text': random.choice(real_phrases) + ' ' +
                     ' '.join(random.choices(real_phrases, k=3)), 'label': 1})

    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    return df


# ── 2. EDA ───────────────────────────────────────────────────
def perform_eda(df):
    print("\n[2/6] Exploratory Data Analysis")
    print(f"  Shape          : {df.shape}")
    print(f"  Null values    : {df.isnull().sum().to_dict()}")
    print(f"  Class dist.    : {df['label'].value_counts().to_dict()}  (0=FAKE, 1=REAL)")
    print(f"  Avg text length: {df['text'].str.len().mean():.0f} chars")


# ── 3. Preprocess ────────────────────────────────────────────
def preprocess_data(df):
    print("\n[3/6] Preprocessing text (this may take a minute)...")
    df['clean_text'] = df['text'].apply(clean_text)
    df = df[df['clean_text'].str.strip() != '']
    return df


# ── 4. TF-IDF Vectorization ──────────────────────────────────
def vectorize(df):
    print("\n[4/6] TF-IDF Vectorization...")
    X_train, X_test, y_train, y_test = train_test_split(
        df['clean_text'], df['label'],
        test_size=0.2, random_state=42, stratify=df['label']
    )

    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_vec = tfidf.fit_transform(X_train)
    X_test_vec  = tfidf.transform(X_test)

    joblib.dump(tfidf, TFIDF_PATH)
    print(f"  Vectorizer saved → {TFIDF_PATH}")

    return X_train_vec, X_test_vec, y_train, y_test, tfidf


# ── 5. Train & Evaluate Models ───────────────────────────────
def train_and_evaluate(X_train, X_test, y_train, y_test):
    print("\n[5/6] Training models...")

    models = {
        'Passive Aggressive': PassiveAggressiveClassifier(max_iter=50, random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Naive Bayes':         MultinomialNB(),
    }

    results = {}
    best_acc = 0
    best_model = None
    best_name = ''

    print(f"\n  {'Model':<25} {'Accuracy':>10}")
    print("  " + "-" * 36)

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc   = accuracy_score(y_test, preds)
        results[name] = {'model': model, 'preds': preds, 'acc': acc}
        print(f"  {name:<25} {acc*100:>9.2f}%")

        if acc > best_acc:
            best_acc   = acc
            best_model = model
            best_name  = name

    print(f"\n  ✅ Best model: {best_name} ({best_acc*100:.2f}%)")

    # Detailed report for best model
    print(f"\n--- Classification Report ({best_name}) ---")
    print(classification_report(y_test, results[best_name]['preds'],
                                 target_names=['FAKE', 'REAL']))

    # Confusion matrix plot
    _plot_confusion_matrix(y_test, results[best_name]['preds'], best_name)

    return best_model, best_name


def _plot_confusion_matrix(y_test, preds, model_name):
    cm = confusion_matrix(y_test, preds)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['FAKE', 'REAL'],
                yticklabels=['FAKE', 'REAL'])
    plt.title(f'Confusion Matrix – {model_name}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    out = os.path.join(MODEL_DIR, 'confusion_matrix.png')
    plt.savefig(out)
    print(f"  Confusion matrix saved → {out}")
    plt.close()


# ── 6. Save Best Model ───────────────────────────────────────
def save_model(model):
    print("\n[6/6] Saving best model...")
    joblib.dump(model, MODEL_PATH)
    print(f"  Model saved → {MODEL_PATH}")


# ── Main ─────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("   AI Spam News Detector — Model Training")
    print("=" * 50)

    df = load_data()
    perform_eda(df)
    df = preprocess_data(df)
    X_train, X_test, y_train, y_test, tfidf = vectorize(df)
    best_model, best_name = train_and_evaluate(X_train, X_test, y_train, y_test)
    save_model(best_model)

    print("\n✅ Training complete! Run `python app.py` to start the web app.")
