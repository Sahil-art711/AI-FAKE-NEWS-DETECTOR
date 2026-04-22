# 🧠 AI Spam News Detector

An end-to-end AI project that classifies news articles as **Real** or **Fake/Spam** using NLP + Machine Learning, served via a Flask web application.

---

## 🚀 How to Run (Step-by-Step)

### Step 1 — Open in VS Code
Unzip the file and open the `spam_news_detector/` folder in VS Code.

### Step 2 — Create a Virtual Environment
```bash
python -m venv venv
```

Activate it:
- **Windows:**  `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — (Optional) Add Real Dataset
Download the Kaggle Fake News Dataset and place:
- `data/fake.csv`
- `data/true.csv`

> **Without dataset:** The trainer auto-generates synthetic demo data — the app will still work!

### Step 5 — Train the Model
```bash
python train_model.py
```
This will:
- Load/generate data
- Preprocess text with NLP
- Train 3 ML models and pick the best
- Save `models/spam_detector_model.pkl` and `models/tfidf_vectorizer.pkl`
- Save `models/confusion_matrix.png`

### Step 6 — Start the Web App
```bash
python app.py
```

### Step 7 — Open in Browser
Go to: [http://localhost:5000](http://localhost:5000)

---

## 📂 Project Structure
```
spam_news_detector/
├── app.py                  # Flask API & routes
├── train_model.py          # Training pipeline
├── preprocess.py           # NLP text cleaning
├── requirements.txt
├── README.md
├── models/                 # Saved model files (generated after training)
│   ├── spam_detector_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── confusion_matrix.png
├── data/                   # Dataset (add fake.csv & true.csv here)
├── templates/
│   ├── index.html
│   └── about.html
└── static/
    ├── css/style.css
    └── js/script.js
```

---

## 🔬 Models Used
| Model | Typical Accuracy |
|---|---|
| Passive Aggressive Classifier | ~93–96% |
| Logistic Regression | ~91–94% |
| Naive Bayes | ~87–91% |

---

## 📦 Dataset Reference
- Kaggle Fake News Dataset: https://www.kaggle.com/c/fake-news/data
- LIAR Dataset: https://www.cs.ucsb.edu/~william/data/liar_dataset.zip

---

## 👤 Author
- **Student Name:** Sahil
- **Enrollment No:** _____
- **Course:** AI & ML Laboratory
