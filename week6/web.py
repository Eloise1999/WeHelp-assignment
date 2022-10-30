# 引入相關套件
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
import mysql.connector

web = Flask(__name__, static_folder="files", static_url_path="/")

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="website"
)

cursor = database.cursor()

web.secret_key = "secret key"

@web.route("/")
def index():
    return render_template("index.html")

@web.route("/signin", methods=["POST"])
def signin():

    # 接收使用者輸入的資料
    username = request.form["login_account"]
    password = request.form["login_password"]

    # 設定使用者狀態為未登入
    session["user_state"] = "not_logged_in"
    # MySQL 指令：在資料表中選取有使用者輸入的 username & password 的資料
    data = (username, password)
    select_command = "select * from member where username=%s and password=%s"
    
    # MySQL 指令：執行
    cursor.execute(select_command, data)
    select_result = cursor.fetchall()
    
    # 若列表為空，代表資料庫中沒有使用者輸入的 username & password 的資料，轉向錯誤頁面
    # 若列表中有資料，代表帳號密碼輸入正確，紀錄 name, id, follower_count 和使用者狀態，轉向首頁
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


@web.route("/member")
def member():

    #接收使用者目前狀態
    user_state = session["user_state"]

    #若使用者狀態不為已登入，跳轉至首頁；若已登入則接收使用者姓名，跳轉至會員頁面
    if (user_state != "logged_in"):
        return redirect("/")
    elif (user_state == "logged_in"):
        name = session["name"]
        return render_template("member.html", message=name)

@web.route("/error")
def error():
    
    # 接收錯誤訊息的 query string
    error_message = request.args.get("message", None)
    
    # 設定使用者狀態為未登入
    session["user_state"] = "not_logged_in"
    
    # 將不同的 query string 傳至失敗頁面
    if error_message == "帳號已經被註冊":
        return render_template("error.html", message="帳號已經被註冊")
    elif error_message == "帳號或密碼輸入錯誤":
        return render_template("error.html", message="帳號或密碼輸入錯誤")

@web.route("/signup", methods=["POST"])
def signup():

    # 接收使用者輸入的資料
    name = request.form["signup_name"]
    username = request.form["signup_username"]
    password = request.form["signup_password"]

    # MySQL 指令：選取資料表中 username 有使用者輸入的 username 的資料
    select_command = "select * from member where username=%(username)s"

    # MySQL 指令：執行
    cursor.execute(select_command,{'username':username})
    select_result = cursor.fetchall()
    print(select_result)

    # 若列表中不為空，代表此帳號已被註冊，資料表中有重複的 username，跳轉至失敗頁面
    # 若列表中為空，代表此帳號尚未被註冊，將資料加入資料表後跳轉至首頁
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
    

@web.route("/signout")
def signout():

    # 設定使用者狀態為未登入
    session["user_state"] = "not_logged_in"

    # 移除使用者在 session 中紀錄的資料，跳轉回首頁
    session.pop("name", None)
    session.pop("id", None)
    session.pop("follower_count", None)
    return redirect("/")

web.run(port=3000)