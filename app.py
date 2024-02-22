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
    return render_template('question.html', question = survey.questions[question_id])