from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from datetime import timedelta
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

SESSION_RESPONSES_KEY = 'responses'
SESSION_SURVEY_CODE_KEY = 'survey_code'


@app.get('/')
def get_surveys_menu():
    """Returns dropdown menu with survey options"""
    return render_template('surveys_menu.html', surveys=surveys)

@app.get('/start_survey')
def start_survey_page():
    """Returns home page with title and instructions for survey.
    Also sets cookie for survey choice."""

    if (request.cookies.get(request.args['survey_code'])):
        flash("You already completed this survey")
        return redirect('/thankyou')

    session[SESSION_SURVEY_CODE_KEY] = request.args['survey_code']
    survey = surveys[request.args['survey_code']]

    return render_template('survey_start.html',
                           title=survey.title,
                           instructions=survey.instructions)


@app.post('/begin')
def redirect_to_questions():
    """Sets cookie for response list and redirects to first question."""
    session[SESSION_RESPONSES_KEY] = []
    return redirect('questions/0')


@app.get('/questions/<int:question_id>')
def get_question(question_id):
    """captures id on questions and displays questions page"""

    survey = surveys[session[SESSION_SURVEY_CODE_KEY]]
    if len(session[SESSION_RESPONSES_KEY]) == len(survey.questions):
        flash("You're already finished")
        return redirect('/thankyou')
    elif question_id == len(session['responses']):
        return render_template('question.html', question=survey.questions[question_id])
    else:
        flash('Please answer questions in order.')
        return redirect(f"/questions/{len(session['responses'])}")


@app.post('/answer')
def answer_page():
    """grabbing submitted answers and redirecting to more questions.
    if all questions answered, set cookie and redirect to thank you page."""

    answer = {
                "choice": request.form['choice'],
                "comment": request.form.get('comment')
            }
    responses = session[SESSION_RESPONSES_KEY]
    responses.append(answer)
    session[SESSION_RESPONSES_KEY] = responses

    survey = surveys[session[SESSION_SURVEY_CODE_KEY]]

    if len(session[SESSION_RESPONSES_KEY]) == len(survey.questions):
        resp = make_response(redirect('/thankyou'))
        resp.set_cookie(session[SESSION_SURVEY_CODE_KEY],
                        "True",
                        max_age=timedelta(days=400))
        return resp
    else:
        return redirect(f"/questions/{len(session[SESSION_RESPONSES_KEY])}")


@app.get('/thankyou')
def thank_you_page():
    """thank you page on completion of questions"""
    survey = surveys[session[SESSION_SURVEY_CODE_KEY]]
    return render_template('completion.html',
                           questions=survey.questions)
