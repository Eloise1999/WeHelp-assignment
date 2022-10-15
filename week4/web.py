from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session

web = Flask(__name__, static_folder="files", static_url_path="/")

web.secret_key="secret string"

@web.route("/")
def index():
    session["user_state"] = "not_logged_in"
    return render_template("index.html")

@web.route("/signin", methods=["POST"])
def signin():
    account = request.form["account"]
    password = request.form["password"]

    if (account == "test") & (password == "test"):
        session["user_state"] = "logged_in"
        return redirect("./member")
    elif (account == "") or (password == ""):
        session["user_state"] = "not_logged_in"
        message = "請輸入帳號、密碼"
        return redirect("/error?message=" + message)
    else:
        session["user_state"] = "not_logged_in"
        message = "帳號、或密碼輸入錯誤"
        return redirect("/error?message=" + message)


@web.route("/member")
def success():
    user_state = session["user_state"]
    if user_state == "logged_in":
        return render_template("member.html")
    else:
        return redirect("/")

@web.route("/error", methods=["GET"])
def error():
    message = request.args.get("message","")
    session["user_state"] = "not_logged_in"

    if message == "請輸入帳號、密碼":
        return render_template("error.html", message="請輸入帳號、密碼")
    elif message == "帳號、或密碼輸入錯誤":
        return render_template("error.html", message="帳號、或密碼輸入錯誤")

@web.route("/signout", methods=["GET"])
def signout():
    session["user_state"] = "not_logged_in"
    return redirect("/")

@web.route("/square", methods=["POST"])
def square():
    num = request.form["number"]
    return redirect("/square/" + num)

@web.route("/square/<data>")
def calculate(data):
    calculate_num = eval(data)**2
    return render_template("square.html", square_num=calculate_num)

web.run(port=3000)