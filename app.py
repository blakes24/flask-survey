from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config["SECRET_KEY"] = "shhhItsAsecret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def pick_survey():
    options = list(surveys.keys())
    return render_template("pick.html", options=options)


@app.route("/start")
def start():
    # pick = request.args["survey"]
    session["survey"] = request.args["survey"]
    survey_pick = surveys[session["survey"]]
    title = survey_pick.title
    instructions = survey_pick.instructions
    return render_template("start.html", title=title, instructions=instructions)


@app.route("/responses", methods=["POST"])
def set_responses():
    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions/<int:num>")
def show_question(num):
    responses = session["responses"]
    survey = surveys[session["survey"]]
    if len(responses) == len(survey.questions):
        flash("You have completed the survey.")
        return redirect("/thank-you")
    if num != len(responses):
        flash("Invalid question url. Please answer questions in order.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[num]
    return render_template(
        "question.html",
        question=question.question,
        choices=question.choices,
        title=survey.title,
        text=question.allow_text,
        num=num,
    )


@app.route("/answer", methods=["POST"])
def record_answer():
    survey = surveys[session["survey"]]
    data = request.form["answer"]
    num = int(request.form["number"])
    next_num = str(num + 1)
    resp = session["responses"]
    if survey.questions[num].allow_text == True:
        answer = {"answer": data, "comment": request.form["comment"]}
        resp.append(answer)
    else:
        resp.append(data)

    session["responses"] = resp
    if int(next_num) == len(survey.questions):
        page = "/thank-you"
    else:
        page = f"/questions/{next_num}"
    return redirect(page)


@app.route("/thank-you")
def thanks():
    survey = surveys[session["survey"]].questions
    questions = []
    for q in survey:
        questions.append(q.question)
    responses = session["responses"]
    answers = dict(zip(questions, responses))
    return render_template("thanks.html", answers=answers)
