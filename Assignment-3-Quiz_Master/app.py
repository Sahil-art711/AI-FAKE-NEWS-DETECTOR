from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'quizmaster_secret_key_2024'

QUESTIONS = [
    {
        "id": 1,
        "question": "Which language is used for web scripting on the client side?",
        "options": ["Python", "Java", "JavaScript", "C++"],
        "answer": "JavaScript"
    },
    {
        "id": 2,
        "question": "What does HTML stand for?",
        "options": [
            "Hyper Text Markup Language",
            "High Tech Modern Language",
            "Hyper Transfer Markup Language",
            "Home Tool Markup Language"
        ],
        "answer": "Hyper Text Markup Language"
    },
    {
        "id": 3,
        "question": "Which Python framework is used to build web applications?",
        "options": ["Django only", "Flask only", "Both Flask and Django", "Neither"],
        "answer": "Both Flask and Django"
    },
    {
        "id": 4,
        "question": "What does CSS stand for?",
        "options": [
            "Computer Style Sheets",
            "Cascading Style Sheets",
            "Creative Style Sheets",
            "Colorful Style Sheets"
        ],
        "answer": "Cascading Style Sheets"
    },
    {
        "id": 5,
        "question": "Which HTTP method is used to submit a form?",
        "options": ["GET", "POST", "PUT", "DELETE"],
        "answer": "POST"
    },
    {
        "id": 6,
        "question": "What is the correct file extension for Python files?",
        "options": [".pt", ".pyt", ".py", ".python"],
        "answer": ".py"
    },
    {
        "id": 7,
        "question": "Which tag is used to create a hyperlink in HTML?",
        "options": ["<link>", "<href>", "<a>", "<url>"],
        "answer": "<a>"
    },
    {
        "id": 8,
        "question": "In Flask, which decorator is used to define a route?",
        "options": ["@app.url()", "@app.route()", "@app.path()", "@app.view()"],
        "answer": "@app.route()"
    },
    {
        "id": 9,
        "question": "What does JSON stand for?",
        "options": [
            "JavaScript Object Notation",
            "Java Scripted Object Names",
            "JavaScript Output Node",
            "Java Simple Object Notation"
        ],
        "answer": "JavaScript Object Notation"
    },
    {
        "id": 10,
        "question": "Which of the following is NOT a valid CSS property?",
        "options": ["color", "font-size", "text-weight", "margin"],
        "answer": "text-weight"
    }
]


def get_feedback(score, total):
    percentage = (score / total) * 100
    if percentage == 100:
        return "🏆 Perfect Score! Outstanding!", "perfect"
    elif percentage >= 80:
        return "🌟 Excellent! Great job!", "excellent"
    elif percentage >= 60:
        return "👍 Good work! Keep it up!", "good"
    elif percentage >= 40:
        return "📚 Fair attempt. More practice needed.", "fair"
    else:
        return "💪 Don't give up! Try again!", "poor"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start')
def start():
    questions = QUESTIONS.copy()
    random.shuffle(questions)
    session['questions'] = questions
    session['current'] = 0
    session['score'] = 0
    session['answers'] = []
    session['negative'] = request.args.get('negative', 'false') == 'true'
    session['time_limit'] = int(request.args.get('time', 30))
    return redirect(url_for('quiz'))


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'questions' not in session:
        return redirect(url_for('index'))

    questions = session['questions']
    current = session['current']

    if request.method == 'POST':
        selected = request.form.get('answer')
        correct_answer = questions[current]['answer']
        answers = session.get('answers', [])

        if selected == correct_answer:
            session['score'] = session.get('score', 0) + 1
            answers.append({'selected': selected, 'correct': True})
        else:
            if session.get('negative'):
                session['score'] = session.get('score', 0) - 0.25
            answers.append({'selected': selected, 'correct': False, 'correct_ans': correct_answer})

        session['answers'] = answers
        session['current'] = current + 1
        current = session['current']

        if current >= len(questions):
            return redirect(url_for('result'))
        return redirect(url_for('quiz'))

    if current >= len(questions):
        return redirect(url_for('result'))

    q = questions[current]
    options = q['options'].copy()
    random.shuffle(options)

    return render_template(
        'quiz.html',
        question=q,
        options=options,
        current=current + 1,
        total=len(questions),
        time_limit=session.get('time_limit', 30),
        negative=session.get('negative', False)
    )


@app.route('/result')
def result():
    if 'questions' not in session:
        return redirect(url_for('index'))

    score = session.get('score', 0)
    total = len(session.get('questions', []))
    answers = session.get('answers', [])
    questions = session.get('questions', [])
    feedback, level = get_feedback(max(score, 0), total)

    result_data = []
    for i, q in enumerate(questions):
        ans = answers[i] if i < len(answers) else {}
        result_data.append({
            'question': q['question'],
            'selected': ans.get('selected', 'Not answered'),
            'correct_ans': q['answer'],
            'is_correct': ans.get('correct', False)
        })

    return render_template(
        'result.html',
        score=score,
        total=total,
        feedback=feedback,
        level=level,
        result_data=result_data
    )


@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
