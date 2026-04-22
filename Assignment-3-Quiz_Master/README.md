# 🧠 Quiz Master - Assignment 3

A full-stack Quiz Master web application built with **HTML, CSS, Python, and Flask**.

## 📁 Project Structure

```
quiz_master/
├── app.py                  ← Flask backend (routing + logic)
├── requirements.txt        ← Python dependencies
├── README.md
├── templates/
│   ├── index.html          ← Home page (Start Quiz)
│   ├── quiz.html           ← Quiz page (MCQs + Timer)
│   └── result.html         ← Result page (Score + Feedback)
└── static/
    └── style.css           ← Full CSS styling
```

## 🚀 How to Run

### Step 1: Open this folder in VS Code

### Step 2: Open the terminal in VS Code (`Ctrl + ~`)

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the app
```bash
python app.py
```

### Step 5: Open in browser
Visit: **http://127.0.0.1:5000**

---

## ✅ Features Implemented

### Mandatory Features
- [x] Flask working application
- [x] Minimum 5 questions (10 MCQs on Web Development topics)
- [x] Home page with Start Quiz button
- [x] Quiz page with multiple-choice questions
- [x] Result page with score and feedback message
- [x] Proper CSS styling for all pages

### Bonus Features
- [x] **Restart Quiz** — button to restart from result page
- [x] **Timer** — configurable per-question timer (15/30/45/60 sec), auto-submits on timeout
- [x] **Negative Marking** — optional -0.25 per wrong answer
- [x] **Shuffle Questions** — questions and options shuffled randomly each time

---

## 📊 Evaluation Coverage

| Criteria                  | Marks | Implemented |
|---------------------------|-------|-------------|
| Project Structure & Flask | 2     | ✅           |
| HTML Design               | 2     | ✅           |
| CSS Styling               | 2     | ✅           |
| Python Logic              | 3     | ✅           |
| Presentation/Viva         | 1     | ✅           |
| **Total**                 | **10**| ✅           |

---

## 🛠️ Technologies Used

- **Python 3** — Backend logic
- **Flask** — Web framework and routing
- **HTML5** — Page structure and templates (Jinja2)
- **CSS3** — Styling with gradients, animations, responsive design
- **JavaScript** — Client-side timer and option selection
