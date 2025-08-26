from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DBの設定（同じフォルダに db.sqlite が作られる）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# Todoモデル（テーブル定義）
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

# タスク表示
@app.route("/", methods=["GET"])
def home():
    todo_list = Todo.query.all()  # DBからすべてのタスクを取得
    return render_template("index.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")  # フォームからタイトルを取得
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))  # 追加後にトップページへ戻る

# DBのテーブル作成
with app.app_context():
    db.create_all()

# サーバー起動
if __name__ == "__main__":
    app.run(debug=True)