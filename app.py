from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "super_secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app) 


responses = []


@app.route('/')
def survey_start():

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('/index.html', title=title, instructions=instructions)


@app.route('/questions/<int:question_number>')
def display_quesiton(question_number):

    # Block to prevent users from skipping questions
    if (question_number is not len(responses)):
      return redirect(f'/questions/{len(responses)}')

      # Block to redirect to thank you page after finishing survey
    if len(responses) == len(satisfaction_survey.questions):
      return redirect('/thank_you')


    question = satisfaction_survey.questions[question_number].question
    choices = satisfaction_survey.questions[question_number].choices

    return render_template('/ask_question.html', question=question, choices=choices)


@app.route('/answer', methods=["POST"])
def log_answer_and_redirect():
    # import pdb
    # pdb.set_trace()

    ans = request.form.get('answer')
    responses.append(ans)
    # print(satisfaction_survey.questions)
    # print("RESPONSES: ", responses)
    if len(responses) == len(satisfaction_survey.questions):
      return redirect("/thank_you")

    return redirect(f'/questions/{len(responses)}')


@app.route('/thank_you')
def thank_you_page():
  return render_template('/thank_you.html')