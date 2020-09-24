from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "shhhItsAsecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start():
    title = satisfaction_survey.title
    instructions  = satisfaction_survey.instructions
    return render_template('start.html', title=title, instructions=instructions)

@app.route('/questions/<int:num>')
def show_question(num):
    if len(responses) == len(satisfaction_survey.questions):
        flash('You have completed the survey.')
        return redirect('/thank-you')
    if num != len(responses):
        flash('Invalid question url. Please answer questions in order.')
        return redirect(f'/questions/{len(responses)}') 
         
    question = satisfaction_survey.questions[num]
    return render_template('question.html', question=question.question, choices=question.choices, title = satisfaction_survey.title, num=num)

@app.route('/answer', methods=["POST"])
def record_answer():
    data = request.form['answer']
    num = int(request.form['number']) + 1
    next_num = str(num)
    responses.append(data)
    if num == len(satisfaction_survey.questions):
        page = '/thank-you'
    else:
        page = f'/questions/{next_num}'
    return redirect(page)

@app.route('/thank-you')
def thanks():
    return render_template('thanks.html')

