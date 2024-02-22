from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def start_survey_page():
    """Returns home page with title and instructions for survey."""
    return render_template('survey_start.html',
                           title=survey.title,
                           instructions=survey.instructions)

@app.post('/begin')
def redirect_to_questions():
    """Sets cookie for response list and redirects to first question."""
    session['responses'] = []
    return redirect('questions/0')


@app.get('/questions/<int:question_id>')
# rename as verb noun
def get_question(question_id):
    """captures id on questions and displays questions page"""
    # TODO: add guards for out of index/out of order
    if len(session['responses']) == len(survey.questions):
        return redirect('/thankyou')
    elif question_id == len(session['responses']):
        return render_template('question.html', question=survey.questions[question_id])
    else:
        return redirect(f"/questions/{len(session['responses'])}")


@app.post('/answer')
def answer_page():
    """grabbing submitted answers and redirecting to more questions."""

    answer = request.form['answer']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if len(session['responses']) == len(survey.questions):
        return redirect('/thankyou')
    else:
        return redirect(f"/questions/{len(session['responses'])}")


@app.get('/thankyou')
def thank_you_page():
    """thank you page on completion of questions"""
    return render_template('completion.html',
                           questions=survey.questions)
