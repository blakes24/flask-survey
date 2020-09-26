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
    question = survey.questions[num]
    if len(responses) == len(survey.questions):
        flash("You have completed the survey.")
        return redirect("/thank-you")
    if num != len(responses):
        flash("Invalid question url. Please answer questions in order.")
        return redirect(f"/questions/{len(responses)}")

    return render_template(
        "question.html",
        question=question.question,
        choices=question.choices,
        title=survey.title,
        num=num,
    )


@app.route("/answer", methods=["POST"])
def record_answer():
    survey = surveys[session["survey"]]
    data = request.form["answer"]
    num = int(request.form["number"]) + 1
    next_num = str(num)
    resp = session["responses"]
    resp.append(data)
    session["responses"] = resp
    if num == len(survey.questions):
        page = "/thank-you"
    else:
        page = f"/questions/{next_num}"
    return redirect(page)


@app.route("/thank-you")
def thanks():
    return render_template("thanks.html")
