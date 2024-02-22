from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []


@app.get('/')
def start_survey_page():
    """Returns home page with title and instructions for survey."""
    return render_template('survey_start.html',
                           title=survey.title,
                           instructions=survey.instructions)


@app.get('/questions/<int:question_id>')
def question(question_id):
    """captures id on questions and displays questions page"""
    return render_template('question.html', question=survey.questions[question_id])


@app.post('/answer')
def answer_page():
    """grabbing subbmited answers and redirecting to more questions."""

    answers_from_form = request.form['answer']
    responses.append(answers_from_form)

    if len(responses) == len(survey.questions):
        return redirect('/thankyou')
    else:
        return redirect(f"/questions/{len(responses)}")


@app.get('/thankyou')
def thank_you_page():
    """thank you page on completion of questions"""
    return render_template('completion.html')
