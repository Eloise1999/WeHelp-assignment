from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import jsonify
import mysql.connector

app = Flask(__name__, static_folder="files", static_url_path="/")

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="website"
)

cursor = database.cursor()

app.secret_key = "secret key"

app.config["JSON_AS_ASCII"] = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin", methods=["POST"])
def signin():


    username = request.form["login_account"]
    password = request.form["login_password"]


    session["user_state"] = "not_logged_in"

    data = (username, password)
    select_command = "select * from member where username=%s and password=%s"

    cursor.execute(select_command, data)
    select_result = cursor.fetchall()

    if len(select_result) == 0:
        error_message = "帳號或密碼輸入錯誤"
        return redirect("/error?message=" + error_message)
    else:
        user_true_name = select_result[0][1]
        session["name"] = user_true_name
        session["id"] = select_result[0][0]
        session["follower_count"] = select_result[0][4]
        session["user_state"] = "logged_in"
        return redirect("/member")


@app.route("/member")
def member():

    user_state = session["user_state"]

    if (user_state != "logged_in"):
        return redirect("/")
    elif (user_state == "logged_in"):
        name = session["name"]
        return render_template("member.html", message=name)

@app.route("/error")
def error():
    
    error_message = request.args.get("message", None)
    
    session["user_state"] = "not_logged_in"
    
    if error_message == "帳號已經被註冊":
        return render_template("error.html", message="帳號已經被註冊")
    elif error_message == "帳號或密碼輸入錯誤":
        return render_template("error.html", message="帳號或密碼輸入錯誤")

@app.route("/signup", methods=["POST"])
def signup():

    name = request.form["signup_name"]
    username = request.form["signup_username"]
    password = request.form["signup_password"]

    select_command = "select * from member where username=%(username)s"

    cursor.execute(select_command,{'username':username})
    select_result = cursor.fetchall()

    if len(select_result) != 0:
        error_message= "帳號已經被註冊"
        return redirect("/error?message=" + error_message)
    else:
        insert_command = "insert into member(name, username, password) values (%s, %s, %s)"
        data =(name, username, password)
        cursor.execute(insert_command, data)
        cursor.execute("select * from member")
        after_insert_result = cursor.fetchall()
        print("新增後的全部資料有：", after_insert_result)
        return redirect("/")
    

@app.route("/signout")
def signout():

    session["user_state"] = "not_logged_in"

    session.pop("name", None)
    session.pop("id", None)
    session.pop("follower_count", None)
    return redirect("/")

@app.route("/api/member", methods=["GET","PATCH"])
def apiMember():
    if request.method == "GET":
        username = request.args.get("username", None)
        select_command = "select * from member where username = %(username)s"
        cursor.execute(select_command, {'username': username})
        select_result = cursor.fetchone()

        if select_result != None:
            id = select_result[0]
            name = session["name"]
            data = {
                "data": {
                    "id": id,
                    "name": name,
                    "username": username
                }
            }
            return jsonify(data)

        data = {"data": None}
        return jsonify(data)

    if request.method == "PATCH":
        if session["user_state"] == "logged_in":
            try:
                name = session["name"]
                newName = request.json["name"]
                data = (newName, name)
                update_command = "update member set name=%s where name=%s"
                cursor.execute(update_command, data)

            except:
                update_state = {"error": True}
                return jsonify(update_state)
                
            update_state = {"ok": True}
            session["name"] = newName
            return jsonify(update_state)


app.run(port=3000, debug=True)