from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/db")
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
