from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "super_secret"

debug = DebugToolbarExtension(app)


responses = []


@app.route('/')
def survey_start():

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('/index.html', title=title, instructions=instructions)


@app.route('/questions/<int:question_number>')
def display_quesiton(question_number):

    question = satisfaction_survey.questions[question_number].question
    choices = satisfaction_survey.questions[question_number].choices

    return render_template('/ask_question.html', question=question, choices=choices)


@app.route('/answer', methods=["POST"])
def log_answer_and_redirect():
    import pdb
    pdb.set_trace()

    ans = request.form.get(['answer'])
    responses.append(ans)

    return redirect('/questions/<int:question_number>')
