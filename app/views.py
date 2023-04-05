from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
import mysql.connector
from datetime import datetime

# 自分で作ったファイルからインポート
from models import User, Task, db

bp = Blueprint("root", __name__, url_prefix="/")

# DBとの接続を確認するため （ヘルスチェック）
@bp.route("/db")
def db_test():
    conn = mysql.connector.connect(
        host="db",
        user="user",
        password="password",
        database="todo_app"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result[0] == 1:
        return "DBとの接続に成功しました"
    else:
        return "DBとの接続に問題が発生しました"

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('user_register.html')
    
    if request.method == 'POST':
        # 書き込まれた項目formから取得する
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(
            email = email,
            username = username,
            password = password
        )

        if User.select_by_email(email) != None:
            flash("このメールアドレスは既に登録されています", "danger")
        else:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('root.login'))
    return render_template('register.html')


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.select_by_email(email)
        if user and user.validate_password(password):
            login_user(user)
            return redirect(url_for("root.home"))
        else:
            flash("メールアドレスまたはパスワードが間違っています", "danger")
            return redirect(url_for("root.login"))

@bp.route("/", methods=["GET"])
@login_required
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", tasks=tasks)


@bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("root.login"))


@bp.route("/task/register", methods=["GET", "POST"])
@login_required
def task_register():
    if request.method == "GET":
        return render_template("task_register.html")
    
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        endtime_str = request.form.get("endtime")

        # 文字列をdatetimeオブジェクトに変換
        endtime = datetime.strptime(endtime_str, "%Y-%m-%d")

        task = Task(
            title = title,
            description = description,
            endtime = endtime,
            user_id = current_user.id
        )

        db.session.add(task)
        db.session.commit()
        return redirect(url_for("root.home"))


@bp.route("/task/update/<task_id>", methods=["GET", "POST"])
@login_required
def task_update(task_id):
    task = Task.query.filter_by(id=task_id).first()

    if request.method == "GET":
        return render_template("task_update.html", task=task)
    
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        endtime = request.form.get("endtime")

        task = Task.query.filter_by(id=task_id).first()
        task.title = title
        task.description = description
        task.endtime = endtime

        db.session.commit()
        return redirect(url_for("root.home"))


@bp.route("/task/delete/<task_id>", methods=["GET"])
@login_required
def task_delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("root.home"))


@bp.route("/task/detail/<task_id>", methods=["GET"])
@login_required
def task_detail(task_id):
    task = Task.query.filter_by(id=task_id).first()
    return render_template("task_detail.html", task=task)
