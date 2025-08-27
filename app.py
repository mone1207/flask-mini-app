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
    complete = db.Column(db.Boolean, default=False)

# タスク表示
@app.route("/", methods=["GET"])
def home():
    todo_list = Todo.query.all()  # DBからすべてのタスクを取得
    return render_template("index.html", todo_list=todo_list)

# タスク追加
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")  # フォームからタイトルを取得
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))  # 追加後にトップページへ戻る  

# タスク削除
@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()  # IDで対象タスクを取得
    if todo:
        db.session.delete(todo)  # DBから削除
        db.session.commit()
    return redirect(url_for("home"))  # 削除後はトップページに戻る  

# 完了フラグ
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.get(todo_id)  # IDでタスクを取得
    todo.complete = not todo.complete  # True ⇔ False を切り替え
    db.session.commit()
    return redirect(url_for("home"))

# サーバー起動
if __name__ == "__main__":
    # DBのテーブル作成
    with app.app_context():
        db.create_all()
    app.run(debug=True)